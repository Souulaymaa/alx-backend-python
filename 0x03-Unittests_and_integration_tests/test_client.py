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

    @patch('client.get_json')
    def test_public_repos(self, mock_getjson:Mock):
        '''
        Test that GithubOrgClient.public_repos returns the expected list of repos
        '''
        # fake payload (what get_json would normally return)
        test_payload = [
            {"name": "repo1"},
            {"name": "repo2"},
            {"name": "repo3"},
        ]
        mock_getjson.return_value = test_payload

        with patch('client.GithubOrgClient._public_repos_url', new_callable=PropertyMock) as mock_public_repos_url:
            mock_public_repos_url.return_value = "https://example-url.com"
            client = GithubOrgClient('example')
            result = client.public_repos()
            expected = ["repo1", "repo2", "repo3"]
            self.assertEqual(result, expected)

            