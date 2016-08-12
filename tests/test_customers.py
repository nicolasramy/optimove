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
