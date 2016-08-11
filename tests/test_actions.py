# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
import unittest
from urlparse import parse_qs, parse_qsl, urlparse

from optimove.client import Client
import responses

from constants import HEADERS, TOKEN
from helpers import login_callback, token_required


"""Callbacks"""


@token_required
def get_action_name_callback(request):
    params = parse_qsl(urlparse(request.url).query)
    if params[0][1] == '104':
        resp_body = {'ActionName': '10% summer bonus'}
        return 200, HEADERS['json'], json.dumps(resp_body)
    else:
        return 404, HEADERS['text'], 'Not Found'


@token_required
def get_action_id_callback(request):
    params = parse_qsl(urlparse(request.url).query)
    if params[0][1] == 'Free Shipping':
        resp_body = {'ActionID': 25}
        return 200, HEADERS['json'], json.dumps(resp_body)
    else:
        return 404, HEADERS['text'], 'Not Found'


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
    def test_get_action_name_with_wrong_action_id(self):
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
        self.assertRaises(Exception, client.actions.get_action_name, None)

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

    @responses.activate
    def test_get_action_id_with_wrong_action_name(self):
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
        self.assertRaises(Exception, client.actions.get_action_id, None)

    @responses.activate
    def test_get_all_actions(self):
        pass
