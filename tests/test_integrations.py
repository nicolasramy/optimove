# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
import random
import string
import unittest
from urlparse import parse_qs, urlparse

from optimove.client import Client
from optimove.integrations import Integrations
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


@token_required
def add_channel_templates_callback(request):
    payload = json.loads(request.body)
    params = parse_qs(urlparse(request.url).query)

    if params['ChannelID'][0] == '3':
        resp_body = all([True if item['TemplateID'] is not None and item['TemplateName'] is not None else False
                         for item in payload])
        return 200, HEADERS['json'], json.dumps(resp_body)

    else:
        return 404, HEADERS['text'], 'Not Found'


@token_required
def get_channel_templates_callback(request):
    params = parse_qs(urlparse(request.url).query)

    if params['ChannelID'][0] == '3':
        resp_body = [
            {'TemplateID': 1, 'TemplateName': 'Welcome Back English'},
            {'TemplateID': 2, 'TemplateName': 'Welcome Back Spanish'}
        ]
        return 200, HEADERS['json'], json.dumps(resp_body)

    else:
        return 404, HEADERS['text'], 'Not Found'


@token_required
def delete_channel_templates_callback(request):
    payload = json.loads(request.body)
    resp_body = all([True if item['ChannelID'] is not None and item['TemplateID'] is not None else False
                     for item in payload])
    return 200, HEADERS['json'], json.dumps(resp_body)


@token_required
def add_channel_apps_callback(request):
    payload = json.loads(request.body)
    params = parse_qs(urlparse(request.url).query)

    if params['ChannelID'][0] == '3':
        resp_body = all([True if item['AppID'] is not None and item['AppName'] is not None else False
                         for item in payload])
        return 200, HEADERS['json'], json.dumps(resp_body)

    else:
        return 404, HEADERS['text'], 'Not Found'


@token_required
def delete_channel_apps_callback(request):
    payload = json.loads(request.body)
    resp_body = all([True if item['ChannelID'] is not None and item['AppID'] is not None else False
                     for item in payload])
    return 200, HEADERS['json'], json.dumps(resp_body)


