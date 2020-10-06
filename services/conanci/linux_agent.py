from conanci.config import app, db
from conanci import database

import sqlalchemy.exc
from conans.client.conan_api import ConanAPIV1

import os

data_dir = os.environ.get("VCS_DATA_DIR", "/data")
logger = app.app.logger

class Conan(object):
    def __init__(self):
        self.api = ConanAPIV1()

    def remotes(self):
        return self.api.remote_list()


def process_builds():
    # setup_database()
    # return

    build = database.Build.query.filter_by(status=database.BuildStatus.new)\
            .populate_existing()\
            .with_for_update(skip_locked=True, of=database.Build)\
            .first()
    
    if not build:
        return

    logger.info("set status of build '%d' to 'active'", build.id)
    build.status = database.BuildStatus.active
    db.session.commit()
    