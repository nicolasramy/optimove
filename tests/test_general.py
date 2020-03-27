# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

import json
import unittest

from optimove.client import Client
from optimove.general import General
from optimove.constants import DEFAULT_URL
import responses

from tests.constants import HEADERS, TOKEN
from tests.helpers import login_callback, token_required


"""Callbacks"""


@token_required
def get_last_data_update_callback(request):
    resp_body = {'Date': '2015-08-13'}
    return 200, HEADERS['json'], json.dumps(resp_body)


@token_required
def register_event_listener_callback(request):
    payload = json.loads(request.body)
    if payload['EventTypeID'] == 1 and payload['ListenerURL'] == 'http%3A%2F%2Fwww.exampleurl.com%2Feventlistener6':
        resp_body = {'ResponseCode': 200}
        return 200, HEADERS['json'], json.dumps(resp_body)
    else:
        return 404, HEADERS['text'], 'Not Found'


@token_required
def unregister_event_listener_callback(request):
    payload = json.loads(request.body)
    if payload['EventTypeID'] == 1:
        resp_body = {'ResponseCode': 200}
        return 200, HEADERS['json'], json.dumps(resp_body)
    else:
        return 404, HEADERS['text'], 'Not Found'


"""Tests"""


class TestGeneral(unittest.TestCase):

    @responses.activate
    def test_login_success(self):
        responses.add_callback(
            responses.POST,
            DEFAULT_URL + '/current/general/login',
            callback=login_callback,
            content_type='application/json'
        )

        client = Client('username', 'password')
        self.assertEqual(client.token, TOKEN)

    @responses.activate
    def test_login_fail(self):
        responses.add_callback(
            responses.POST,
            DEFAULT_URL + '/current/general/login',
            callback=login_callback,
            content_type='application/json'
        )

        client = Client()
        self.assertRaises(Exception, client.general.login, 'username', 'wrong_password')

    @responses.activate
    def test_login_no_credentials(self):
        responses.add_callback(
            responses.POST,
            DEFAULT_URL + '/current/general/login',
            callback=login_callback,
            content_type='application/json'
        )

        client = Client()
        self.assertRaises(Exception, client.general.login, None, None)

    @responses.activate
    def test_last_update_date(self):
        responses.add_callback(
            responses.POST,
            DEFAULT_URL + '/current/general/login',
            callback=login_callback,
            content_type='application/json'
        )

        responses.add_callback(
            responses.GET,
            DEFAULT_URL + '/current/general/GetLastDataUpdate',
            callback=get_last_data_update_callback,
            content_type='application/json'
        )

        client = Client('username', 'password')
        data = client.general.get_last_data_update()
        self.assertEqual(data, '2015-08-13')

    @responses.activate
    def test_register_event_listener(self):
        responses.add_callback(
            responses.POST,
            DEFAULT_URL + '/current/general/login',
            callback=login_callback,
            content_type='application/json'
        )

        responses.add_callback(
            responses.POST,
            DEFAULT_URL + '/current/general/RegisterEventListener',
            callback=register_event_listener_callback,
            content_type='application/json'
        )

        client = Client('username', 'password')
        data = client.general.register_event_listener(General.EVENT_TYPE_CAMPAIGN_PROCESSED,
                                                      'http://www.exampleurl.com/eventlistener6')
        self.assertTrue(data)

    @responses.activate
    def test_register_event_listener_with_empty_url(self):
        responses.add_callback(
            responses.POST,
            DEFAULT_URL + '/current/general/login',
            callback=login_callback,
            content_type='application/json'
        )

        responses.add_callback(
            responses.POST,
            DEFAULT_URL + '/current/general/RegisterEventListener',
            callback=register_event_listener_callback,
            content_type='application/json'
        )

        client = Client('username', 'password')
        self.assertRaises(Exception, client.general.register_event_listener,
                          General.EVENT_TYPE_CAMPAIGN_PROCESSED, None)

    @responses.activate
    def test_unregister_event_listener(self):
        responses.add_callback(
            responses.POST,
            DEFAULT_URL + '/current/general/login',
            callback=login_callback,
            content_type='application/json'
        )

        responses.add_callback(
            responses.POST,
            DEFAULT_URL + '/current/general/UnregisterEventListener',
            callback=unregister_event_listener_callback,
            content_type='application/json'
        )

        client = Client('username', 'password')
        data = client.general.unregister_event_listener(General.EVENT_TYPE_CAMPAIGN_PROCESSED)
        self.assertTrue(data)

    @responses.activate
    def test_unregister_event_listener_with_empty_event_type(self):
        responses.add_callback(
            responses.POST,
            DEFAULT_URL + '/current/general/login',
            callback=login_callback,
            content_type='application/json'
        )

        responses.add_callback(
            responses.POST,
            DEFAULT_URL + '/current/general/UnregisterEventListener',
            callback=unregister_event_listener_callback,
            content_type='application/json'
        )

        client = Client('username', 'password')
        self.assertRaises(Exception, client.general.unregister_event_listener, None)
