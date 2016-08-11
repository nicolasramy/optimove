# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
import unittest
from urlparse import urlparse, parse_qs, parse_qsl

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


def get_customer_attribute_list_callback(request):
    headers = {'Content-Type': 'text/plain'}

    if 'Authorization-Token' in request.headers:
        if request.headers['Authorization-Token'] == TOKEN:
            headers = {'Content-Type': 'application/json'}
            resp_body = [
                {'RealFieldName': 'Affiliate', 'Description': 'Acquisition affiliate'},
                {'RealFieldName': 'Age', 'Description': 'Customer age'},
                {'RealFieldName': 'Country', 'Description': 'Country of residence'}
            ]
            return 200, headers, json.dumps(resp_body)

        else:
            return 403, headers, 'Unauthorized User'

    else:
        return 401, headers, 'Missing Authorization-Token'


def get_lifecycle_stage_list_callback(request):
    headers = {'Content-Type': 'text/plain'}

    if 'Authorization-Token' in request.headers:
        if request.headers['Authorization-Token'] == TOKEN:
            headers = {'Content-Type': 'application/json'}
            resp_body = [
                {'StageID': 1, 'StageName': 'New'},
                {'StageID': 2, 'StageName': 'Active'},
                {'StageID': 3, 'StageName': 'FromChurn'},
                {'StageID': 4, 'StageName': 'Churn'}
            ]
            return 200, headers, json.dumps(resp_body)

        else:
            return 403, headers, 'Unauthorized User'

    else:
        return 401, headers, 'Missing Authorization-Token'


def get_microsegment_list_callback(request):
    headers = {'Content-Type': 'text/plain'}

    if 'Authorization-Token' in request.headers:
        if request.headers['Authorization-Token'] == TOKEN:
            headers = {'Content-Type': 'application/json'}
            resp_body = [
                {'MicrosegmentID': 1, 'MicrosegmentName': 'DWag1-Europe-Winner',
                 'LifecycleStageID': 1, 'FutureValue': 870.55, 'ChurnRate': 0.55},
                {'MicrosegmentID': 2, 'MicrosegmentName': 'DWag2-US-Loser',
                 'LifecycleStageID': 2, 'FutureValue': 1065.10, 'ChurnRate': 0.52},
                {'MicrosegmentID': 3, 'MicrosegmentName': 'DWag3-ROW-Winner',
                 'LifecycleStageID': 2, 'FutureValue': 1213.76, 'ChurnRate': 0.57}
            ]
            return 200, headers, json.dumps(resp_body)

        else:
            return 403, headers, 'Unauthorized User'

    else:
        return 401, headers, 'Missing Authorization-Token'


def get_microsegment_changers_callback(request):
    headers = {'Content-Type': 'text/plain'}

    if 'Authorization-Token' in request.headers:
        if request.headers['Authorization-Token'] == TOKEN:
            headers = {'Content-Type': 'application/json'}
            resp_body = [
                {'CustomerID': '231342', 'InitialMicrosegmentID': 4, 'FinalMicrosegmentID': 12},
                {'CustomerID': '231342', 'InitialMicrosegmentID': 3, 'FinalMicrosegmentID': 67}
            ]
            return 200, headers, json.dumps(resp_body)

        else:
            return 403, headers, 'Unauthorized User'

    else:
        return 401, headers, 'Missing Authorization-Token'


def get_microsegment_changers_with_attributes_callback(request):
    headers = {'Content-Type': 'text/plain'}

    if 'Authorization-Token' in request.headers:
        if request.headers['Authorization-Token'] == TOKEN:
            params = parse_qsl(urlparse(request.url).query)

            if params[0][1] == '2016-01-01':
                headers = {'Content-Type': 'application/json'}
                resp_body = [
                    {'CustomerID': '231342', 'InitialMicrosegmentID': 4, 'FinalMicrosegmentID': 12,
                     'CustomerAttributes': 'BuddyZZ,UK'},
                    {'CustomerID': '231342', 'InitialMicrosegmentID': 3, 'FinalMicrosegmentID': 67,
                     'CustomerAttributes': 'Player99,US'}
                ]
                return 200, headers, json.dumps(resp_body)

            else:
                return 404, headers, 'Not Found'

        else:
            return 403, headers, 'Unauthorized User'

    else:
        return 401, headers, 'Missing Authorization-Token'


