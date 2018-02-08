# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
import unittest
from urlparse import parse_qs, urlparse

from optimove.client import Client
from optimove.constants import DEFAULT_URL
import responses

from constants import HEADERS
from helpers import login_callback, token_required


"""Callbacks"""


@token_required
def get_value_segment_name_callback(request):
    params = parse_qs(urlparse(request.url).query)

    if params['ValueSegmentID'][0] == '1':
        resp_body = {'ValueSegmentName': 'Diamond'}
        return 200, HEADERS['json'], json.dumps(resp_body)

    else:
        return 404, HEADERS['text'], 'Not Found'


@token_required
def get_value_segment_id_callback(request):
    params = parse_qs(urlparse(request.url).query)

    if params['ValueSegmentName'][0] == 'Diamond':
        resp_body = {'ValueSegmentID': 1}
        return 200, HEADERS['json'], json.dumps(resp_body)

    else:
        return 404, HEADERS['text'], 'Not Found'


@token_required
def get_value_segments_callback(request):
    resp_body = [
        {'ValueSegmentName': 'Diamond', 'ValueSegmentID': 1},
        {'ValueSegmentName': 'Gold', 'ValueSegmentID': 2},
        {'ValueSegmentName': 'Silver', 'ValueSegmentID': 3},
        {'ValueSegmentName': 'Bronze', 'ValueSegmentID': 4}
    ]
    return 200, HEADERS['json'], json.dumps(resp_body)


@token_required
def get_customers_by_value_segment_callback(request):
    params = parse_qs(urlparse(request.url).query)

    if params['ValueSegmentID'][0] == '3' and params['Date'][0] == '2015-05-10':
        if 'CustomerAttributes' in params and 'CustomerAttributesDelimiter' in params:
            if params['CustomerAttributes'][0] == 'Alias;Country' and params['CustomerAttributesDelimiter'][0] == ',':
                resp_body = [
                    {'CustomerID': 'AC7615', 'CustomerAttributes': ['Robin777', 'ES']},
                    {'CustomerID': 'FP8721', 'CustomerAttributes': ['JollyPop', 'UK']}
                ]

            else:
                return 404, HEADERS['text'], 'Not Found'

        else:
            resp_body = [
                {'CustomerID': 'AC7615'},
                {'CustomerID': 'FP8721'}
            ]

        return 200, HEADERS['json'], json.dumps(resp_body)

    else:
        return 404, HEADERS['text'], 'Not Found'


@token_required
def get_value_segment_changers_callback(request):
    params = parse_qs(urlparse(request.url).query)

    if params['StartDate'][0] == '2015-09-01' and params['EndDate'][0] == '2015-09-30':
        if 'CustomerAttributes' in params and 'CustomerAttributesDelimiter' in params:
            if params['CustomerAttributes'][0] == 'Alias;Country' and params['CustomerAttributesDelimiter'][0] == ',':
                resp_body = [
                    {'CustomerID': '231342', 'InitialValueSegmentID': 2, 'FinalValueSegmentID': 3,
                     'CustomerAttributes': ['BuddyZZ', 'UK']},
                    {'CustomerID': '931342', 'InitialValueSegmentID': 1, 'FinalValueSegmentID': 2,
                     'CustomerAttributes': ['Pax65', 'DE']}
                ]

            else:
                return 404, HEADERS['text'], 'Not Found'

        else:
            resp_body = [
                {'CustomerID': '231342', 'InitialValueSegmentID': 2, 'FinalValueSegmentID': 3},
                {'CustomerID': '931342', 'InitialValueSegmentID': 1, 'FinalValueSegmentID': 2}
            ]

        return 200, HEADERS['json'], json.dumps(resp_body)

    else:
        return 404, HEADERS['text'], 'Not Found'


"""Tests"""


