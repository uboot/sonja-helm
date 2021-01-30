# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from swagger_server.models.base_model_ import Model
from swagger_server.models.commit_attributes import CommitAttributes  # noqa: F401,E501
from swagger_server.models.commit_relationships import CommitRelationships  # noqa: F401,E501
from swagger_server import util


class Commit(Model):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """
    def __init__(self, id: str=None, type: str=None, attributes: CommitAttributes=None, relationships: CommitRelationships=None):  # noqa: E501
        """Commit - a model defined in Swagger

        :param id: The id of this Commit.  # noqa: E501
        :type id: str
        :param type: The type of this Commit.  # noqa: E501
        :type type: str
        :param attributes: The attributes of this Commit.  # noqa: E501
        :type attributes: CommitAttributes
        :param relationships: The relationships of this Commit.  # noqa: E501
        :type relationships: CommitRelationships
        """
        self.swagger_types = {
            'id': str,
            'type': str,
            'attributes': CommitAttributes,
            'relationships': CommitRelationships
        }

        self.attribute_map = {
            'id': 'id',
            'type': 'type',
            'attributes': 'attributes',
            'relationships': 'relationships'
        }
        self._id = id
        self._type = type
        self._attributes = attributes
        self._relationships = relationships

    @classmethod
    def from_dict(cls, dikt) -> 'Commit':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The Commit of this Commit.  # noqa: E501
        :rtype: Commit
        """
        return util.deserialize_model(dikt, cls)

    @property
    def id(self) -> str:
        """Gets the id of this Commit.


        :return: The id of this Commit.
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id: str):
        """Sets the id of this Commit.


        :param id: The id of this Commit.
        :type id: str
        """

        self._id = id

    @property
    def type(self) -> str:
        """Gets the type of this Commit.


        :return: The type of this Commit.
        :rtype: str
        """
        return self._type

    @type.setter
    def type(self, type: str):
        """Sets the type of this Commit.


        :param type: The type of this Commit.
        :type type: str
        """
        if type is None:
            raise ValueError("Invalid value for `type`, must not be `None`")  # noqa: E501

        self._type = type

    @property
    def attributes(self) -> CommitAttributes:
        """Gets the attributes of this Commit.


        :return: The attributes of this Commit.
        :rtype: CommitAttributes
        """
        return self._attributes

    @attributes.setter
    def attributes(self, attributes: CommitAttributes):
        """Sets the attributes of this Commit.


        :param attributes: The attributes of this Commit.
        :type attributes: CommitAttributes
        """

        self._attributes = attributes

    @property
    def relationships(self) -> CommitRelationships:
        """Gets the relationships of this Commit.


        :return: The relationships of this Commit.
        :rtype: CommitRelationships
        """
        return self._relationships

    @relationships.setter
    def relationships(self, relationships: CommitRelationships):
        """Sets the relationships of this Commit.


        :param relationships: The relationships of this Commit.
        :type relationships: CommitRelationships
        """

        self._relationships = relationships