# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from swagger_server.models.base_model_ import Model
from swagger_server import util


class RepoRelationshipsCommitsLinks(Model):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """
    def __init__(self, related: str=None):  # noqa: E501
        """RepoRelationshipsCommitsLinks - a model defined in Swagger

        :param related: The related of this RepoRelationshipsCommitsLinks.  # noqa: E501
        :type related: str
        """
        self.swagger_types = {
            'related': str
        }

        self.attribute_map = {
            'related': 'related'
        }
        self._related = related

    @classmethod
    def from_dict(cls, dikt) -> 'RepoRelationshipsCommitsLinks':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The Repo_relationships_commits_links of this RepoRelationshipsCommitsLinks.  # noqa: E501
        :rtype: RepoRelationshipsCommitsLinks
        """
        return util.deserialize_model(dikt, cls)

    @property
    def related(self) -> str:
        """Gets the related of this RepoRelationshipsCommitsLinks.


        :return: The related of this RepoRelationshipsCommitsLinks.
        :rtype: str
        """
        return self._related

    @related.setter
    def related(self, related: str):
        """Sets the related of this RepoRelationshipsCommitsLinks.


        :param related: The related of this RepoRelationshipsCommitsLinks.
        :type related: str
        """

        self._related = related
