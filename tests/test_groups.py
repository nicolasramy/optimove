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


@token_required
def get_target_groups_by_date_callback(request):
    params = parse_qs(urlparse(request.url).query)
    if params['Date'][0] == '2015-05-31':
        resp_body = [
            {'TargetGroupID': 9},
            {'TargetGroupID': 24},
            {'TargetGroupID': 31},
            {'TargetGroupID': 36}
        ]
        return 200, HEADERS['json'], json.dumps(resp_body)
    else:
        return 404, HEADERS['text'], 'Not Found'


@token_required
def get_target_group_details_callback(request):
    resp_body = [
        {'TargetGroupID': 1, 'TargetGroupName': 'New UK', 'TargetGroupPriority': 1},
        {'TargetGroupID': 2, 'TargetGroupName': 'New DE', 'TargetGroupPriority': 2}
    ]
    return 200, HEADERS['json'], json.dumps(resp_body)


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
    def test_get_target_group_id_with_empty_name(self):
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

    @responses.activate
    def test_get_target_groups_by_date(self):
        responses.add_callback(
            responses.POST,
            'https://api.optimove.net/v3.0/general/login',
            callback=login_callback,
            content_type='application/json'
        )

        responses.add_callback(
            responses.GET,
            'https://api.optimove.net/v3.0/groups/GetTargetGroupsByDate',
            callback=get_target_groups_by_date_callback,
            content_type='application/json'
        )

        client = Client('username', 'password')
        data = client.groups.get_target_groups_by_date('2015-05-31')
        self.assertEqual(data, [9, 24, 31, 36])

    @responses.activate
    def test_get_target_groups_by_date_with_empty_date(self):
        responses.add_callback(
            responses.POST,
            'https://api.optimove.net/v3.0/general/login',
            callback=login_callback,
            content_type='application/json'
        )

        responses.add_callback(
            responses.GET,
            'https://api.optimove.net/v3.0/groups/GetTargetGroupsByDate',
            callback=get_target_groups_by_date_callback,
            content_type='application/json'
        )

        client = Client('username', 'password')
        self.assertRaises(Exception, client.groups.get_target_groups_by_date, None)

    @responses.activate
    def test_get_target_groups_by_date_with_wrong_date(self):
        responses.add_callback(
            responses.POST,
            'https://api.optimove.net/v3.0/general/login',
            callback=login_callback,
            content_type='application/json'
        )

        responses.add_callback(
            responses.GET,
            'https://api.optimove.net/v3.0/groups/GetTargetGroupsByDate',
            callback=get_target_groups_by_date_callback,
            content_type='application/json'
        )

        client = Client('username', 'password')
        data = client.groups.get_target_groups_by_date('3015-05-31')
        self.assertFalse(data)

    @responses.activate
    def test_get_target_group_details(self):
        responses.add_callback(
            responses.POST,
            'https://api.optimove.net/v3.0/general/login',
            callback=login_callback,
            content_type='application/json'
        )

        responses.add_callback(
            responses.GET,
            'https://api.optimove.net/v3.0/groups/GetTargetGroupDetails',
            callback=get_target_group_details_callback,
            content_type='application/json'
        )

        client = Client('username', 'password')
        data = client.groups.get_target_group_details()
        self.assertEqual(data, {
            1: {
                'name': 'New UK',
                'priority': 1
            },
            2: {
                'name': 'New DE',
                'priority': 2
            }
        })
