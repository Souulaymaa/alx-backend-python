#!/usr/bin/env python3

"""
Unittests for client.py.

Tests:
- Github0rgClient
"""

import unittest
from client import GithubOrgClient
from unittest.mock import patch, Mock, PropertyMock
from parameterized import parameterized

class TestGithubOrgClient(unittest.TestCase):
    '''
    Class to test the method in client.py
    '''
    @parameterized.expand([
        ('google',),
        ('abc',)
    ])
    @patch("client.get_json")
    def test_org(self, orgname, mock_getjson:Mock):
        '''
        Test that GithubOrgClient.org returns the correct value
        '''
        expected = {'login' : orgname}
        mock_getjson.return_value = expected
        client = GithubOrgClient(orgname)
        result = client.org
        self.assertEqual(result, expected)
        mock_getjson.assert_called_once_with(
            f"https://api.github.com/orgs/{orgname}"
        )


    def test_public_repos_url(self):
        '''
        Test if _public_repos_url returns expected URL
        '''
        with patch('client.GithubOrgClient.org', new_callable=PropertyMock) as mock_org:
            mock_org.return_value = {"repos_url": "https://api.github.com/orgs/example/repos"}
            client = GithubOrgClient('example')
            self.assertEqual(client._public_repos_url, "https://api.github.com/orgs/example/repos")

