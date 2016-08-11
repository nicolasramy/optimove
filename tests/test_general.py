# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
import unittest
from urlparse import parse_qs

from optimove.client import Client
import responses

from constants import TOKEN


"""Callbacks"""


def login_callback(request):
    payload = parse_qs(request.body)
    headers = {'Content-Type': 'text/plain'}

    if payload['Username'][0] == 'username' and payload['Password'][0] == 'password':
        headers = {'Content-Type': 'application/json'}
        resp_body = TOKEN
        return 200, headers, json.dumps(resp_body)

    else:
        return 401, headers, 'Wrong user / password combination'


def get_last_data_update_callback(request):
    headers = {'Content-Type': 'text/plain'}

    if 'Authorization-Token' in request.headers:
        if request.headers['Authorization-Token'] == TOKEN:
            headers = {'Content-Type': 'application/json'}
            resp_body = {'Date': '2016-08-10'}
            return 200, headers, json.dumps(resp_body)

        else:
            return 403, headers, 'Unauthorized User'

    else:
        return 401, headers, 'Missing Authorization-Token'


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
        self.assertEqual(data, '2016-08-10')
