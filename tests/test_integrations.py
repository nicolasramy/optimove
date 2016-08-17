# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
import random
import string
import unittest
from urlparse import parse_qs, urlparse

from optimove.client import Client
import responses

from constants import HEADERS, TOKEN
from helpers import login_callback, token_required


"""Callbacks"""


@token_required
def add_promotions_callback(request):
    payload = json.loads(request.body)
    resp_body = all([True if item['PromotionName'] is not None and item['PromoCode'] is not None else False
                     for item in payload])
    return 200, HEADERS['json'], json.dumps(resp_body)


@token_required
def get_promotions_callback(request):
    resp_body = [
        {'PromoCode': 'WB23', 'PromotionName': 'Welcome back Promo'},
        {'PromoCode': 'NV10', 'PromotionName': 'New VIP 10% Discount'}
    ]
    return 200, HEADERS['json'], json.dumps(resp_body)


@token_required
def delete_promotions_callback(request):
    payload = json.loads(request.body)
    resp_body = all([True if item['PromoCode'] is not None else False for item in payload])
    return 200, HEADERS['json'], json.dumps(resp_body)


"""Tests"""


class TestIntegrations(unittest.TestCase):

    @responses.activate
    def test_add_promotions(self):
        responses.add_callback(
            responses.POST,
            'https://api.optimove.net/v3.0/general/login',
            callback=login_callback,
            content_type='application/json'
        )

        responses.add_callback(
            responses.POST,
            'https://api.optimove.net/v3.0/integrations/AddPromotions',
            callback=add_promotions_callback,
            content_type='application/json'
        )

        client = Client('username', 'password')
        data = client.integrations.add_promotions({
            'WB23': 'Welcome back Promo',
            'NV10': 'New VIP 10% Discount',
        })
        self.assertTrue(data)

    @responses.activate
    def test_add_promotion_with_empty_promotions(self):
        responses.add_callback(
            responses.POST,
            'https://api.optimove.net/v3.0/general/login',
            callback=login_callback,
            content_type='application/json'
        )

        responses.add_callback(
            responses.POST,
            'https://api.optimove.net/v3.0/integrations/AddPromotions',
            callback=add_promotions_callback,
            content_type='application/json'
        )

        client = Client('username', 'password')
        self.assertRaises(Exception, client.integrations.add_promotions, None)

    @responses.activate
    def test_add_promotions_overflow(self):
        responses.add_callback(
            responses.POST,
            'https://api.optimove.net/v3.0/general/login',
            callback=login_callback,
            content_type='application/json'
        )

        responses.add_callback(
            responses.POST,
            'https://api.optimove.net/v3.0/integrations/AddPromotions',
            callback=add_promotions_callback,
            content_type='application/json'
        )

        client = Client('username', 'password')
        too_much_promotions = {}
        for it in range(150):
            promo_code = ''.join([random.choice(string.ascii_uppercase + string.digits) for _ in range(5)])
            too_much_promotions[promo_code] = promo_code

        self.assertRaises(Exception, client.integrations.add_promotions, too_much_promotions)

    @responses.activate
    def test_get_promotions(self):
        responses.add_callback(
            responses.POST,
            'https://api.optimove.net/v3.0/general/login',
            callback=login_callback,
            content_type='application/json'
        )

        responses.add_callback(
            responses.GET,
            'https://api.optimove.net/v3.0/integrations/GetPromotions',
            callback=get_promotions_callback,
            content_type='application/json'
        )

        client = Client('username', 'password')
        data = client.integrations.get_promotions()
        self.assertEqual(data, {
            'WB23': 'Welcome back Promo',
            'NV10': 'New VIP 10% Discount'
        })

    @responses.activate
    def test_delete_promotions(self):
        responses.add_callback(
            responses.POST,
            'https://api.optimove.net/v3.0/general/login',
            callback=login_callback,
            content_type='application/json'
        )

        responses.add_callback(
            responses.POST,
            'https://api.optimove.net/v3.0/integrations/DeletePromotions',
            callback=delete_promotions_callback,
            content_type='application/json'
        )

        client = Client('username', 'password')
        data = client.integrations.delete_promotions(['WB23', 'NV10'])
        self.assertTrue(data)

    @responses.activate
    def test_delete_promotion_with_empty_promotions(self):
        responses.add_callback(
            responses.POST,
            'https://api.optimove.net/v3.0/general/login',
            callback=login_callback,
            content_type='application/json'
        )

        responses.add_callback(
            responses.POST,
            'https://api.optimove.net/v3.0/integrations/DeletePromotions',
            callback=delete_promotions_callback,
            content_type='application/json'
        )

        client = Client('username', 'password')
        self.assertRaises(Exception, client.integrations.delete_promotions, None)

    @responses.activate
    def test_delete_promotions_overflow(self):
        responses.add_callback(
            responses.POST,
            'https://api.optimove.net/v3.0/general/login',
            callback=login_callback,
            content_type='application/json'
        )

        responses.add_callback(
            responses.POST,
            'https://api.optimove.net/v3.0/integrations/DeletePromotions',
            callback=delete_promotions_callback,
            content_type='application/json'
        )

        client = Client('username', 'password')
        too_much_promotions = []
        for it in range(150):
            promo_code = ''.join([random.choice(string.ascii_uppercase + string.digits) for _ in range(5)])
            too_much_promotions.append(promo_code)

        self.assertRaises(Exception, client.integrations.delete_promotions, too_much_promotions)
