# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
import unittest
from urlparse import parse_qs, urlparse

from optimove.client import Client
import responses

from constants import HEADERS, TOKEN
from helpers import login_callback, token_required


"""Callbacks"""


@token_required
def get_target_group_name_callback(request):
    params = parse_qs(urlparse(request.url).query)
    if params['TargetGroupID'][0] == '42':
        resp_body = {'TargetGroupName': 'Ireland VIPs Played Last 30 Days'}
        return 200, HEADERS['json'], json.dumps(resp_body)
    else:
        return 404, HEADERS['text'], 'Not Found'


@token_required
def get_target_group_id_callback(request):
    params = parse_qs(urlparse(request.url).query)
    if params['TargetGroupName'][0] == 'UK 20VIPs':
        resp_body = {'TargetGroupID': 26}
        return 200, HEADERS['json'], json.dumps(resp_body)
    else:
        return 404, HEADERS['text'], 'Not Found'


"""Tests"""


class TestGroups(unittest.TestCase):

    @responses.activate
    def test_get_target_group_name(self):
        responses.add_callback(
            responses.POST,
            'https://api.optimove.net/v3.0/general/login',
            callback=login_callback,
            content_type='application/json'
        )

        responses.add_callback(
            responses.GET,
            'https://api.optimove.net/v3.0/groups/GetTargetGroupName',
            callback=get_target_group_name_callback,
            content_type='application/json'
        )

        client = Client('username', 'password')
        data = client.groups.get_target_group_name(42)
        self.assertEqual(data, 'Ireland VIPs Played Last 30 Days')

    @responses.activate
    def test_get_target_group_name_with_empty_target_group_id(self):
        responses.add_callback(
            responses.POST,
            'https://api.optimove.net/v3.0/general/login',
            callback=login_callback,
            content_type='application/json'
        )

        responses.add_callback(
            responses.GET,
            'https://api.optimove.net/v3.0/groups/GetTargetGroupName',
            callback=get_target_group_name_callback,
            content_type='application/json'
        )

        client = Client('username', 'password')
        self.assertRaises(Exception, client.groups.get_target_group_name, None)

    @responses.activate
    def test_get_target_group_name_with_wrong_name(self):
        responses.add_callback(
            responses.POST,
            'https://api.optimove.net/v3.0/general/login',
            callback=login_callback,
            content_type='application/json'
        )

        responses.add_callback(
            responses.GET,
            'https://api.optimove.net/v3.0/groups/GetTargetGroupName',
            callback=get_target_group_name_callback,
            content_type='application/json'
        )

        client = Client('username', 'password')
        data = client.groups.get_target_group_name(24)
        self.assertFalse(data)

    @responses.activate
    def test_get_target_group_id(self):
        responses.add_callback(
            responses.POST,
            'https://api.optimove.net/v3.0/general/login',
            callback=login_callback,
            content_type='application/json'
        )

        responses.add_callback(
            responses.GET,
            'https://api.optimove.net/v3.0/groups/GetTargetGroupID',
            callback=get_target_group_id_callback,
            content_type='application/json'
        )

        client = Client('username', 'password')
        data = client.groups.get_target_group_id('UK 20VIPs')
        self.assertEqual(data, 26)

    @responses.activate
    def test_get_target_group_id_with_empty_target_group_name(self):
        responses.add_callback(
            responses.POST,
            'https://api.optimove.net/v3.0/general/login',
            callback=login_callback,
            content_type='application/json'
        )

        responses.add_callback(
            responses.GET,
            'https://api.optimove.net/v3.0/groups/GetTargetGroupID',
            callback=get_target_group_id_callback,
            content_type='application/json'
        )

        client = Client('username', 'password')
        self.assertRaises(Exception, client.groups.get_target_group_id, None)

    @responses.activate
    def test_get_target_group_id_with_wrong_name(self):
        responses.add_callback(
            responses.POST,
            'https://api.optimove.net/v3.0/general/login',
            callback=login_callback,
            content_type='application/json'
        )

        responses.add_callback(
            responses.GET,
            'https://api.optimove.net/v3.0/groups/GetTargetGroupID',
            callback=get_target_group_id_callback,
            content_type='application/json'
        )

        client = Client('username', 'password')
        data = client.groups.get_target_group_id('UK 25VIPs')
        self.assertFalse(data)
