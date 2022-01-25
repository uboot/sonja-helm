import json
import re

from sonja import database
from sonja.config import logger


def _process_recipe(session: database.Session, recipe_data: dict, ecosystem: database.Ecosystem) -> database.Recipe:
    ecosystem_id = ecosystem.id
    name = recipe_data["name"]
    version = recipe_data["version"]
    user = recipe_data.get("user", None)
    channel = recipe_data.get("channel", None)

    recipe = session.query(database.Recipe).filter_by(
        ecosystem_id=ecosystem_id,
        name=name,
        version=version,
        user=user,
        channel=channel
    ).first()

    if not recipe:
        recipe = database.Recipe()
        recipe.ecosystem = ecosystem
        recipe.name = name
        recipe.version = version
        recipe.user = user
        recipe.channel = channel

    logger.debug("Process recipe '%s' ('%s/%s@%s/%s')", recipe.id, recipe.name, recipe.version,
                 recipe.user, recipe.channel)
    return recipe


def _process_recipe_revision(session: database.Session, recipe_data: dict, ecosystem: database.Ecosystem)\
        -> database.RecipeRevision:
    recipe = _process_recipe(session, recipe_data, ecosystem)
    if not recipe:
        return None

    m = re.match("[\\w\\+\\.-]+/[\\w\\+\\.-]+(?:@\\w+/\\w+)?(#(\\w+))?", recipe_data["id"])
    if m:
        revision = m.group(2) if m.group(2) else ""
    else:
        logger.error("Invalid recipe ID '%s'", recipe_data["id"])
        return None

    recipe_revision = session.query(database.RecipeRevision).filter_by(
        recipe_id=recipe.id,
        revision=revision
    ).first()

    if not recipe_revision:
        recipe_revision = database.RecipeRevision()
        recipe_revision.recipe = recipe
        recipe_revision.revision = revision

    logger.debug("Process recipe revision '%s' (revision: '%s')", recipe_revision.id, recipe_revision.revision)
    return recipe_revision


def _process_package(session: database.Session, package_data: dict, recipe_revision: database.RecipeRevision)\
        -> database.Package:
    package_id = package_data["id"]
    package = session.query(database.Package).filter_by(
        package_id=package_id,
        recipe_revision_id=recipe_revision.id
    ).first()

    if not package:
        package = database.Package()
        package.package_id = package_id
        package.recipe_revision = recipe_revision
        session.add(package)

    logger.debug("Process package '%s' (ID: '%s')", package.id, package.package_id)
    return package


def _trigger_builds_for_recipe(session: database.Session, recipe: database.Recipe):

    # get all failed builds which are waiting for this recipe
    builds = session.query(database.Build).filter(database.Build.status==database.BuildStatus.error).\
        filter(database.missing_recipe.columns['build_id']==database.Build.id).\
        filter(database.missing_recipe.columns['recipe_id']==recipe.id).\
        filter(database.Build.commit_id==database.Commit.id).\
        filter(database.Commit.status==database.CommitStatus.building).\
        all()

    # re-trigger these builds
    for build in builds:
        logger.info("Set status of build '%d' to 'new'", build.id)
        build.status = database.BuildStatus.new

    logger.debug("Trigger builds for recipe '%s' ('%s/%s@%s/%s')", recipe.id, recipe.name, recipe.version,
                 recipe.user, recipe.channel)
    return builds


def _trigger_builds_for_package(session: database.Session, package: database.Package):

    # Get all failed builds which are waiting a package of the same recipe revision. In these cases the package ID
    # should match exactly.
    same_recipe_revision = session.query(database.Build).filter(database.Build.status == database.BuildStatus.error).\
        filter(database.missing_package.columns['build_id'] == database.Build.id).\
        filter(database.missing_package.columns['package_id'] == package.id).\
        filter(database.Build.commit_id == database.Commit.id).\
        filter(database.Commit.status == database.CommitStatus.building).\
        all()

    # Get all failed builds which are waiting for a package of the same recipe but a different recipe revision. In these
    # cases a build is triggered regardless of the exact package ID (because the package ID might be computed
    # differently for a different recipe revision).
    different_recipe_revision = session.query(database.Build).\
        filter(database.Build.status == database.BuildStatus.error).\
        filter(database.missing_package.columns['build_id'] == database.Build.id).\
        filter(database.missing_package.columns['package_id'] == database.Package.id).\
        filter(database.Build.commit_id == database.Commit.id).\
        filter(database.Commit.status == database.CommitStatus.building).\
        filter(database.Package.recipe_revision_id == database.RecipeRevision.id).\
        filter(database.RecipeRevision.revision != package.recipe_revision.revision).\
        filter(database.RecipeRevision.recipe_id == package.recipe_revision.recipe.id).\
        all()

    # re-trigger these builds
    builds = same_recipe_revision + different_recipe_revision
    for build in builds:
        logger.info("Set status of build '%d' to 'new'", build.id)
        build.status = database.BuildStatus.new

    logger.debug("Trigger builds for package '%s' (ID: '%s')", package.id, package.package_id)
    return builds


def process_success(build_id, build_output) -> dict:
    result = dict()

    try:
        data = json.loads(build_output["create"])
    except KeyError:
        logger.error("Failed to obtain JSON output of the Conan create stage for build '%d'", build_id)
        return result

    with database.session_scope() as session:
        build = session.query(database.Build).filter_by(id=build_id).first()
        build.package = None
        build.missing_recipes = []
        build.missing_packages = []
        for recipe_compound in data["installed"]:
            recipe_data = recipe_compound["recipe"]
            if recipe_data["dependency"]:
                continue

            recipe_revision = _process_recipe_revision(session, recipe_data, build.profile.ecosystem)
            if not recipe_revision:
                continue

            for package_data in recipe_compound["packages"]:
                package = _process_package(session, package_data, recipe_revision)
                if not package:
                    continue
                build.package = package

                if _trigger_builds_for_package(session, package):
                    result['new_builds'] = True

            if _trigger_builds_for_recipe(session, recipe_revision.recipe):
                result['new_builds'] = True

        logger.info("Updated database for the successful build '%d'", build_id)
        return result


def process_failure(build_id, build_output) -> dict:
    result = dict()
    try:
        data = json.loads(build_output["create"])
    except KeyError:
        logger.info("Failed build contains no JSON output of the Conan create stage")
        return result

    if not data["error"]:
        logger.info("Conan create for failed build '%d' was successful, no missing dependencies", build_id)

    with database.session_scope() as session:
        build = session.query(database.Build).filter_by(id=build_id).first()
        build.package = None
        build.missing_recipes = []
        build.missing_packages = []
        for recipe_compound in data["installed"]:
            recipe_data = recipe_compound["recipe"]
            if not recipe_data["dependency"]:
                continue

            if recipe_data["error"] and recipe_data["error"]["type"] == "missing":
                recipe = _process_recipe(session, recipe_data, build.profile.ecosystem)
                build.missing_recipes.append(recipe)
                continue

            recipe_revision = _process_recipe_revision(session, recipe_data, build.profile.ecosystem)
            if not recipe_revision:
                continue

            for package_data in recipe_compound["packages"]:
                if package_data["error"] and package_data["error"]["type"] == "missing":
                    package = _process_package(session, package_data, recipe_revision)
                    build.missing_packages.append(package)

        logger.info("Updated database for the failed build '%d'", build_id)
        return result
