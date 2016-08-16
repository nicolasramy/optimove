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
def get_customers_by_action_callback(request):
    params = parse_qs(urlparse(request.url).query)
    if params['RecipientGroupID'][0] == '1' and params['ActionID'][0] == '2' and params['Date'][0] == '2015-06-24':
        if 'CustomerAttributes' in params and 'CustomerAttributesDelimiter' in params:
            if params['CustomerAttributes'][0] == 'Alias;Country' and params['CustomerAttributesDelimiter'][0] == ',':
                resp_body = [
                    {'CustomerID': '231342', 'CustomerAttributes': 'BuddyZZ,UK'},
                    {'CustomerID': '943157', 'CustomerAttributes': 'Pax65,DE'}
                ]
            else:
                return 404, HEADERS['text'], 'Not Found'

        else:
            resp_body = [
                {'CustomerID': '231342'},
                {'CustomerID': '943157'}
            ]

        return 200, HEADERS['json'], json.dumps(resp_body)

    else:
        return 404, HEADERS['text'], 'Not Found'


@token_required
def get_customer_actions_by_target_group_callback(request):
    params = parse_qs(urlparse(request.url).query)
    if params['TargetGroupID'][0] == '2' and params['Date'][0] == '2015-12-24':
        if 'CustomerAttributes' in params and 'CustomerAttributesDelimiter' in params:
            if params['CustomerAttributes'][0] == 'Alias;Country' and params['CustomerAttributesDelimiter'][0] == ',':
                resp_body = [
                    {'CustomerID': 'A1342', 'ActionID': 49, 'ChannelID': 6, 'CustomerAttributes': 'BuddyZZ,UK'},
                    {'CustomerID': 'G4650', 'ActionID': 49, 'ChannelID': 6, 'CustomerAttributes': 'Mighty6,ES'}
                ]
            else:
                return 404, HEADERS['text'], 'Not Found'

        else:
            resp_body = [
                {'CustomerID': 'A1342', 'ActionID': 49, 'ChannelID': 6},
                {'CustomerID': 'G4650', 'ActionID': 49, 'ChannelID': 6}
            ]

        return 200, HEADERS['json'], json.dumps(resp_body)

    else:
        return 404, HEADERS['text'], 'Not Found'


@token_required
def get_customer_one_time_actions_by_date_callback(request):
    params = parse_qs(urlparse(request.url).query)
    if params['Date'][0] == '2015-06-24':
        if 'CustomerAttributes' in params and 'CustomerAttributesDelimiter' in params:
            if params['CustomerAttributes'][0] == 'Alias;Country' and params['CustomerAttributesDelimiter'][0] == ',':
                resp_body = [
                    {'CustomerID': '8D871', 'ActionID': 19, 'ChannelID': 3, 'CustomerAttributes': 'Yo999,UA'},
                    {'CustomerID': '8U76T', 'ActionID': 19, 'ChannelID': 3, 'CustomerAttributes': 'Neto2,TR'}
                ]
            else:
                return 404, HEADERS['text'], 'Not Found'

        else:
            resp_body = [
                {'CustomerID': '8D871', 'ActionID': 19, 'ChannelID': 3},
                {'CustomerID': '8U76T', 'ActionID': 19, 'ChannelID': 3}
            ]

        return 200, HEADERS['json'], json.dumps(resp_body)

    else:
        return 404, HEADERS['text'], 'Not Found'


@token_required
def get_target_group_changers_callback(request):
    params = parse_qs(urlparse(request.url).query)
    if params['StartDate'][0] == '2015-09-01' and params['EndDate'][0] == '2015-09-30':
        if 'CustomerAttributes' in params and 'CustomerAttributesDelimiter' in params:
            if params['CustomerAttributes'][0] == 'Alias;Country' and params['CustomerAttributesDelimiter'][0] == ',':
                resp_body = [
                    {'CustomerID': '231342', 'InitialTargetGroupID': 4, 'FinalTargetGroupID': 12,
                     'CustomerAttributes': 'BuddyZZ,UK'},
                    {'CustomerID': '931342', 'InitialTargetGroupID': -1, 'FinalTargetGroupID': 8,
                     'CustomerAttributes': 'Pax65,DE'}
                ]
            else:
                return 404, HEADERS['text'], 'Not Found'

        else:
            resp_body = [
                {'CustomerID': '231342', 'InitialTargetGroupID': 4, 'FinalTargetGroupID': 12},
                {'CustomerID': '931342', 'InitialTargetGroupID': -1, 'FinalTargetGroupID': 8}
            ]

        return 200, HEADERS['json'], json.dumps(resp_body)

    else:
        return 404, HEADERS['text'], 'Not Found'


