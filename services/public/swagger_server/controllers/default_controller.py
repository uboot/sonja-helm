import connexion
import base64
import six

from conanci import database
from conanci.ssh import decode, encode, generate_rsa_key

from flask import abort
from swagger_server.models.build import Build  # noqa: E501
from swagger_server.models.channel import Channel  # noqa: E501
from swagger_server.models.ecosystem import Ecosystem  # noqa: E501
from swagger_server.models.commit import Commit  # noqa: E501
from swagger_server.models.profile import Profile  # noqa: E501
from swagger_server.models.setting import Setting  # noqa: E501
from swagger_server.models.repo import Repo  # noqa: E501


build_status_table = {
    "new": database.BuildStatus.new,
    "active": database.BuildStatus.active,
    "error": database.BuildStatus.error,
    "stopping": database.BuildStatus.stopping,
    "stopped": database.BuildStatus.stopped,
    "success": database.BuildStatus.success
}


def ping():  # noqa: E501
    """ping the service

     # noqa: E501


    :rtype: None
    """
    return 'success'

def add_channel(body=None):  # noqa: E501
    """add a new channel

     # noqa: E501

    :param body: channel to add
    :type body: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        body = Channel.from_dict(connexion.request.get_json())  # noqa: E501
        with database.session_scope() as session:
            ecosystem = session.query(database.Ecosystem).filter_by(id=body.ecosystem).first()
            if not ecosystem:
                abort(400)
            channel = database.Channel()
            channel.name = body.name
            channel.ecosystem = ecosystem
            channel.branch = body.branch
            session.add(channel)
            session.commit()
            body.id = channel.id

    return body, 201


def add_ecosystem(body=None):  # noqa: E501
    """add a new ecosystem

     # noqa: E501

    :param body: ecosystem to add
    :type body: dict | bytes

    :rtype: Ecosystem
    """
    if connexion.request.is_json:
        body = Ecosystem.from_dict(connexion.request.get_json())  # noqa: E501
        ecosystem = database.Ecosystem()
        ecosystem.name = body.name
        ecosystem.user = body.user
        ecosystem.known_hosts = body.known_hosts
        private, public = generate_rsa_key()
        ecosystem.ssh_key = encode(private)
        ecosystem.public_ssh_key = encode(public)
        ecosystem.settings = body.settings
        with database.session_scope() as session:
            session.add(ecosystem)
            session.commit()
            body.id = ecosystem.id
            body.public_ssh_key = ecosystem.public_ssh_key

    return body, 201


def add_profile(body=None):  # noqa: E501
    """add a new profile

     # noqa: E501

    :param body: profile to add
    :type body: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        body = Profile.from_dict(connexion.request.get_json())  # noqa: E501
        with database.session_scope() as session:
            ecosystem = session.query(database.Ecosystem).filter_by(id=body.ecosystem).first()
            if not ecosystem:
                abort(400)
            profile = database.Profile()
            profile.name = body.name
            profile.ecosystem = ecosystem
            profile.container = body.container
            profile.settings = [database.Setting(s.key, s.value) for s in body.settings]
            session.add(profile)
            session.commit()
            body.id = profile.id

    return body, 201


def add_repo(body=None):  # noqa: E501
    """add a new repo

     # noqa: E501

    :param body: repo to add
    :type body: dict | bytes

    :rtype: Repo
    """
    if connexion.request.is_json:
        body = Repo.from_dict(connexion.request.get_json())  # noqa: E501
        with database.session_scope() as session:
            ecosystem = session.query(database.Ecosystem).filter_by(id=body.ecosystem).first()
            if not ecosystem:
                abort(400)
            repo = database.Repo()
            repo.path = body.path
            repo.url = body.url
            repo.ecosystem = ecosystem
            session.add(repo)
            session.commit()
            body.id = repo.id

    return body, 201


def clear_database():  # noqa: E501
    """remove all entries from the database

     # noqa: E501


    :rtype: None
    """
    database.clear_database()
    return 'success'


def delete_channel(channel_id):  # noqa: E501
    """delete a channel

     # noqa: E501

    :param channel_id: channel id to delete
    :type channel_id: int

    :rtype: None
    """
    with database.session_scope() as session:
        channel = session.query(database.Channel).filter_by(id=channel_id).first()
        if not channel:
            abort(404)
        session.delete(channel)
    return None


def delete_ecosystem(ecosystem_id):  # noqa: E501
    """delete an ecosystem

     # noqa: E501

    :param ecosystem_id: ecosystem id to delete
    :type ecosystem_id: int

    :rtype: None
    """
    with database.session_scope() as session:
        ecosystem = session.query(database.Ecosystem).filter_by(id=ecosystem_id).first()
        if not ecosystem:
            abort(404)
        session.delete(ecosystem)
    return None


