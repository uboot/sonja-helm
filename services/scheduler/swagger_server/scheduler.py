from swagger_server.config import app, db
from swagger_server import database

logger = app.app.logger


def process_commits():
    logger.info("start processing commits")

    commits = database.Commit.query.filter_by(status=database.CommitStatus.new)
    profiles = database.Profile.query.all()
    for commit in commits:
        logger.info("process commit '%s' of repo '%s'", commit.sha[:7], commit.repo.url)
        for profile in profiles:
            logger.info("schedule build for '%s' with profile '%s'", commit.sha[:7], profile.name)
            build = database.Build()
            build.profile = profile
            build.commit = commit
            build.status = database.BuildStatus.new
            db.session.add(build)
        logger.info("set commit '%s' to 'building'", commit.sha[:7])
        commit.status = database.CommitStatus.building
        db.session.commit()

    logger.info("finish processing commits")
