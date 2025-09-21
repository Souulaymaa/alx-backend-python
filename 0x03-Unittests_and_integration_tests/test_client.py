#!/usr/bin/env python3

"""
Unittests for client.py.

Tests:
- Github0rgClient
"""

import unittest
from client import GithubOrgClient
from unittest.mock import patch, Mock, PropertyMock
from parameterized import parameterized, parameterized_class
from fixtures import TEST_PAYLOAD


class TestGithubOrgClient(unittest.TestCase):
    '''
    Class to test the method in client.py
    '''
    @parameterized.expand([
        ('google',),
        ('abc',)
    ])
    @patch("client.get_json")
    def test_org(self, orgname, mock_getjson: Mock):
        '''
        Test that GithubOrgClient.org returns the correct value
        '''
        expected = {'login': orgname}
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
        with patch(
            'client.GithubOrgClient.org', new_callable=PropertyMock
        ) as mock_org:
            mock_org.return_value = {
                "repos_url":
                    "https://api.github.com/orgs/example/repos"
            }
            client = GithubOrgClient('example')
            expected_url = "https://api.github.com/orgs/example/repos"
            self.assertEqual(client._public_repos_url, expected_url)

    @patch('client.get_json')
    def test_public_repos(self, mock_getjson: Mock):
        '''
        Test that GithubOrgClient.public_repos
        returns the expected list of repos
        '''
        # fake payload (what get_json would normally return)
        test_payload = [
            {"name": "repo1"},
            {"name": "repo2"},
            {"name": "repo3"},
        ]
        mock_getjson.return_value = test_payload

        with patch(
            'client.GithubOrgClient._public_repos_url',
            new_callable=PropertyMock
        ) as mock_public_repos_url:
            mock_public_repos_url.return_value = "https://example-url.com"
            client = GithubOrgClient('example')
            result = client.public_repos()
            expected = ["repo1", "repo2", "repo3"]
            self.assertEqual(result, expected)
            # testing if only called once
            mock_getjson.assert_called_once_with("https://example-url.com")
            mock_public_repos_url.assert_called_once()

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),
    ])
    def test_has_license(self, repo, license_key, expected):
        '''
        Test if GithubOrgClient.has_license returns the
        expected value
        '''
        result = GithubOrgClient.has_license(repo, license_key)
        self.assertEqual(result, expected)


class MockResponse:
    '''Mocked response object for requests.get'''

    def __init__(self, json_data):
        self._json_data = json_data

    def json(self):
        '''Return JSON payload'''
        return self._json_data
    

@parameterized_class([
     {
        "org_payload": TEST_PAYLOAD[0][0],
        "repos_payload": TEST_PAYLOAD[0][1],
        "expected_repos": TEST_PAYLOAD[0][2],
        "apache2_repos": TEST_PAYLOAD[0][3],
    }
])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    '''Integration Tests'''
    @classmethod
    def setUpClass(cls):
        '''Start patcher for requests.get'''
        cls.get_patcher = patch('requests.get')
        cls.mock_get = cls.get_patcher.start()

        def side_effect(url):
            if url.endswith("/orgs/google"):
                return MockResponse(cls.org_payload)
            elif url.endswith("/repos"):
                return MockResponse(cls.repos_payload)
            return None
        
        cls.mock_get.side_effect = side_effect

    @classmethod
    def tearDownClass(cls):
        '''Stop patcher for requests.get'''
        cls.get_patcher.stop()

    def test_public_repos(self):
        '''Test if public_repos returns expected repos'''
        client = GithubOrgClient('google')
        self.assertEqual(client.public_repos(), self.expected_repos)

    def test_public_repos_with_license(self):
        '''Test public_repos filters repos by license'''
        client = GithubOrgClient('google')
        self.assertEqual(client.public_repos(license="apache-2.0"), self.apache2_repos)



            