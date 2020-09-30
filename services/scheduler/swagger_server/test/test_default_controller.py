# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.test import BaseTestCase


class TestDefaultController(BaseTestCase):
    """DefaultController integration test stubs"""

    def test_process_commits(self):
        """Test case for process_commits

        Process new commits
        """
        response = self.client.open(
            '/process-commits',
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_process_packages(self):
        """Test case for process_packages

        Process new packages
        """
        response = self.client.open(
            '/process-packages',
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
