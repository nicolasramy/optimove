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


def get_action_name_callback(request):
    headers = {'Content-Type': 'text/plain'}

    if 'Authorization-Token' in request.headers:
        if request.headers['Authorization-Token'] == TOKEN:
            headers = {'Content-Type': 'application/json'}
            resp_body = {'ActionName': '10% summer bonus'}
            return 200, headers, json.dumps(resp_body)

        else:
            return 403, headers, 'Unauthorized User'

    else:
        return 401, headers, 'Missing Authorization-Token'


def get_action_id_callback(request):
    headers = {'Content-Type': 'text/plain'}

    if 'Authorization-Token' in request.headers:
        if request.headers['Authorization-Token'] == TOKEN:
            headers = {'Content-Type': 'application/json'}
            resp_body = {'ActionID': 25}
            return 200, headers, json.dumps(resp_body)

        else:
            return 403, headers, 'Unauthorized User'

    else:
        return 401, headers, 'Missing Authorization-Token'


class TestActions(unittest.TestCase):

    @responses.activate
    def test_get_action_name(self):
        responses.add_callback(
            responses.POST,
            'https://api.optimove.net/v3.0/general/login',
            callback=login_callback,
            content_type='application/json'
        )

        responses.add_callback(
            responses.GET,
            'https://api.optimove.net/v3.0/actions/GetActionName',
            callback=get_action_name_callback,
            content_type='application/json'
        )

        client = Client('username', 'password')
        data = client.actions.get_action_name(104)
        self.assertEqual(data, '10% summer bonus')

    @responses.activate
    def test_get_action_id(self):
        responses.add_callback(
            responses.POST,
            'https://api.optimove.net/v3.0/general/login',
            callback=login_callback,
            content_type='application/json'
        )

        responses.add_callback(
            responses.GET,
            'https://api.optimove.net/v3.0/actions/GetActionID',
            callback=get_action_id_callback,
            content_type='application/json'
        )

        client = Client('username', 'password')
        data = client.actions.get_action_id('Free Shipping')
        self.assertEqual(data, 25)