@token_required
def update_campaign_metrics_callback(request):
    payload = json.loads(request.body)

    resp_body = all([True if item['ChannelID'] is not None
                     and item['CampaignID'] is not None
                     and item['TemplateID'] is not None
                     and item['MetricID'] is not None
                     and item['MetricValue'] is not None else False for item in payload])
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
    def test_add_promotions_with_empty_promotions(self):
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
    def test_delete_promotions_with_empty_promotions(self):
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

    @responses.activate
    def test_add_channel_templates(self):
        responses.add_callback(
            responses.POST,
            'https://api.optimove.net/v3.0/general/login',
            callback=login_callback,
            content_type='application/json'
        )

        responses.add_callback(
            responses.POST,
            'https://api.optimove.net/v3.0/integrations/AddChannelTemplates',
            callback=add_channel_templates_callback,
            content_type='application/json'
        )

        client = Client('username', 'password')
        data = client.integrations.add_channel_templates(3, [
            {'id': 1, 'name': 'Welcome Back English'},
            {'id': 2, 'name': 'Welcome Back Spanish', 'app_id': 'app123'},
        ])
        self.assertTrue(data)

    @responses.activate
    def test_add_channel_templates_with_empty_channel_id(self):
        responses.add_callback(
            responses.POST,
            'https://api.optimove.net/v3.0/general/login',
            callback=login_callback,
            content_type='application/json'
        )

        responses.add_callback(
            responses.POST,
            'https://api.optimove.net/v3.0/integrations/AddChannelTemplates',
            callback=add_channel_templates_callback,
            content_type='application/json'
        )

        client = Client('username', 'password')
        self.assertRaises(Exception, client.integrations.add_channel_templates, None, [
            {'id': 1, 'name': 'Welcome Back English'},
            {'id': 2, 'name': 'Welcome Back Spanish', 'app_id': 'app123'},
        ])

    @responses.activate
    def test_add_channel_templates_overflow(self):
        responses.add_callback(
            responses.POST,
            'https://api.optimove.net/v3.0/general/login',
            callback=login_callback,
            content_type='application/json'
        )

        responses.add_callback(
            responses.POST,
            'https://api.optimove.net/v3.0/integrations/AddChannelTemplates',
            callback=add_channel_templates_callback,
            content_type='application/json'
        )

        client = Client('username', 'password')
        too_much_channel_templates = []
        for channel_template_id in range(150):
            channel_template = {
                'id': channel_template_id,
                'name': ''.join([random.choice(string.ascii_uppercase + string.digits + ' ') for _ in range(50)])
            }

            if random.choice([True, False]):
                channel_template['app_id'] = ''.join([random.choice(string.ascii_uppercase + string.digits)
                                                      for _ in range(5)])

            too_much_channel_templates.append(channel_template)

        self.assertRaises(Exception, client.integrations.add_channel_templates, 3, too_much_channel_templates)

    @responses.activate
    def test_get_channels_templates(self):
        responses.add_callback(
            responses.POST,
            'https://api.optimove.net/v3.0/general/login',
            callback=login_callback,
            content_type='application/json'
        )

        responses.add_callback(
            responses.GET,
            'https://api.optimove.net/v3.0/integrations/GetChannelTemplates',
            callback=get_channel_templates_callback,
            content_type='application/json'
        )

        client = Client('username', 'password')
        data = client.integrations.get_channel_templates(3)
        self.assertEqual(data, {
            1: 'Welcome Back English',
            2: 'Welcome Back Spanish'
        })

    @responses.activate
    def test_get_channels_templates_with_empty_channel_id(self):
        responses.add_callback(
            responses.POST,
            'https://api.optimove.net/v3.0/general/login',
            callback=login_callback,
            content_type='application/json'
        )

        responses.add_callback(
            responses.GET,
            'https://api.optimove.net/v3.0/integrations/GetChannelTemplates',
            callback=get_channel_templates_callback,
            content_type='application/json'
        )

        client = Client('username', 'password')
        self.assertRaises(Exception, client.integrations.get_channel_templates, None)

    @responses.activate
    def test_get_channels_templates_with_wrong_channel_id(self):
        responses.add_callback(
            responses.POST,
            'https://api.optimove.net/v3.0/general/login',
            callback=login_callback,
            content_type='application/json'
        )

        responses.add_callback(
            responses.GET,
            'https://api.optimove.net/v3.0/integrations/GetChannelTemplates',
            callback=get_channel_templates_callback,
            content_type='application/json'
        )

        client = Client('username', 'password')
        data = client.integrations.get_channel_templates(4)
        self.assertFalse(data)

    @responses.activate
    def test_delete_channel_templates(self):
        responses.add_callback(
            responses.POST,
            'https://api.optimove.net/v3.0/general/login',
            callback=login_callback,
            content_type='application/json'
        )

        responses.add_callback(
            responses.POST,
            'https://api.optimove.net/v3.0/integrations/DeleteChannelTemplates',
            callback=delete_channel_templates_callback,
            content_type='application/json'
        )

        client = Client('username', 'password')
        data = client.integrations.delete_channel_templates([
            {'channel_id': 3, 'template_id': 15},
            {'channel_id': 4, 'template_id': 26}
        ])
        self.assertTrue(data)

    @responses.activate
    def test_delete_channel_templates_with_empty_channel_templates(self):
        responses.add_callback(
            responses.POST,
            'https://api.optimove.net/v3.0/general/login',
            callback=login_callback,
            content_type='application/json'
        )

        responses.add_callback(
            responses.POST,
            'https://api.optimove.net/v3.0/integrations/DeleteChannelTemplates',
            callback=delete_channel_templates_callback,
            content_type='application/json'
        )

        client = Client('username', 'password')
        self.assertRaises(Exception, client.integrations.delete_channel_templates, None)

    @responses.activate
    def test_delete_channel_templates_overflow(self):
        responses.add_callback(
            responses.POST,
            'https://api.optimove.net/v3.0/general/login',
            callback=login_callback,
            content_type='application/json'
        )

        responses.add_callback(
            responses.POST,
            'https://api.optimove.net/v3.0/integrations/DeleteChannelTemplates',
            callback=delete_channel_templates_callback,
            content_type='application/json'
        )

        client = Client('username', 'password')
        too_much_channel_templates = []
        for channel_template_id in range(150):
            channel_template = {
                'template_id': channel_template_id,
                'channel_id': random.choice(range(1, 5))
            }
            too_much_channel_templates.append(channel_template)

        self.assertRaises(Exception, client.integrations.delete_channel_templates, too_much_channel_templates)

    @responses.activate
    def test_add_channel_apps(self):
        responses.add_callback(
            responses.POST,
            'https://api.optimove.net/v3.0/general/login',
            callback=login_callback,
            content_type='application/json'
        )

        responses.add_callback(
            responses.POST,
            'https://api.optimove.net/v3.0/integrations/AddChannelApps',
            callback=add_channel_apps_callback,
            content_type='application/json'
        )

        client = Client('username', 'password')
        data = client.integrations.add_channel_apps(3, {
            1: 'Bingo Mania',
            2: 'Super Slots'
        })
        self.assertTrue(data)

    @responses.activate
    def test_add_channel_apps_with_empty_channel_id(self):
        responses.add_callback(
            responses.POST,
            'https://api.optimove.net/v3.0/general/login',
            callback=login_callback,
            content_type='application/json'
        )

        responses.add_callback(
            responses.POST,
            'https://api.optimove.net/v3.0/integrations/AddChannelApps',
            callback=add_channel_apps_callback,
            content_type='application/json'
        )

        client = Client('username', 'password')
        self.assertRaises(Exception, client.integrations.add_channel_apps, None, {
            1: 'Bingo Mania',
            2: 'Super Slots'
        })

    @responses.activate
    def test_add_channel_apps_overflow(self):
        responses.add_callback(
            responses.POST,
            'https://api.optimove.net/v3.0/general/login',
            callback=login_callback,
            content_type='application/json'
        )

        responses.add_callback(
            responses.POST,
            'https://api.optimove.net/v3.0/integrations/AddChannelApps',
            callback=add_channel_apps_callback,
            content_type='application/json'
        )

        client = Client('username', 'password')
        too_much_channel_apps = {}
        for app_id in range(150):
            too_much_channel_apps[app_id] = \
                ''.join([random.choice(string.ascii_uppercase + string.digits + ' ') for _ in range(50)])

        self.assertRaises(Exception, client.integrations.add_channel_apps, 3, too_much_channel_apps)

    @responses.activate
    def test_delete_channel_apps(self):
        responses.add_callback(
            responses.POST,
            'https://api.optimove.net/v3.0/general/login',
            callback=login_callback,
            content_type='application/json'
        )

        responses.add_callback(
            responses.POST,
            'https://api.optimove.net/v3.0/integrations/DeleteChannelApps',
            callback=delete_channel_apps_callback,
            content_type='application/json'
        )

        client = Client('username', 'password')
        data = client.integrations.delete_channel_apps([
            {'channel_id': 3, 'app_id': 1},
            {'channel_id': 3, 'app_id': 2}
        ])
        self.assertTrue(data)

    @responses.activate
    def test_delete_channel_apps_with_empty_channel_apps(self):
        responses.add_callback(
            responses.POST,
            'https://api.optimove.net/v3.0/general/login',
            callback=login_callback,
            content_type='application/json'
        )

        responses.add_callback(
            responses.POST,
            'https://api.optimove.net/v3.0/integrations/DeleteChannelApps',
            callback=delete_channel_apps_callback,
            content_type='application/json'
        )

        client = Client('username', 'password')
        self.assertRaises(Exception, client.integrations.delete_channel_apps, None)

    @responses.activate
    def test_delete_channel_apps_overflow(self):
        responses.add_callback(
            responses.POST,
            'https://api.optimove.net/v3.0/general/login',
            callback=login_callback,
            content_type='application/json'
        )

        responses.add_callback(
            responses.POST,
            'https://api.optimove.net/v3.0/integrations/DeleteChannelApps',
            callback=delete_channel_apps_callback,
            content_type='application/json'
        )

        client = Client('username', 'password')
        too_much_channel_apps = []
        for channel_app_id in range(150):
            channel_app = {
                'app_id': channel_app_id,
                'channel_id': random.choice(range(1, 5))
            }
            too_much_channel_apps.append(channel_app)

        self.assertRaises(Exception, client.integrations.delete_channel_apps, too_much_channel_apps)

    @responses.activate
    def test_update_campaign_metrics(self):
        responses.add_callback(
            responses.POST,
            'https://api.optimove.net/v3.0/general/login',
            callback=login_callback,
            content_type='application/json'
        )

        responses.add_callback(
            responses.POST,
            'https://api.optimove.net/v3.0/integrations/UpdateCampaignMetrics',
            callback=update_campaign_metrics_callback,
            content_type='application/json'
        )

        client = Client('username', 'password')
        data = client.integrations.update_campaign_metrics([
            {'channel_id': 3, 'campaign_id': 42, 'template_id': 8,
             'metric': Integrations.METRIC_SENT, 'value': 925},
            {'channel_id': 3, 'campaign_id': 42, 'template_id': 8,
             'metric': Integrations.METRIC_DELIVERED, 'value': 809},
            {'channel_id': 3, 'campaign_id': 42, 'template_id': 8,
             'metric': Integrations.METRIC_OPENED, 'value': 250},
            {'channel_id': 3, 'campaign_id': 42, 'template_id': 8,
             'metric': Integrations.METRIC_CLICKED, 'value': 122},
            {'channel_id': 3, 'campaign_id': 42, 'template_id': 8,
             'metric': Integrations.METRIC_UNSUBSCRIBED, 'value': 11}
        ])
        self.assertTrue(data)

    @responses.activate
    def test_update_campaign_metrics_with_empty_metrics(self):
        responses.add_callback(
            responses.POST,
            'https://api.optimove.net/v3.0/general/login',
            callback=login_callback,
            content_type='application/json'
        )

        responses.add_callback(
            responses.POST,
            'https://api.optimove.net/v3.0/integrations/UpdateCampaignMetrics',
            callback=update_campaign_metrics_callback,
            content_type='application/json'
        )

        client = Client('username', 'password')
        self.assertRaises(Exception, client.integrations.update_campaign_metrics, None)

    @responses.activate
    def test_update_campaign_metrics_overflow(self):
        responses.add_callback(
            responses.POST,
            'https://api.optimove.net/v3.0/general/login',
            callback=login_callback,
            content_type='application/json'
        )

        responses.add_callback(
            responses.POST,
            'https://api.optimove.net/v3.0/integrations/UpdateCampaignMetrics',
            callback=update_campaign_metrics_callback,
            content_type='application/json'
        )

        client = Client('username', 'password')
        too_much_metrics = []
        for campaign_id in range(25):
            template_id = random.choice(range(1, 100))
            too_much_metrics.append({
                'channel_id': 3,
                'campaign_id': campaign_id,
                'template_id': template_id,
                'metric': Integrations.METRIC_SENT,
                'value': random.choice(range(1000))
            })
            too_much_metrics.append({
                'channel_id': 3,
                'campaign_id': campaign_id,
                'template_id': template_id,
                'metric': Integrations.METRIC_DELIVERED,
                'value': random.choice(range(1000))
            })
            too_much_metrics.append({
                'channel_id': 3,
                'campaign_id': campaign_id,
                'template_id': template_id,
                'metric': Integrations.METRIC_OPENED,
                'value': random.choice(range(1000))
            })
            too_much_metrics.append({
                'channel_id': 3,
                'campaign_id': campaign_id,
                'template_id': template_id,
                'metric': Integrations.METRIC_CLICKED,
                'value': random.choice(range(1000))
            })
            too_much_metrics.append({
                'channel_id': 3,
                'campaign_id': campaign_id,
                'template_id': template_id,
                'metric': Integrations.METRIC_UNSUBSCRIBED,
                'value': random.choice(range(1000))
            })

        self.assertRaises(Exception, client.integrations.update_campaign_metrics, too_much_metrics)
