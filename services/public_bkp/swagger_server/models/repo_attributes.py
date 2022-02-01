# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from swagger_server.models.base_model_ import Model
from swagger_server.models.repo_attributes_exclude import RepoAttributesExclude  # noqa: F401,E501
from swagger_server.models.repo_attributes_options import RepoAttributesOptions  # noqa: F401,E501
from swagger_server import util


class RepoAttributes(Model):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """
    def __init__(self, name: str=None, url: str=None, path: str=None, exclude: List[RepoAttributesExclude]=None, options: List[RepoAttributesOptions]=None):  # noqa: E501
        """RepoAttributes - a model defined in Swagger

        :param name: The name of this RepoAttributes.  # noqa: E501
        :type name: str
        :param url: The url of this RepoAttributes.  # noqa: E501
        :type url: str
        :param path: The path of this RepoAttributes.  # noqa: E501
        :type path: str
        :param exclude: The exclude of this RepoAttributes.  # noqa: E501
        :type exclude: List[RepoAttributesExclude]
        :param options: The options of this RepoAttributes.  # noqa: E501
        :type options: List[RepoAttributesOptions]
        """
        self.swagger_types = {
            'name': str,
            'url': str,
            'path': str,
            'exclude': List[RepoAttributesExclude],
            'options': List[RepoAttributesOptions]
        }

        self.attribute_map = {
            'name': 'name',
            'url': 'url',
            'path': 'path',
            'exclude': 'exclude',
            'options': 'options'
        }
        self._name = name
        self._url = url
        self._path = path
        self._exclude = exclude
        self._options = options

    @classmethod
    def from_dict(cls, dikt) -> 'RepoAttributes':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The Repo_attributes of this RepoAttributes.  # noqa: E501
        :rtype: RepoAttributes
        """
        return util.deserialize_model(dikt, cls)

    @property
    def name(self) -> str:
        """Gets the name of this RepoAttributes.


        :return: The name of this RepoAttributes.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name: str):
        """Sets the name of this RepoAttributes.


        :param name: The name of this RepoAttributes.
        :type name: str
        """

        self._name = name

    @property
    def url(self) -> str:
        """Gets the url of this RepoAttributes.


        :return: The url of this RepoAttributes.
        :rtype: str
        """
        return self._url

    @url.setter
    def url(self, url: str):
        """Sets the url of this RepoAttributes.


        :param url: The url of this RepoAttributes.
        :type url: str
        """

        self._url = url

    @property
    def path(self) -> str:
        """Gets the path of this RepoAttributes.


        :return: The path of this RepoAttributes.
        :rtype: str
        """
        return self._path

    @path.setter
    def path(self, path: str):
        """Sets the path of this RepoAttributes.


        :param path: The path of this RepoAttributes.
        :type path: str
        """

        self._path = path

    @property
    def exclude(self) -> List[RepoAttributesExclude]:
        """Gets the exclude of this RepoAttributes.


        :return: The exclude of this RepoAttributes.
        :rtype: List[RepoAttributesExclude]
        """
        return self._exclude

    @exclude.setter
    def exclude(self, exclude: List[RepoAttributesExclude]):
        """Sets the exclude of this RepoAttributes.


        :param exclude: The exclude of this RepoAttributes.
        :type exclude: List[RepoAttributesExclude]
        """

        self._exclude = exclude

    @property
    def options(self) -> List[RepoAttributesOptions]:
        """Gets the options of this RepoAttributes.


        :return: The options of this RepoAttributes.
        :rtype: List[RepoAttributesOptions]
        """
        return self._options

    @options.setter
    def options(self, options: List[RepoAttributesOptions]):
        """Sets the options of this RepoAttributes.


        :param options: The options of this RepoAttributes.
        :type options: List[RepoAttributesOptions]
        """

        self._options = options