@token_required
def get_customer_attribute_changers_callback(request):
    params = parse_qs(urlparse(request.url).query)
    if params['StartDate'][0] == '2015-01-30' and params['EndDate'][0] == '2015-01-31'and \
            params['ChangedCustomerAttribute'][0] == 'OptimailUnsubscribed':
        if 'CustomerAttributes' in params and 'CustomerAttributesDelimiter' in params:
            if params['CustomerAttributes'][0] == 'Alias;Country' and params['CustomerAttributesDelimiter'][0] == ',':
                resp_body = [
                    {'CustomerID': '231342', 'InitialCustomerAttribute': 'NULL',
                     'FinalCustomerAttribute': 'SuperBrand', 'CustomerAttributes': 'BuddyZZ,UK'},
                    {'CustomerID': '231343', 'InitialCustomerAttribute': 'SuperBrand',
                     'FinalCustomerAttribute': 'Super Brand, Mega Brand', 'CustomerAttributes': 'Pax65,DE'}
                ]
            else:
                return 404, HEADERS['text'], 'Not Found'

        else:
            resp_body = [
                {'CustomerID': '231342', 'InitialCustomerAttribute': 'NULL',
                 'FinalCustomerAttribute': 'SuperBrand'},
                {'CustomerID': '231343', 'InitialCustomerAttribute': 'SuperBrand',
                 'FinalCustomerAttribute': 'Super Brand, Mega Brand'}
            ]

        return 200, HEADERS['json'], json.dumps(resp_body)

    else:
        return 404, HEADERS['text'], 'Not Found'


@token_required
def get_customer_future_values_callback(request):
    params = parse_qs(urlparse(request.url).query)

    if 'LifecycleStageID' in params and 'CustomerAttribute' not in params and 'CustomerAttributeValue' not in params:
        if params['LifecycleStageID'][0] == '6':
            resp_body = [
                {'CustomerID': '631942', 'FutureValue': 342.65},
                {'CustomerID': '257938', 'FutureValue': 102.33}
            ]
            return 200, HEADERS['json'], json.dumps(resp_body)

        else:
            return 404, HEADERS['text'], 'Not Found'

    elif 'LifecycleStageID' not in params and 'CustomerAttribute' in params and 'CustomerAttributeValue' in params:
        if params['CustomerAttribute'][0] == 'Country' and params['CustomerAttributeValue'][0] == 'Australia':
            resp_body = [
                {'CustomerID': '631942', 'FutureValue': 342.65},
                {'CustomerID': '257938', 'FutureValue': 102.33}
            ]
            return 200, HEADERS['json'], json.dumps(resp_body)

        else:
            return 404, HEADERS['text'], 'Not Found'

    else:
        return 404, HEADERS['text'], 'Not Found'


"""Tests"""


