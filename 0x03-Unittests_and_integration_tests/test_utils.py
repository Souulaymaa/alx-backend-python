#!/usr/bin/env python3

import unittest
from parameterized import parameterized
from utils import access_nested_map, get_json, memoize
from unittest.mock import patch, Mock

class TestAccessNestedMap(unittest.TestCase):

    @parameterized.expand([
        ({"a":1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a"), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2)
        ])
    #testing if the function returns the expected result.
    def test_access_nested_map(self, nested_map, path, expected):
        self.assertEqual(access_nested_map(nested_map, path), expected)
        
    @parameterized.expand([
        ({}, ("a"), KeyError ),
        ({"a": 1}, ("a", "b"), KeyError)
    ])
    # testing if a KeyError is raised
    def test_access_nested_map_exception(self,nested_map, path, exception):
        #using assertRaises as a context manager
        with self.assertRaises(exception):
            access_nested_map(nested_map, path)

class TestGetJson(unittest.TestCase):

    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False})
    ])

    #using patch as a decorator
    @patch("utils.requests.get")
    def test_get_json(self, url, mock_obj, payload):
        mock_response = Mock()
        mock_response.json.return_value = payload
        mock_obj.return_value = mock_response

        # call the function
        result = get_json(url)

        # Assert if output matches expected payload
        self.assertEqual(result, payload)

        # requests.get was called exactly once with the URL
        mock_obj.assert_called_once_with(url)
