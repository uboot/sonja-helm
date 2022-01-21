from sonja import database, manager

import sonja.test.util as util
import os
import unittest

# Requires:
#
# 1. MySQL database
# docker run --rm -d --name mysql -p 3306:3306 -e MYSQL_DATABASE=sonja -e MYSQL_ROOT_PASSWORD=secret mysql:8.0.21


def _setup_build_output(create_file="create.json"):
    build_output = dict()
    create_output_file = os.path.join(os.path.dirname(__file__), "data/{0}".format(create_file))
    with open(create_output_file) as f:
        build_output["create"] = f.read()
    return build_output


class ManagerTest(unittest.TestCase):
    def setUp(self):
        database.reset_database()

    def test_process_success(self):
        build_output = _setup_build_output()

        with database.session_scope() as session:
            build = util.create_build(dict())
            session.add(build)
            session.commit()
            build_id = build.id

        manager.process_success(build_id, build_output)

        with database.session_scope() as session:
            build = session.query(database.Build).filter_by(id=build_id).first()
            self.assertIsNotNone(build.package)
            self.assertEqual("227220812d7ea3aa060187bae41abbc9911dfdfd", build.package.package_id)
            self.assertEqual("app", build.package.recipe_revision.recipe.name)
            self.assertEqual("2b44d2dde63878dd279ebe5d38c60dfaa97153fb", build.package.recipe_revision.revision)

    def test_process_success_existing_recipe(self):
        build_output = _setup_build_output()

        with database.session_scope() as session:
            parameters = dict()
            recipe = util.create_recipe(parameters)
            session.add(recipe)
            build = util.create_build(parameters)
            session.add(build)
            session.commit()
            build_id = build.id

        manager.process_success(build_id, build_output)

        with database.session_scope() as session:
            build = session.query(database.Build).filter_by(id=build_id).first()
            recipes = session.query(database.Recipe).all()
            recipe_revisions = session.query(database.RecipeRevision).all()
            self.assertEqual(1, len(recipes))
            self.assertEqual(1, len(recipe_revisions))
            self.assertEqual(1, build.package.recipe_revision.id)

    def test_process_success_existing_recipe_revision(self):
        build_output = _setup_build_output()

        with database.session_scope() as session:
            parameters = dict()
            recipe = util.create_recipe_revision(parameters)
            session.add(recipe)
            build = util.create_build(parameters)
            session.add(build)
            session.commit()
            build_id = build.id

        manager.process_success(build_id, build_output)

        with database.session_scope() as session:
            build = session.query(database.Build).filter_by(id=build_id).first()
            recipes = session.query(database.Recipe).all()
            recipe_revisions = session.query(database.RecipeRevision).all()
            self.assertEqual(1, len(recipes))
            self.assertEqual(1, len(recipe_revisions))
            self.assertEqual(1, build.package.recipe_revision.id)

    def test_process_success_existing_package(self):
        build_output = _setup_build_output()

        with database.session_scope() as session:
            parameters = dict()
            package = util.create_package(parameters)
            session.add(package)
            build = util.create_build(parameters)
            session.add(build)
            session.commit()
            build_id = build.id

        manager.process_success(build_id, build_output)

        with database.session_scope() as session:
            build = session.query(database.Build).filter_by(id=build_id).first()
            packages = session.query(database.Package).all()
            self.assertEqual(1, len(packages))
            self.assertEqual(1, build.package.id)

    def test_process_failure_missing_package(self):
        build_output = _setup_build_output("create_missing_package.json")

        with database.session_scope() as session:
            build = util.create_build(dict())
            session.add(build)
            session.commit()
            build_id = build.id

        manager.process_failure(build_id, build_output)

        with database.session_scope() as session:
            build = session.query(database.Build).filter_by(id=build_id).first()
            self.assertEqual(1, len(build.missing_packages))
            package = build.missing_packages[0]
            self.assertEqual("d057732059ea44a47760900cb5e4855d2bea8714", package.package_id)

            recipe_revision = package.recipe_revision
            self.assertIsNotNone(recipe_revision)
            self.assertEqual("f5c1ba6f1af634f500f7e0255619fecf4777965f", recipe_revision.revision)

            recipe = recipe_revision.recipe
            self.assertIsNotNone(recipe)
            self.assertEqual("base", recipe.name)
            self.assertEqual("1.2.3", recipe.version)
            self.assertEqual("mycompany", recipe.user)
            self.assertEqual("stable", recipe.channel)

    def test_process_failure_missing_package_twice(self):
        build_output_missing_package = _setup_build_output("create_missing_package.json")
        build_output_missing_recipe = _setup_build_output("create_missing_recipe.json")

        with database.session_scope() as session:
            build = util.create_build(dict())
            session.add(build)
            session.commit()
            build_id = build.id

        manager.process_failure(build_id, build_output_missing_package)
        manager.process_failure(build_id, build_output_missing_recipe)

        with database.session_scope() as session:
            build = session.query(database.Build).filter_by(id=build_id).first()
            self.assertEqual(0, len(build.missing_packages))
            self.assertEqual(1, len(build.missing_recipes))

    def test_process_failure_missing_recipe(self):
        build_output = _setup_build_output("create_missing_recipe.json")

        with database.session_scope() as session:
            build = util.create_build(dict())
            session.add(build)
            session.commit()
            build_id = build.id

        manager.process_failure(build_id, build_output)

        with database.session_scope() as session:
            build = session.query(database.Build).filter_by(id=build_id).first()
            self.assertEqual(1, len(build.missing_recipes))
            recipe = build.missing_recipes[0]
            self.assertEqual("base", recipe.name)
            self.assertEqual("1.2.3", recipe.version)
            self.assertEqual("mycompany", recipe.user)
            self.assertEqual("stable", recipe.channel)

    def test_process_success_remove_missing_items(self):
        build_output = _setup_build_output("create.json")

        with database.session_scope() as session:
            build = util.create_build(dict())
            build.missing_recipes = [util.create_recipe(dict())]
            build.missing_packages = [util.create_package(dict())]
            session.add(build)
            session.commit()
            build_id = build.id

        manager.process_success(build_id, build_output)

        with database.session_scope() as session:
            build = session.query(database.Build).filter_by(id=build_id).first()
            self.assertEqual(0, len(build.missing_recipes))
            self.assertEqual(0, len(build.missing_packages))
