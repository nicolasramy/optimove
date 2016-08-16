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
def get_value_segment_name_callback(request):
    params = parse_qs(urlparse(request.url).query)

    if params['ValueSegmentID'][0] == '1':
        resp_body = {'ValueSegmentName': 'Diamond'}
        return 200, HEADERS['json'], json.dumps(resp_body)

    else:
        return 404, HEADERS['text'], 'Not Found'


"""Tests"""


class TestSegments(unittest.TestCase):

    @responses.activate
    def test_get_value_segment_name(self):
        responses.add_callback(
            responses.POST,
            'https://api.optimove.net/v3.0/general/login',
            callback=login_callback,
            content_type='application/json'
        )

        responses.add_callback(
            responses.GET,
            'https://api.optimove.net/v3.0/segments/GetValueSegmentName',
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
            'https://api.optimove.net/v3.0/general/login',
            callback=login_callback,
            content_type='application/json'
        )

        responses.add_callback(
            responses.GET,
            'https://api.optimove.net/v3.0/segments/GetValueSegmentName',
            callback=get_value_segment_name_callback,
            content_type='application/json'
        )

        client = Client('username', 'password')
        self.assertRaises(Exception, client.segments.get_value_segment_name, None)

    @responses.activate
    def test_get_value_segment_name_with_wrong_segment_id(self):
        responses.add_callback(
            responses.POST,
            'https://api.optimove.net/v3.0/general/login',
            callback=login_callback,
            content_type='application/json'
        )

        responses.add_callback(
            responses.GET,
            'https://api.optimove.net/v3.0/segments/GetValueSegmentName',
            callback=get_value_segment_name_callback,
            content_type='application/json'
        )

        client = Client('username', 'password')
        data = client.segments.get_value_segment_name(2)
        self.assertFalse(data)
