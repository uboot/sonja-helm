# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from swagger_server.models.base_model_ import Model
from swagger_server.models.build_relationships_commit import BuildRelationshipsCommit  # noqa: F401,E501
from swagger_server.models.build_relationships_profile import BuildRelationshipsProfile  # noqa: F401,E501
from swagger_server.models.repo_relationships_ecosystem import RepoRelationshipsEcosystem  # noqa: F401,E501
from swagger_server import util


class BuildRelationships(Model):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """
    def __init__(self, ecosystem: RepoRelationshipsEcosystem=None, commit: BuildRelationshipsCommit=None, profile: BuildRelationshipsProfile=None):  # noqa: E501
        """BuildRelationships - a model defined in Swagger

        :param ecosystem: The ecosystem of this BuildRelationships.  # noqa: E501
        :type ecosystem: RepoRelationshipsEcosystem
        :param commit: The commit of this BuildRelationships.  # noqa: E501
        :type commit: BuildRelationshipsCommit
        :param profile: The profile of this BuildRelationships.  # noqa: E501
        :type profile: BuildRelationshipsProfile
        """
        self.swagger_types = {
            'ecosystem': RepoRelationshipsEcosystem,
            'commit': BuildRelationshipsCommit,
            'profile': BuildRelationshipsProfile
        }

        self.attribute_map = {
            'ecosystem': 'ecosystem',
            'commit': 'commit',
            'profile': 'profile'
        }
        self._ecosystem = ecosystem
        self._commit = commit
        self._profile = profile

    @classmethod
    def from_dict(cls, dikt) -> 'BuildRelationships':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The Build_relationships of this BuildRelationships.  # noqa: E501
        :rtype: BuildRelationships
        """
        return util.deserialize_model(dikt, cls)

    @property
    def ecosystem(self) -> RepoRelationshipsEcosystem:
        """Gets the ecosystem of this BuildRelationships.


        :return: The ecosystem of this BuildRelationships.
        :rtype: RepoRelationshipsEcosystem
        """
        return self._ecosystem

    @ecosystem.setter
    def ecosystem(self, ecosystem: RepoRelationshipsEcosystem):
        """Sets the ecosystem of this BuildRelationships.


        :param ecosystem: The ecosystem of this BuildRelationships.
        :type ecosystem: RepoRelationshipsEcosystem
        """

        self._ecosystem = ecosystem

    @property
    def commit(self) -> BuildRelationshipsCommit:
        """Gets the commit of this BuildRelationships.


        :return: The commit of this BuildRelationships.
        :rtype: BuildRelationshipsCommit
        """
        return self._commit

    @commit.setter
    def commit(self, commit: BuildRelationshipsCommit):
        """Sets the commit of this BuildRelationships.


        :param commit: The commit of this BuildRelationships.
        :type commit: BuildRelationshipsCommit
        """

        self._commit = commit

    @property
    def profile(self) -> BuildRelationshipsProfile:
        """Gets the profile of this BuildRelationships.


        :return: The profile of this BuildRelationships.
        :rtype: BuildRelationshipsProfile
        """
        return self._profile

    @profile.setter
    def profile(self, profile: BuildRelationshipsProfile):
        """Sets the profile of this BuildRelationships.


        :param profile: The profile of this BuildRelationships.
        :type profile: BuildRelationshipsProfile
        """

        self._profile = profile