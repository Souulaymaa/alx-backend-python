#!/usr/bin/env python3

"""
Unittests for utils.py.

Tests:
- access_nested_map
- get_json
- memoize
"""

import unittest
from parameterized import parameterized
from utils import access_nested_map, get_json, memoize
from unittest.mock import patch, Mock


class TestAccessNestedMap(unittest.TestCase):

    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a"), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2)
        ])
    # testing if the function returns the expected result.
    def test_access_nested_map(self, nested_map, path, expected):
        self.assertEqual(access_nested_map(nested_map, path), expected)

    @parameterized.expand([
        ({}, ("a"), KeyError),
        ({"a": 1}, ("a", "b"), KeyError)
    ])
    # testing if a KeyError is raised
    def test_access_nested_map_exception(self, nested_map, path, exception):

        # using assertRaises as a context manager
        with self.assertRaises(exception):
            access_nested_map(nested_map, path)


class TestGetJson(unittest.TestCase):

    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False})
    ])
    # Mocking HTTP calls
    def test_get_json(self, test_url, test_payload):
        with patch("utils.requests.get") as mock_obj:
            mock_response = Mock()
            mock_response.json.return_value = test_payload
            mock_obj.return_value = mock_response

            # call the function
            result = get_json(test_url)

            # Assert if output matches expected payload
            self.assertEqual(result, test_payload)

            # requests.get was called exactly once with the URL
            mock_obj.assert_called_once_with(test_url)


class TestMemoize(unittest.TestCase):

    def test_memoize(self):

        # given
        class TestClass:

            def a_method(self):
                return 42

            @memoize
            def a_property(self):
                return self.a_method()

        test_instance = TestClass()

        with patch.object(
            TestClass, 'a_method', return_value=42
        ) as mock_method:

            # Call the memoized property twice
            first_call = test_instance.a_property
            second_call = test_instance.a_property

            # check the return value
            self.assertEqual(first_call, 42)
            self.assertEqual(second_call, 42)

            # check if a_method is only called once
            mock_method.assert_called_once()