class TestCustomers(unittest.TestCase):

    @responses.activate
    def test_get_customers_by_action(self):
        responses.add_callback(
            responses.POST,
            'https://api.optimove.net/v3.0/general/login',
            callback=login_callback,
            content_type='application/json'
        )

        responses.add_callback(
            responses.GET,
            'https://api.optimove.net/v3.0/customers/GetCustomersByAction',
            callback=get_customers_by_action_callback,
            content_type='application/json'
        )

        client = Client('username', 'password')
        data = client.customers.get_customers_by_action(1, 2, '2015-06-24')
        self.assertEqual(data, ['231342', '943157'])

    @responses.activate
    def test_get_customers_by_action_with_empty_date(self):
        responses.add_callback(
            responses.POST,
            'https://api.optimove.net/v3.0/general/login',
            callback=login_callback,
            content_type='application/json'
        )

        responses.add_callback(
            responses.GET,
            'https://api.optimove.net/v3.0/customers/GetCustomersByAction',
            callback=get_customers_by_action_callback,
            content_type='application/json'
        )

        client = Client('username', 'password')
        self.assertRaises(Exception, client.customers.get_customers_by_action, 1, 2, None)

    @responses.activate
    def test_get_customers_by_action_with_wrong_date(self):
        responses.add_callback(
            responses.POST,
            'https://api.optimove.net/v3.0/general/login',
            callback=login_callback,
            content_type='application/json'
        )

        responses.add_callback(
            responses.GET,
            'https://api.optimove.net/v3.0/customers/GetCustomersByAction',
            callback=get_customers_by_action_callback,
            content_type='application/json'
        )

        client = Client('username', 'password')
        data = client.customers.get_customers_by_action(1, 2, '3015-06-24')
        self.assertFalse(data)

    @responses.activate
    def test_get_customers_by_action_with_attributes(self):
        responses.add_callback(
            responses.POST,
            'https://api.optimove.net/v3.0/general/login',
            callback=login_callback,
            content_type='application/json'
        )

        responses.add_callback(
            responses.GET,
            'https://api.optimove.net/v3.0/customers/GetCustomersByAction',
            callback=get_customers_by_action_callback,
            content_type='application/json'
        )

        client = Client('username', 'password')
        data = client.customers.get_customers_by_action(1, 2, '2015-06-24', ['Alias', 'Country'], ',')
        self.assertEqual(data, [
            {
                'customer_id': '231342',
                'attributes': {
                    'Alias': 'BuddyZZ',
                    'Country': 'UK'
                }
            },
            {
                'customer_id': '943157',
                'attributes': {
                    'Alias': 'Pax65',
                    'Country': 'DE'
                }
            }
        ])

    @responses.activate
    def test_get_customers_by_action_with_wrong_delimiter(self):
        responses.add_callback(
            responses.POST,
            'https://api.optimove.net/v3.0/general/login',
            callback=login_callback,
            content_type='application/json'
        )

        responses.add_callback(
            responses.GET,
            'https://api.optimove.net/v3.0/customers/GetCustomersByAction',
            callback=get_customers_by_action_callback,
            content_type='application/json'
        )

        client = Client('username', 'password')
        self.assertRaises(Exception, client.customers.get_customers_by_action, 1, 2, '2015-06-24',
                          ['Alias', 'Country'], '/')

    @responses.activate
    def test_get_customer_actions_by_target_group(self):
        responses.add_callback(
            responses.POST,
            'https://api.optimove.net/v3.0/general/login',
            callback=login_callback,
            content_type='application/json'
        )

        responses.add_callback(
            responses.GET,
            'https://api.optimove.net/v3.0/customers/GetCustomerActionsByTargetGroup',
            callback=get_customer_actions_by_target_group_callback,
            content_type='application/json'
        )

        client = Client('username', 'password')
        data = client.customers.get_customer_actions_by_target_group(2, '2015-12-24')
        self.assertEqual(data, [
            {
                'customer_id': 'A1342',
                'action_id': 49,
                'channel_id': 6
            },
            {
                'customer_id': 'G4650',
                'action_id': 49,
                'channel_id': 6
            }
        ])

    @responses.activate
    def test_get_customer_actions_by_target_group_with_empty_date(self):
        responses.add_callback(
            responses.POST,
            'https://api.optimove.net/v3.0/general/login',
            callback=login_callback,
            content_type='application/json'
        )

        responses.add_callback(
            responses.GET,
            'https://api.optimove.net/v3.0/customers/GetCustomerActionsByTargetGroup',
            callback=get_customer_actions_by_target_group_callback,
            content_type='application/json'
        )

        client = Client('username', 'password')
        self.assertRaises(Exception, client.customers.get_customer_actions_by_target_group, 2, None)

    @responses.activate
    def test_get_customer_actions_by_target_group_with_wrong_date(self):
        responses.add_callback(
            responses.POST,
            'https://api.optimove.net/v3.0/general/login',
            callback=login_callback,
            content_type='application/json'
        )

        responses.add_callback(
            responses.GET,
            'https://api.optimove.net/v3.0/customers/GetCustomerActionsByTargetGroup',
            callback=get_customer_actions_by_target_group_callback,
            content_type='application/json'
        )

        client = Client('username', 'password')
        data = client.customers.get_customer_actions_by_target_group(2, '3015-12-24')
        self.assertFalse(data)

    @responses.activate
    def test_get_customer_actions_by_target_group_with_attributes(self):
        responses.add_callback(
            responses.POST,
            'https://api.optimove.net/v3.0/general/login',
            callback=login_callback,
            content_type='application/json'
        )

        responses.add_callback(
            responses.GET,
            'https://api.optimove.net/v3.0/customers/GetCustomerActionsByTargetGroup',
            callback=get_customer_actions_by_target_group_callback,
            content_type='application/json'
        )

        client = Client('username', 'password')
        data = client.customers.get_customer_actions_by_target_group(2, '2015-12-24', True, ['Alias', 'Country'], ',')
        self.assertEqual(data, [
            {
                'customer_id': 'A1342',
                'action_id': 49,
                'channel_id': 6,
                'attributes': {
                    'Alias': 'BuddyZZ',
                    'Country': 'UK'
                }
            },
            {
                'customer_id': 'G4650',
                'action_id': 49,
                'channel_id': 6,
                'attributes': {
                    'Alias': 'Mighty6',
                    'Country': 'ES'
                }
            }
        ])

    @responses.activate
    def test_get_customer_actions_by_target_group_with_wrong_delimiter(self):
        responses.add_callback(
            responses.POST,
            'https://api.optimove.net/v3.0/general/login',
            callback=login_callback,
            content_type='application/json'
        )

        responses.add_callback(
            responses.GET,
            'https://api.optimove.net/v3.0/customers/GetCustomerActionsByTargetGroup',
            callback=get_customer_actions_by_target_group_callback,
            content_type='application/json'
        )

        client = Client('username', 'password')
        self.assertRaises(Exception, client.customers.get_customer_actions_by_target_group, 2, '2015-12-24',
                          True, ['Alias', 'Country'], '/')

    @responses.activate
    def test_get_customer_one_time_actions_by_date(self):
        responses.add_callback(
            responses.POST,
            'https://api.optimove.net/v3.0/general/login',
            callback=login_callback,
            content_type='application/json'
        )

        responses.add_callback(
            responses.GET,
            'https://api.optimove.net/v3.0/customers/GetCustomerOneTimeActionsByDate',
            callback=get_customer_one_time_actions_by_date_callback,
            content_type='application/json'
        )

        client = Client('username', 'password')
        data = client.customers.get_customer_one_time_actions_by_date('2015-06-24')
        self.assertEqual(data, [
            {
                'customer_id': '8D871',
                'action_id': 19,
                'channel_id': 3
            },
            {
                'customer_id': '8U76T',
                'action_id': 19,
                'channel_id': 3
            }
        ])

    @responses.activate
    def test_get_customer_one_time_actions_by_date_with_empty_date(self):
        responses.add_callback(
            responses.POST,
            'https://api.optimove.net/v3.0/general/login',
            callback=login_callback,
            content_type='application/json'
        )

        responses.add_callback(
            responses.GET,
            'https://api.optimove.net/v3.0/customers/GetCustomerOneTimeActionsByDate',
            callback=get_customer_one_time_actions_by_date_callback,
            content_type='application/json'
        )

        client = Client('username', 'password')
        self.assertRaises(Exception, client.customers.get_customer_one_time_actions_by_date, None)

    @responses.activate
    def test_get_customer_one_time_actions_by_date_with_wrong_date(self):
        responses.add_callback(
            responses.POST,
            'https://api.optimove.net/v3.0/general/login',
            callback=login_callback,
            content_type='application/json'
        )

        responses.add_callback(
            responses.GET,
            'https://api.optimove.net/v3.0/customers/GetCustomerOneTimeActionsByDate',
            callback=get_customer_one_time_actions_by_date_callback,
            content_type='application/json'
        )

        client = Client('username', 'password')
        data = client.customers.get_customer_one_time_actions_by_date('3015-06-24')
        self.assertFalse(data)

    @responses.activate
    def test_get_customer_one_time_actions_by_date_with_attributes(self):
        responses.add_callback(
            responses.POST,
            'https://api.optimove.net/v3.0/general/login',
            callback=login_callback,
            content_type='application/json'
        )

        responses.add_callback(
            responses.GET,
            'https://api.optimove.net/v3.0/customers/GetCustomerOneTimeActionsByDate',
            callback=get_customer_one_time_actions_by_date_callback,
            content_type='application/json'
        )

        client = Client('username', 'password')
        data = client.customers.get_customer_one_time_actions_by_date('2015-06-24', True, ['Alias', 'Country'], ',')
        self.assertEqual(data, [
            {
                'customer_id': '8D871',
                'action_id': 19,
                'channel_id': 3,
                'attributes': {
                    'Alias': 'Yo999',
                    'Country': 'UA'
                }
            },
            {
                'customer_id': '8U76T',
                'action_id': 19,
                'channel_id': 3,
                'attributes': {
                    'Alias': 'Neto2',
                    'Country': 'TR'
                }
            }
        ])

    @responses.activate
    def test_get_customer_one_time_actions_by_date_with_wrong_delimiter(self):
        responses.add_callback(
            responses.POST,
            'https://api.optimove.net/v3.0/general/login',
            callback=login_callback,
            content_type='application/json'
        )

        responses.add_callback(
            responses.GET,
            'https://api.optimove.net/v3.0/customers/GetCustomerOneTimeActionsByDate',
            callback=get_customer_one_time_actions_by_date_callback,
            content_type='application/json'
        )

        client = Client('username', 'password')
        self.assertRaises(Exception, client.customers.get_customer_one_time_actions_by_date, '2015-06-24',
                          True, ['Alias', 'Country'], '/')

    @responses.activate
    def test_get_target_group_changers(self):
        responses.add_callback(
            responses.POST,
            'https://api.optimove.net/v3.0/general/login',
            callback=login_callback,
            content_type='application/json'
        )

        responses.add_callback(
            responses.GET,
            'https://api.optimove.net/v3.0/customers/GetTargetGroupChangers',
            callback=get_target_group_changers_callback,
            content_type='application/json'
        )

        client = Client('username', 'password')
        data = client.customers.get_target_group_changers('2015-09-01', '2015-09-30')
        self.assertEqual(data, [
            {
                'customer_id': '231342',
                'initial_target_group_id': 4,
                'final_target_group_id': 12
            },
            {
                'customer_id': '931342',
                'initial_target_group_id': -1,
                'final_target_group_id': 8
            }
        ])

    @responses.activate
    def test_get_target_group_changers_with_empty_date(self):
        responses.add_callback(
            responses.POST,
            'https://api.optimove.net/v3.0/general/login',
            callback=login_callback,
            content_type='application/json'
        )

        responses.add_callback(
            responses.GET,
            'https://api.optimove.net/v3.0/customers/GetTargetGroupChangers',
            callback=get_target_group_changers_callback,
            content_type='application/json'
        )

        client = Client('username', 'password')
        self.assertRaises(Exception, client.customers.get_target_group_changers, '2015-09-01', None)

    @responses.activate
    def test_get_target_group_changers_with_wrong_date(self):
        responses.add_callback(
            responses.POST,
            'https://api.optimove.net/v3.0/general/login',
            callback=login_callback,
            content_type='application/json'
        )

        responses.add_callback(
            responses.GET,
            'https://api.optimove.net/v3.0/customers/GetTargetGroupChangers',
            callback=get_target_group_changers_callback,
            content_type='application/json'
        )

        client = Client('username', 'password')
        data = client.customers.get_target_group_changers('3015-09-01', '3015-09-30')
        self.assertFalse(data)

    @responses.activate
    def test_get_target_group_changers_with_attributes(self):
        responses.add_callback(
            responses.POST,
            'https://api.optimove.net/v3.0/general/login',
            callback=login_callback,
            content_type='application/json'
        )

        responses.add_callback(
            responses.GET,
            'https://api.optimove.net/v3.0/customers/GetTargetGroupChangers',
            callback=get_target_group_changers_callback,
            content_type='application/json'
        )

        client = Client('username', 'password')
        data = client.customers.get_target_group_changers('2015-09-01', '2015-09-30', ['Alias', 'Country'], ',')
        self.assertEqual(data, [
            {
                'customer_id': '231342',
                'initial_target_group_id': 4,
                'final_target_group_id': 12,
                'attributes': {
                    'Alias': 'BuddyZZ',
                    'Country': 'UK'
                }
            },
            {
                'customer_id': '931342',
                'initial_target_group_id': -1,
                'final_target_group_id': 8,
                'attributes': {
                    'Alias': 'Pax65',
                    'Country': 'DE'
                }
            }
        ])

    @responses.activate
    def test_get_target_group_changers_with_wrong_delimiter(self):
        responses.add_callback(
            responses.POST,
            'https://api.optimove.net/v3.0/general/login',
            callback=login_callback,
            content_type='application/json'
        )

        responses.add_callback(
            responses.GET,
            'https://api.optimove.net/v3.0/customers/GetTargetGroupChangers',
            callback=get_target_group_changers_callback,
            content_type='application/json'
        )

        client = Client('username', 'password')
        self.assertRaises(Exception, client.customers.get_target_group_changers, '2015-09-01', '2015-09-30',
                          ['Alias', 'Country'], '/')

    @responses.activate
    def test_get_customer_attribute_changers(self):
        responses.add_callback(
            responses.POST,
            'https://api.optimove.net/v3.0/general/login',
            callback=login_callback,
            content_type='application/json'
        )

        responses.add_callback(
            responses.GET,
            'https://api.optimove.net/v3.0/customers/GetCustomerAttributeChangers',
            callback=get_customer_attribute_changers_callback,
            content_type='application/json'
        )

        client = Client('username', 'password')
        data = client.customers.get_customer_attribute_changers('2015-01-30', '2015-01-31', 'OptimailUnsubscribed')
        self.assertEqual(data, [
            {
                'customer_id': '231342',
                'initial_customer_attribute': None,
                'final_customer_attribute': 'SuperBrand'
            },
            {
                'customer_id': '231343',
                'initial_customer_attribute': 'SuperBrand',
                'final_customer_attribute': 'Super Brand, Mega Brand'
            }
        ])

    @responses.activate
    def test_get_customer_attribute_changers_with_empty_date(self):
        responses.add_callback(
            responses.POST,
            'https://api.optimove.net/v3.0/general/login',
            callback=login_callback,
            content_type='application/json'
        )

        responses.add_callback(
            responses.GET,
            'https://api.optimove.net/v3.0/customers/GetCustomerAttributeChangers',
            callback=get_customer_attribute_changers_callback,
            content_type='application/json'
        )

        client = Client('username', 'password')
        self.assertRaises(Exception, client.customers.get_customer_attribute_changers, '2015-01-30', None,
                          'OptimailUnsubscribed')

    @responses.activate
    def test_get_customer_attribute_changers_with_wrong_date(self):
        responses.add_callback(
            responses.POST,
            'https://api.optimove.net/v3.0/general/login',
            callback=login_callback,
            content_type='application/json'
        )

        responses.add_callback(
            responses.GET,
            'https://api.optimove.net/v3.0/customers/GetCustomerAttributeChangers',
            callback=get_customer_attribute_changers_callback,
            content_type='application/json'
        )

        client = Client('username', 'password')
        data = client.customers.get_customer_attribute_changers('3015-01-30', '3015-01-31', 'OptimailUnsubscribed')
        self.assertFalse(data)

    @responses.activate
    def test_get_customer_attribute_changers_with_attributes(self):
        responses.add_callback(
            responses.POST,
            'https://api.optimove.net/v3.0/general/login',
            callback=login_callback,
            content_type='application/json'
        )

        responses.add_callback(
            responses.GET,
            'https://api.optimove.net/v3.0/customers/GetCustomerAttributeChangers',
            callback=get_customer_attribute_changers_callback,
            content_type='application/json'
        )

        client = Client('username', 'password')
        data = client.customers.get_customer_attribute_changers('2015-01-30', '2015-01-31', 'OptimailUnsubscribed',
                                                                ['Alias', 'Country'], ',')
        self.assertEqual(data, [
            {
                'customer_id': '231342',
                'initial_customer_attribute': None,
                'final_customer_attribute': 'SuperBrand',
                'attributes': {
                    'Alias': 'BuddyZZ',
                    'Country': 'UK'
                }
            },
            {
                'customer_id': '231343',
                'initial_customer_attribute': 'SuperBrand',
                'final_customer_attribute': 'Super Brand, Mega Brand',
                'attributes': {
                    'Alias': 'Pax65',
                    'Country': 'DE'
                }
            }
        ])

    @responses.activate
    def test_get_customer_attribute_changers_with_wrong_delimiter(self):
        responses.add_callback(
            responses.POST,
            'https://api.optimove.net/v3.0/general/login',
            callback=login_callback,
            content_type='application/json'
        )

        responses.add_callback(
            responses.GET,
            'https://api.optimove.net/v3.0/customers/GetCustomerAttributeChangers',
            callback=get_customer_attribute_changers_callback,
            content_type='application/json'
        )

        client = Client('username', 'password')
        self.assertRaises(Exception, client.customers.get_customer_attribute_changers, '2015-01-30', '2015-01-31',
                          'OptimailUnsubscribed', ['Alias', 'Country'], '/')

    @responses.activate
    def test_get_customer_future_values(self):
        responses.add_callback(
            responses.POST,
            'https://api.optimove.net/v3.0/general/login',
            callback=login_callback,
            content_type='application/json'
        )

        responses.add_callback(
            responses.GET,
            'https://api.optimove.net/v3.0/customers/GetCustomerFutureValues',
            callback=get_customer_future_values_callback,
            content_type='application/json'
        )

        client = Client('username', 'password')
        data = client.customers.get_customer_future_values(attribute='Country', attribute_value='Australia')
        self.assertEqual(data, {
            '631942': 342.65,
            '257938': 102.33
        })

    @responses.activate
    def test_get_customer_future_values_alt(self):
        responses.add_callback(
            responses.POST,
            'https://api.optimove.net/v3.0/general/login',
            callback=login_callback,
            content_type='application/json'
        )

        responses.add_callback(
            responses.GET,
            'https://api.optimove.net/v3.0/customers/GetCustomerFutureValues',
            callback=get_customer_future_values_callback,
            content_type='application/json'
        )

        client = Client('username', 'password')
        data = client.customers.get_customer_future_values(6)
        self.assertEqual(data, {
            '631942': 342.65,
            '257938': 102.33
        })

    @responses.activate
    def test_get_customer_future_values_no_params(self):
        responses.add_callback(
            responses.POST,
            'https://api.optimove.net/v3.0/general/login',
            callback=login_callback,
            content_type='application/json'
        )

        responses.add_callback(
            responses.GET,
            'https://api.optimove.net/v3.0/customers/GetCustomerFutureValues',
            callback=get_customer_future_values_callback,
            content_type='application/json'
        )

        client = Client('username', 'password')
        self.assertRaises(Exception, client.customers.get_customer_future_values)

    @responses.activate
    def test_get_customer_future_values_wrong_params_combination(self):
        responses.add_callback(
            responses.POST,
            'https://api.optimove.net/v3.0/general/login',
            callback=login_callback,
            content_type='application/json'
        )

        responses.add_callback(
            responses.GET,
            'https://api.optimove.net/v3.0/customers/GetCustomerFutureValues',
            callback=get_customer_future_values_callback,
            content_type='application/json'
        )

        client = Client('username', 'password')
        self.assertRaises(Exception, client.customers.get_customer_future_values, 6, 'Country')

    @responses.activate
    def test_get_customer_future_values_wrong_customer_attribute(self):
        responses.add_callback(
            responses.POST,
            'https://api.optimove.net/v3.0/general/login',
            callback=login_callback,
            content_type='application/json'
        )

        responses.add_callback(
            responses.GET,
            'https://api.optimove.net/v3.0/customers/GetCustomerFutureValues',
            callback=get_customer_future_values_callback,
            content_type='application/json'
        )

        client = Client('username', 'password')
        data = client.customers.get_customer_future_values(attribute='Language', attribute_value='Australia')
        self.assertFalse(data)
