# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
import unittest
from urlparse import parse_qs

from optimove.client import Client
import responses

from constants import HEADERS, TOKEN
from helpers import login_callback, token_required


"""Callbacks"""


@token_required
def get_last_data_update_callback(request):
    resp_body = {'Date': '2015-08-13'}
    return 200, HEADERS['json'], json.dumps(resp_body)


"""Tests"""


class TestGeneral(unittest.TestCase):

    @responses.activate
    def test_login_success(self):
        responses.add_callback(
            responses.POST,
            'https://api.optimove.net/v3.0/general/login',
            callback=login_callback,
            content_type='application/json'
        )

        client = Client('username', 'password')
        self.assertEqual(client.token, TOKEN)

    @responses.activate
    def test_login_fail(self):
        responses.add_callback(
            responses.POST,
            'https://api.optimove.net/v3.0/general/login',
            callback=login_callback,
            content_type='application/json'
        )

        client = Client()
        self.assertRaises(Exception, client.general.login, 'username', 'wrong_password')

    @responses.activate
    def test_login_no_credentials(self):
        responses.add_callback(
            responses.POST,
            'https://api.optimove.net/v3.0/general/login',
            callback=login_callback,
            content_type='application/json'
        )

        client = Client()
        self.assertRaises(Exception, client.general.login, None, None)

    @responses.activate
    def test_last_update_date(self):
        responses.add_callback(
            responses.POST,
            'https://api.optimove.net/v3.0/general/login',
            callback=login_callback,
            content_type='application/json'
        )

        responses.add_callback(
            responses.GET,
            'https://api.optimove.net/v3.0/general/GetLastDataUpdate',
            callback=get_last_data_update_callback,
            content_type='application/json'
        )

        client = Client('username', 'password')
        data = client.general.get_last_data_update()
        self.assertEqual(data, '2015-08-13')