class TestModel(unittest.TestCase):

    @responses.activate
    def test_get_customer_attribute_list(self):
        responses.add_callback(
            responses.POST,
            'https://api.optimove.net/v3.0/general/login',
            callback=login_callback,
            content_type='application/json'
        )

        responses.add_callback(
            responses.GET,
            'https://api.optimove.net/v3.0/model/GetCustomerAttributeList',
            callback=get_customer_attribute_list_callback,
            content_type='application/json'
        )

        client = Client('username', 'password')
        data = client.model.get_customer_attribute_list()
        self.assertEqual(data, {
            'Affiliate': 'Acquisition affiliate',
            'Age': 'Customer age',
            'Country': 'Country of residence',
        })

    @responses.activate
    def test_get_lifecycle_stage_list(self):
        responses.add_callback(
            responses.POST,
            'https://api.optimove.net/v3.0/general/login',
            callback=login_callback,
            content_type='application/json'
        )

        responses.add_callback(
            responses.GET,
            'https://api.optimove.net/v3.0/model/GetLifecycleStageList',
            callback=get_lifecycle_stage_list_callback,
            content_type='application/json'
        )

        client = Client('username', 'password')
        data = client.model.get_lifecycle_stage_list()
        self.assertEqual(data, {
            1: 'New',
            2: 'Active',
            3: 'FromChurn',
            4: 'Churn',
        })

    @responses.activate
    def test_get_microsegment_list(self):
        responses.add_callback(
            responses.POST,
            'https://api.optimove.net/v3.0/general/login',
            callback=login_callback,
            content_type='application/json'
        )

        responses.add_callback(
            responses.GET,
            'https://api.optimove.net/v3.0/model/GetMicrosegmentList',
            callback=get_microsegment_list_callback,
            content_type='application/json'
        )

        client = Client('username', 'password')
        data = client.model.get_microsegment_list()
        self.assertEqual(data, {
            1: {
                'name': 'DWag1-Europe-Winner',
                'stage_id': 1,
                'future_value': 870.55,
                'churn_rate': 0.55
            },
            2: {
                'name': 'DWag2-US-Loser',
                'stage_id': 2,
                'future_value': 1065.10,
                'churn_rate': 0.52
            },
            3: {
                'name': 'DWag3-ROW-Winner',
                'stage_id': 2,
                'future_value': 1213.76,
                'churn_rate': 0.57
            }
        })

    @responses.activate
    def test_get_microsegment_changers(self):
        responses.add_callback(
            responses.POST,
            'https://api.optimove.net/v3.0/general/login',
            callback=login_callback,
            content_type='application/json'
        )

        responses.add_callback(
            responses.GET,
            'https://api.optimove.net/v3.0/model/GetMicrosegmentChangers',
            callback=get_microsegment_changers_callback,
            content_type='application/json'
        )

        client = Client('username', 'password')
        data = client.model.get_microsegment_changers('2016-01-01', '2016-01-31')
        self.assertEqual(data, [
            {
                'customer_id': '231342',
                'initial': 4,
                'final': 12
            },
            {
                'customer_id': '231342',
                'initial': 3,
                'final': 67
            },
        ])

    @responses.activate
    def test_get_microsegment_changers_with_attributes(self):
        responses.add_callback(
            responses.POST,
            'https://api.optimove.net/v3.0/general/login',
            callback=login_callback,
            content_type='application/json'
        )

        responses.add_callback(
            responses.GET,
            'https://api.optimove.net/v3.0/model/GetMicrosegmentChangers',
            callback=get_microsegment_changers_with_attributes_callback,
            content_type='application/json'
        )

        client = Client('username', 'password')
        data = client.model.get_microsegment_changers('2016-01-01', '2016-01-31', ['Alias', 'Country'], ',')
        self.assertEqual(data, [
            {
                'customer_id': '231342',
                'initial': 4,
                'final': 12,
                'attributes': {
                    'Alias': 'BuddyZZ',
                    'Country': 'UK'
                }
            },
            {
                'customer_id': '231342',
                'initial': 3,
                'final': 67,
                'attributes': {
                    'Alias': 'Player99',
                    'Country': 'US'
                }
            },
        ])

    @responses.activate
    def test_get_microsegment_changers_with_wrong_delimiter(self):
        responses.add_callback(
            responses.POST,
            'https://api.optimove.net/v3.0/general/login',
            callback=login_callback,
            content_type='application/json'
        )

        responses.add_callback(
            responses.GET,
            'https://api.optimove.net/v3.0/model/GetMicrosegmentChangers',
            callback=get_microsegment_changers_with_attributes_callback,
            content_type='application/json'
        )

        client = Client('username', 'password')
        self.assertRaises(Exception, client.model.get_microsegment_changers,
                          '2016-01-01', '2016-01-31', ['Alias', 'Country'], '/')

    @responses.activate
    def test_get_microsegment_changers_with_wrong_dates(self):
        responses.add_callback(
            responses.POST,
            'https://api.optimove.net/v3.0/general/login',
            callback=login_callback,
            content_type='application/json'
        )

        responses.add_callback(
            responses.GET,
            'https://api.optimove.net/v3.0/model/GetMicrosegmentChangers',
            callback=get_microsegment_changers_with_attributes_callback,
            content_type='application/json'
        )

        client = Client('username', 'password')
        self.assertRaises(Exception, client.model.get_microsegment_changers,
                          '2016-01-01', None, ['Alias', 'Country'], ',')

    @responses.activate
    def test_get_microsegment_changers_with_unreasonable_dates(self):
        responses.add_callback(
            responses.POST,
            'https://api.optimove.net/v3.0/general/login',
            callback=login_callback,
            content_type='application/json'
        )

        responses.add_callback(
            responses.GET,
            'https://api.optimove.net/v3.0/model/GetMicrosegmentChangers',
            callback=get_microsegment_changers_with_attributes_callback,
            content_type='application/json'
        )

        client = Client('username', 'password')
        data = client.model.get_microsegment_changers('3016-01-01', '3016-01-31', ['Alias', 'Country'], ',')
        self.assertFalse(data)