def delete_profile(profile_id):  # noqa: E501
    """delete a profile

     # noqa: E501

    :param profile_id: profile id to delete
    :type profile_id: int

    :rtype: None
    """
    with database.session_scope() as session:
        profile = session.query(database.Profile).filter_by(id=profile_id).first()
        if not profile:
            abort(404)
        session.delete(profile)
    return None


def delete_repo(repo_id):  # noqa: E501
    """delete a repo

     # noqa: E501

    :param repo_id: repo id to delete
    :type repo_id: int

    :rtype: None
    """
    with database.session_scope() as session:
        repo = session.query(database.Repo).filter_by(id=repo_id).first()
        if not repo:
            abort(404)
        session.delete(repo)
    return None


def get_channels():  # noqa: E501
    """get all channels

     # noqa: E501


    :rtype: List[Channel]
    """
    with database.session_scope() as session:
        return [Channel(c.id, c.ecosystem.id, c.name, c.branch) for c in session.query(database.Channel).all()]


def get_ecosystems():  # noqa: E501
    """get all ecosystems

     # noqa: E501


    :rtype: List[Ecosystem]
    """
    with database.session_scope() as session:
        return [Ecosystem(e.id, e.name, e.user, e.settings, e.public_ssh_key, e.known_hosts)
                for e in session.query(database.Ecosystem).all()]


def get_profiles():  # noqa: E501
    """get all active profiles

     # noqa: E501


    :rtype: List[Profile]
    """
    with database.session_scope() as session:
        return [Profile(p.id, p.ecosystem.id, p.name, p.container, [Setting(s.key, s.value) for s in p.settings])
                for p in session.query(database.Profile).all()]


def get_repos():  # noqa: E501
    """get all current repos

     # noqa: E501


    :rtype: List[Repo]
    """
    with database.session_scope() as session:
        return [Repo(r.id, r.ecosystem.id, r.url, r.path) for r in session.query(database.Repo).all()]


def get_builds(build_status):  # noqa: E501
    """get builds

     # noqa: E501

    :param build_status: build status
    :type build_status: str

    :rtype: List[Build]
    """
    with database.session_scope() as session:
        try:
            status = build_status_table[build_status]
        except KeyError:
            abort(400)
        return [Build(b.id, b.status.name,
                      Commit(b.commit.id, b.commit.sha,
                             Repo(b.commit.repo.id, b.commit.repo.url, b.commit.repo.path)),
                      Profile(b.profile.id, b.profile.name, b.profile.container,
                              [Setting(s.key, s.value) for s in b.profile.settings])
                      )
                for b in session.query(database.Build).filter_by(status=status).all()]


def update_build(build_id, body=None):  # noqa: E501
    """update a build

     # noqa: E501

    :param build_id: id of the build to update
    :type build_id: int
    :param body: updated build data
    :type body: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        body = Build.from_dict(connexion.request.get_json())  # noqa: E501
    with database.session_scope() as session:
        build = session.query(database.Build).filter_by(id=build_id).first()
        if not build:
            abort(404)
        try:
            build.status = build_status_table[body.status]
        except KeyError:
            abort(400)

        commit = build.commit
        repo = commit.repo
        profile = build.profile
        return Build(build.id, build.status.name,
                     Commit(commit.id, commit.sha,
                            Repo(repo.id, repo.url, repo.path)),
                     Profile(profile.id, profile.name, profile.container,
                             [Setting(s.key, s.value) for s in profile.settings]))


def update_ecosystem(ecosystem_id, body=None):  # noqa: E501
    """update an ecosystem

     # noqa: E501

    :param ecosystem_id: id of the ecosystem to update
    :type ecosystem_id: int
    :param body: updated ecosystem data
    :type body: dict | bytes

    :rtype: Ecosystem
    """
    if connexion.request.is_json:
        body = Ecosystem.from_dict(connexion.request.get_json())  # noqa: E501
    with database.session_scope() as session:
        ecosystem = session.query(database.Ecosystem).filter_by(id=ecosystem_id).first()
        if not ecosystem:
            abort(404)

        ecosystem.name = body.name
        ecosystem.user = body.user
        ecosystem.known_hosts = body.known_hosts
        if body.ssh_key == '':
            private, public = generate_rsa_key()
        ecosystem.ssh_key = encode(private)
        ecosystem.public_ssh_key = encode(public)
        ecosystem.settings = body.settings

        body.id = ecosystem.id
        body.public_ssh_key = ecosystem.public_ssh_key
        return body


def populate_database():  # noqa: E501
    """Populate the database with sample data

     # noqa: E501


    :rtype: None
    """
    database.populate_database()
    return 'success'