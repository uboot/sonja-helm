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

    if recipe:
        return recipe

    recipe = database.Recipe()
    recipe.ecosystem = ecosystem
    recipe.name = name
    recipe.version = version
    recipe.user = user
    recipe.channel = channel

    return recipe


def _process_recipe_revision(session: database.Session, recipe_data: dict, ecosystem: database.Ecosystem)\
        -> database.RecipeRevision:
    recipe = _process_recipe(session, recipe_data, ecosystem)
    if not recipe:
        return None

    m = re.match("[\\w\\+\\.-]+/[\\w\\+\\.-]+(?:@\\w+/\\w+)?(#(\\w+))?", recipe_data["id"])
    if m:
        revision = m.group(2)
    else:
        logger.error("Invalid recipe ID '%s'", recipe_data["id"])
        return None

    recipe_revision = session.query(database.RecipeRevision).filter_by(
        recipe_id=recipe.id,
        revision=revision
    ).first()

    if recipe_revision:
        return recipe_revision

    recipe_revision = database.RecipeRevision()
    recipe_revision.recipe = recipe
    recipe_revision.revision = revision

    return recipe_revision


def _process_package(session: database.Session, package_data: dict, recipe_revision: database.RecipeRevision)\
        -> database.Package:
    package_id = package_data["id"]
    package = session.query(database.Package).filter_by(
        package_id=package_id,
        recipe_revision_id=recipe_revision.id
    ).first()

    if package:
        return package

    package = database.Package()
    package.package_id = package_id
    package.recipe_revision = recipe_revision
    session.add(package)

    return package


def process_success(build_id, build_output):
    try:
        data = json.loads(build_output["create"])
    except KeyError:
        logger.error("Failed to obtain JSON output of the Conan create stage for build '%d'", build_id)
        return

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

        logger.info("Updated database for the successful build '%d'", build_id)


def process_failure(build_id, build_output):
    try:
        data = json.loads(build_output["create"])
    except KeyError:
        logger.info("Failed build contains no JSON output of the Conan create stage")
        return

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