class TestSegments(unittest.TestCase):

    @responses.activate
    def test_get_value_segment_name(self):
        responses.add_callback(
            responses.POST,
            DEFAULT_URL + '/general/login',
            callback=login_callback,
            content_type='application/json'
        )

        responses.add_callback(
            responses.GET,
            DEFAULT_URL + '/segments/GetValueSegmentName',
            callback=get_value_segment_name_callback,
            content_type='application/json'
        )

        client = Client('username', 'password')
        data = client.segments.get_value_segment_name(1)
        self.assertEqual(data, 'Diamond')

    @responses.activate
    def test_get_value_segment_name_with_empty_segment_id(self):
        responses.add_callback(
            responses.POST,
            DEFAULT_URL + '/general/login',
            callback=login_callback,
            content_type='application/json'
        )

        responses.add_callback(
            responses.GET,
            DEFAULT_URL + '/segments/GetValueSegmentName',
            callback=get_value_segment_name_callback,
            content_type='application/json'
        )

        client = Client('username', 'password')
        self.assertRaises(Exception, client.segments.get_value_segment_name, None)

    @responses.activate
    def test_get_value_segment_name_with_wrong_segment_id(self):
        responses.add_callback(
            responses.POST,
            DEFAULT_URL + '/general/login',
            callback=login_callback,
            content_type='application/json'
        )

        responses.add_callback(
            responses.GET,
            DEFAULT_URL + '/segments/GetValueSegmentName',
            callback=get_value_segment_name_callback,
            content_type='application/json'
        )

        client = Client('username', 'password')
        data = client.segments.get_value_segment_name(2)
        self.assertFalse(data)

    @responses.activate
    def test_get_value_segment_id(self):
        responses.add_callback(
            responses.POST,
            DEFAULT_URL + '/general/login',
            callback=login_callback,
            content_type='application/json'
        )

        responses.add_callback(
            responses.GET,
            DEFAULT_URL + '/segments/GetValueSegmentID',
            callback=get_value_segment_id_callback,
            content_type='application/json'
        )

        client = Client('username', 'password')
        data = client.segments.get_value_segment_id('Diamond')
        self.assertEqual(data, 1)

    @responses.activate
    def test_get_value_segment_id_with_empty_segment_name(self):
        responses.add_callback(
            responses.POST,
            DEFAULT_URL + '/general/login',
            callback=login_callback,
            content_type='application/json'
        )

        responses.add_callback(
            responses.GET,
            DEFAULT_URL + '/segments/GetValueSegmentID',
            callback=get_value_segment_id_callback,
            content_type='application/json'
        )

        client = Client('username', 'password')
        self.assertRaises(Exception, client.segments.get_value_segment_id, None)

    @responses.activate
    def test_get_value_segment_id_with_wrong_segment_name(self):
        responses.add_callback(
            responses.POST,
            DEFAULT_URL + '/general/login',
            callback=login_callback,
            content_type='application/json'
        )

        responses.add_callback(
            responses.GET,
            DEFAULT_URL + '/segments/GetValueSegmentID',
            callback=get_value_segment_id_callback,
            content_type='application/json'
        )

        client = Client('username', 'password')
        data = client.segments.get_value_segment_id('Gold')
        self.assertFalse(data)

    @responses.activate
    def test_get_value_segments(self):
        responses.add_callback(
            responses.POST,
            DEFAULT_URL + '/general/login',
            callback=login_callback,
            content_type='application/json'
        )

        responses.add_callback(
            responses.GET,
            DEFAULT_URL + '/segments/GetValueSegments',
            callback=get_value_segments_callback,
            content_type='application/json'
        )

        client = Client('username', 'password')
        data = client.segments.get_value_segments()
        self.assertEqual(data, {
            1: 'Diamond',
            2: 'Gold',
            3: 'Silver',
            4: 'Bronze'
        })

    @responses.activate
    def test_get_customers_by_value_segment(self):
        responses.add_callback(
            responses.POST,
            DEFAULT_URL + '/general/login',
            callback=login_callback,
            content_type='application/json'
        )

        responses.add_callback(
            responses.GET,
            DEFAULT_URL + '/segments/GetCustomersByValueSegment',
            callback=get_customers_by_value_segment_callback,
            content_type='application/json'
        )

        client = Client('username', 'password')
        data = client.segments.get_customers_by_value_segment(3, '2015-05-10')
        self.assertEqual(data, ['AC7615', 'FP8721'])

    @responses.activate
    def test_get_customers_by_value_segment_with_attributes(self):
        responses.add_callback(
            responses.POST,
            DEFAULT_URL + '/general/login',
            callback=login_callback,
            content_type='application/json'
        )

        responses.add_callback(
            responses.GET,
            DEFAULT_URL + '/segments/GetCustomersByValueSegment',
            callback=get_customers_by_value_segment_callback,
            content_type='application/json'
        )

        client = Client('username', 'password')
        data = client.segments.get_customers_by_value_segment(3, '2015-05-10', ['Alias', 'Country'], ',')
        self.assertEqual(data, {
            'AC7615': {
                'Alias': 'Robin777',
                'Country': 'ES'
            },
            'FP8721': {
                'Alias': 'JollyPop',
                'Country': 'UK'
            }
        })

    @responses.activate
    def test_get_customers_by_value_segment_with_wrong_delimiter(self):
        responses.add_callback(
            responses.POST,
            DEFAULT_URL + '/general/login',
            callback=login_callback,
            content_type='application/json'
        )

        responses.add_callback(
            responses.GET,
            DEFAULT_URL + '/segments/GetCustomersByValueSegment',
            callback=get_customers_by_value_segment_callback,
            content_type='application/json'
        )

        client = Client('username', 'password')
        self.assertRaises(Exception, client.segments.get_customers_by_value_segment, 3, '2015-05-10',
                          ['Alias', 'Country'], '/')

    @responses.activate
    def test_get_customers_by_value_segment_with_empty_date(self):
        responses.add_callback(
            responses.POST,
            DEFAULT_URL + '/general/login',
            callback=login_callback,
            content_type='application/json'
        )

        responses.add_callback(
            responses.GET,
            DEFAULT_URL + '/segments/GetCustomersByValueSegment',
            callback=get_customers_by_value_segment_callback,
            content_type='application/json'
        )

        client = Client('username', 'password')
        self.assertRaises(Exception, client.segments.get_customers_by_value_segment, 3, None)

    @responses.activate
    def test_get_customers_by_value_segment_with_wrong_date(self):
        responses.add_callback(
            responses.POST,
            DEFAULT_URL + '/general/login',
            callback=login_callback,
            content_type='application/json'
        )

        responses.add_callback(
            responses.GET,
            DEFAULT_URL + '/segments/GetCustomersByValueSegment',
            callback=get_customers_by_value_segment_callback,
            content_type='application/json'
        )

        client = Client('username', 'password')
        data = client.segments.get_customers_by_value_segment(3, '3015-05-10')
        self.assertFalse(data)

    @responses.activate
    def test_get_value_segment_changers(self):
        responses.add_callback(
            responses.POST,
            DEFAULT_URL + '/general/login',
            callback=login_callback,
            content_type='application/json'
        )

        responses.add_callback(
            responses.GET,
            DEFAULT_URL + '/segments/GetValueSegmentChangers',
            callback=get_value_segment_changers_callback,
            content_type='application/json'
        )

        client = Client('username', 'password')
        data = client.segments.get_value_segment_changers('2015-09-01', '2015-09-30')
        self.assertEqual(data, [
            {
                'customer_id': '231342',
                'initial_value_segment': 2,
                'final_value_segment': 3
            },
            {
                'customer_id': '931342',
                'initial_value_segment': 1,
                'final_value_segment': 2
            },
        ])

    @responses.activate
    def test_get_value_segment_changers_with_delimiter(self):
        responses.add_callback(
            responses.POST,
            DEFAULT_URL + '/general/login',
            callback=login_callback,
            content_type='application/json'
        )

        responses.add_callback(
            responses.GET,
            DEFAULT_URL + '/segments/GetValueSegmentChangers',
            callback=get_value_segment_changers_callback,
            content_type='application/json'
        )

        client = Client('username', 'password')
        data = client.segments.get_value_segment_changers('2015-09-01', '2015-09-30', ['Alias', 'Country'], ',')
        self.assertEqual(data, [
            {
                'customer_id': '231342',
                'initial_value_segment': 2,
                'final_value_segment': 3,
                'attributes': {
                    'Alias': 'BuddyZZ',
                    'Country': 'UK'
                }
            },
            {
                'customer_id': '931342',
                'initial_value_segment': 1,
                'final_value_segment': 2,
                'attributes': {
                    'Alias': 'Pax65',
                    'Country': 'DE'
                }
            }
        ])

    @responses.activate
    def test_get_value_segment_changers_with_empty_date(self):
        responses.add_callback(
            responses.POST,
            DEFAULT_URL + '/general/login',
            callback=login_callback,
            content_type='application/json'
        )

        responses.add_callback(
            responses.GET,
            DEFAULT_URL + '/segments/GetValueSegmentChangers',
            callback=get_value_segment_changers_callback,
            content_type='application/json'
        )

        client = Client('username', 'password')
        self.assertRaises(Exception, client.segments.get_value_segment_changers, '2015-09-01', None)

    @responses.activate
    def test_get_value_segment_changers_with_wrong_delimiter(self):
        responses.add_callback(
            responses.POST,
            DEFAULT_URL + '/general/login',
            callback=login_callback,
            content_type='application/json'
        )

        responses.add_callback(
            responses.GET,
            DEFAULT_URL + '/segments/GetValueSegmentChangers',
            callback=get_value_segment_changers_callback,
            content_type='application/json'
        )

        client = Client('username', 'password')
        self.assertRaises(Exception, client.segments.get_value_segment_changers, '2015-09-01', '2015-09-30',
                          ['Country', 'Alias'], '/')

    @responses.activate
    def test_get_value_segment_changers_with_wrong_start_date(self):
        responses.add_callback(
            responses.POST,
            DEFAULT_URL + '/general/login',
            callback=login_callback,
            content_type='application/json'
        )

        responses.add_callback(
            responses.GET,
            DEFAULT_URL + '/segments/GetValueSegmentChangers',
            callback=get_value_segment_changers_callback,
            content_type='application/json'
        )

        client = Client('username', 'password')
        data = client.segments.get_value_segment_changers('3015-09-01', '3015-09-30')
        self.assertFalse(data)

