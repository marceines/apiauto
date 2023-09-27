"""
(c) Copyright Jalasoft. 2023

test_rest_client.py

"""
import json
import logging
import unittest
from unittest.mock import Mock, patch

import requests
from requests import Response

from utils.logger import get_logger
from utils.rest_client import RestClient

LOGGER = get_logger(__name__, logging.DEBUG)


class TestRestClient(unittest.TestCase):
    """
    Class to define methods for test RestClient
    """
    def setUp(self):
        self.session = requests.Session()

    def test_send_request_success(self):
        """
        Test to verify send_request method success
        """
        response_mock = Mock(spec=Response)
        response_mock.status_code = 200
        with patch.object(requests.Session, "get", return_value=response_mock) as mock_get:
            response = RestClient().send_request(
                    method_name="get",
                    session=self.session,
                    url="https://www.google.com"
            )
            mock_get.assert_called_once_with("https://www.google.com", headers='', data=None)
            self.assertEqual(response, response_mock)

    def test_send_request_post(self):
        """
        Test Send request
        """
        response_mock = Mock(spec=Response)
        response_mock.status_code = 200
        body = {
            "key": "value"
        }
        with patch.object(requests.Session, "post", return_value=response_mock) as mock_get:
            response = RestClient().send_request(
                method_name="post", session=self.session,
                url="https://www.google.com", data=json.dumps(body)
            )
            mock_get.assert_called_once_with(
                "https://www.google.com",
                headers='',
                data=json.dumps(body)
            )
            self.assertEqual(response, response_mock)

    def test_send_request_invalid_method(self):
        """
        Test send request invalid
        """
        with self.assertRaises(AssertionError):
            RestClient().send_request(
                method_name="put",
                session=self.session,
                url="https://www.google.com"
            )
