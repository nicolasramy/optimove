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
def get_action_name_callback(request):
    params = parse_qs(urlparse(request.url).query)
    if params['ActionID'][0] == '104':
        resp_body = {'ActionName': '10% summer bonus'}
        return 200, HEADERS['json'], json.dumps(resp_body)
    else:
        return 404, HEADERS['text'], 'Not Found'


@token_required
def get_action_id_callback(request):
    params = parse_qs(urlparse(request.url).query)
    if params['ActionName'][0] == 'Free Shipping':
        resp_body = {'ActionID': 25}
        return 200, HEADERS['json'], json.dumps(resp_body)
    else:
        return 404, HEADERS['text'], 'Not Found'


@token_required
def get_all_actions_callback(request):
    resp_body = [
        {'ActionID': 1, 'ActionName': '10% Bonus'},
        {'ActionID': 2, 'ActionName': '15% Bonus'},
        {'ActionID': 3, 'ActionName': '20% Bonus'}
    ]
    return 200, HEADERS['json'], json.dumps(resp_body)


@token_required
def get_actions_by_target_group_callback(request):
    params = parse_qs(urlparse(request.url).query)

    if params['TargetGroupID'][0] == '7' and params['Date'][0] == '2015-10-23':
        resp_body = [
            {'RecipientGroupID': 1, 'ActionID': 23},
            {'RecipientGroupID': 2, 'ActionID': 27}
        ]
        return 200, HEADERS['json'], json.dumps(resp_body)

    else:
        return 404, HEADERS['text'], 'Not Found'


@token_required
def get_promo_codes_callback(request):
    params = parse_qs(urlparse(request.url).query)

    if params['Date'][0] == '2015-02-20':
        resp_body = [
            {'TargetGroupID': 9, 'RecipientGroupID': 1, 'ActionID': 24, 'PromoCode': 'HEP-FEB'},
            {'TargetGroupID': 9, 'RecipientGroupID': 2, 'ActionID': 25, 'PromoCode': 'HEP-FCC'},
            {'TargetGroupID': 13, 'RecipientGroupID': 1, 'ActionID': 65, 'PromoCode': 'GDG-FAL'}
        ]
        return 200, HEADERS['json'], json.dumps(resp_body)

    else:
        return 404, HEADERS['text'], 'Not Found'


@token_required
def get_promo_codes_by_campaign_callback(request):
    params = parse_qs(urlparse(request.url).query)

    if params['CampaignID'][0] == '721':
        resp_body = [
            {'RecipientGroupID': 1, 'ActionID': 24, 'PromoCode': 'HEP-75-FEB'},
            {'RecipientGroupID': 2, 'ActionID': 65, 'PromoCode': 'GDG-50-FRT'}
        ]
        return 200, HEADERS['json'], json.dumps(resp_body)

    else:
        return 404, HEADERS['text'], 'Not Found'


@token_required
def get_promo_codes_by_target_group_callback(request):
    params = parse_qs(urlparse(request.url).query)

    if params['TargetGroupID'][0] == '41' and params['Date'][0] == '2015-09-23':
        resp_body = [
            {'RecipientGroupID': 1, 'ActionID': 24, 'PromoCode': 'HEP-FEB'},
            {'RecipientGroupID': 2, 'ActionID': 25, 'PromoCode': 'HEP-FCC'},
            {'RecipientGroupID': 1, 'ActionID': 65, 'PromoCode': 'GDG-FAL'}
        ]
        return 200, HEADERS['json'], json.dumps(resp_body)

    else:
        return 404, HEADERS['text'], 'Not Found'


@token_required
def get_action_details_by_target_group_callback(request):
    params = parse_qs(urlparse(request.url).query)

    if params['TargetGroupID'][0] == '9' and params['Date'][0] == '2015-11-11':
        resp_body = [
            {'RecipientGroupID': 1, 'ActionID': 65, 'Duration': 7, 'LeadTime': 0, 'ChannelID': 1},
            {'RecipientGroupID': 1, 'ActionID': 78, 'Duration': 7, 'LeadTime': 0, 'ChannelID': 3}
        ]
        return 200, HEADERS['json'], json.dumps(resp_body)

    else:
        return 404, HEADERS['text'], 'Not Found'


@token_required
def get_executed_campaign_details_callback(request):
    params = parse_qs(urlparse(request.url).query)

    if params['Date'][0] == '2015-06-19':
        resp_body = [
            {'CampaignID': 221, 'TargetGroupID': 15, 'CampaignType': 'Test/Control', 'Duration': 7,
             'LeadTime': 3, 'Notes': '', 'IsMultiChannel': 'false', 'IsRecurrence': 'false',
             'Status': 'Successful', 'Error': ''},
            {'CampaignID': 81, 'TargetGroupID': 40, 'CampaignType': 'Test/Control', 'Duration': 10,
             'LeadTime': 0, 'Notes': '', 'IsMultiChannel': 'true', 'IsRecurrence': 'true',
             'Status': 'Failed', 'Error': 'ESP unavailable'}
        ]
        return 200, HEADERS['json'], json.dumps(resp_body)

    else:
        return 404, HEADERS['text'], 'Not Found'


@token_required
def get_campaign_details_callback(request):
    params = parse_qs(urlparse(request.url).query)

    if params['CampaignID'][0] == '21':
        resp_body = {'TargetGroupID': 15, 'CampaignType': 'Test/Control', 'Duration': 7,
                     'LeadTime': 3, 'Notes': '', 'IsMultiChannel': 'false', 'IsRecurrence': 'false',
                     'Status': 'Successful', 'Error': ''}
        return 200, HEADERS['json'], json.dumps(resp_body)

    else:
        return 404, HEADERS['text'], 'Not Found'


@token_required
def get_execution_channels_callback(request):
    resp_body = [
        {'ChannelID': 1, 'ChannelName': 'Silverpop'},
        {'ChannelID': 2, 'ChannelName': 'ExactTarget'},
        {'ChannelID': 3, 'ChannelName': 'Lobby Banner'},
        {'ChannelID': 4, 'ChannelName': 'Call Center'}
    ]
    return 200, HEADERS['json'], json.dumps(resp_body)


@token_required
def get_executed_campaign_channel_details_callback(request):
    params = parse_qs(urlparse(request.url).query)

    if params['CampaignID'][0] == '9214' and params['ChannelID'][0] == '35':
        resp_body = [
            {'ListID': 12, 'SendID': 'YTGF3C', 'TemplateID': 520, 'ScheduledTime': '2015-12-30 08:00:00'},
            {'TemplateID': 27, 'ScheduledTime': '2016-08-23 16:00:00', 'SendID': ''},
            {'TemplateID': 1321, 'ScheduledTime': '2016-08-23 18:00:00', 'SendID': ''}
        ]
        return 200, HEADERS['json'], json.dumps(resp_body)

    else:
        return 404, HEADERS['text'], 'Not Found'


@token_required
def get_executed_campaigns_by_channel_callback(request):
    params = parse_qs(urlparse(request.url).query)

    if params['ChannelID'][0] == '35' and params['Date'][0] == '2016-02-20':
        resp_body = [
            {'CampaignID': 12}, {'CampaignID': 16}, {'CampaignID': 17}, {'CampaignID': 19}
        ]
        return 200, HEADERS['json'], json.dumps(resp_body)

    else:
        return 404, HEADERS['text'], 'Not Found'


"""Tests"""


class TestActions(unittest.TestCase):

    @responses.activate
    def test_get_action_name(self):
        responses.add_callback(
            responses.POST,
            DEFAULT_URL + '/general/login',
            callback=login_callback,
            content_type='application/json'
        )

        responses.add_callback(
            responses.GET,
            DEFAULT_URL + '/actions/GetActionName',
            callback=get_action_name_callback,
            content_type='application/json'
        )

        client = Client('username', 'password')
        data = client.actions.get_action_name(104)
        self.assertEqual(data, '10% summer bonus')

    @responses.activate
    def test_get_action_name_with_empty_action_id(self):
        responses.add_callback(
            responses.POST,
            DEFAULT_URL + '/general/login',
            callback=login_callback,
            content_type='application/json'
        )

        responses.add_callback(
            responses.GET,
            DEFAULT_URL + '/actions/GetActionName',
            callback=get_action_name_callback,
            content_type='application/json'
        )

        client = Client('username', 'password')
        self.assertRaises(Exception, client.actions.get_action_name, None)

    @responses.activate
    def test_get_action_id(self):
        responses.add_callback(
            responses.POST,
            DEFAULT_URL + '/general/login',
            callback=login_callback,
            content_type='application/json'
        )

        responses.add_callback(
            responses.GET,
            DEFAULT_URL + '/actions/GetActionID',
            callback=get_action_id_callback,
            content_type='application/json'
        )

        client = Client('username', 'password')
        data = client.actions.get_action_id('Free Shipping')
        self.assertEqual(data, 25)

    @responses.activate
    def test_get_action_id_with_empty_action_name(self):
        responses.add_callback(
            responses.POST,
            DEFAULT_URL + '/general/login',
            callback=login_callback,
            content_type='application/json'
        )

        responses.add_callback(
            responses.GET,
            DEFAULT_URL + '/actions/GetActionID',
            callback=get_action_id_callback,
            content_type='application/json'
        )

        client = Client('username', 'password')
        self.assertRaises(Exception, client.actions.get_action_id, None)

    @responses.activate
    def test_get_all_actions(self):
        responses.add_callback(
            responses.POST,
            DEFAULT_URL + '/general/login',
            callback=login_callback,
            content_type='application/json'
        )

        responses.add_callback(
            responses.GET,
            DEFAULT_URL + '/actions/GetAllActions',
            callback=get_all_actions_callback,
            content_type='application/json'
        )

        client = Client('username', 'password')
        data = client.actions.get_all_actions()
        self.assertEqual(data, {
            1: '10% Bonus',
            2: '15% Bonus',
            3: '20% Bonus'
        })

    @responses.activate
    def test_get_actions_by_target_group(self):
        responses.add_callback(
            responses.POST,
            DEFAULT_URL + '/general/login',
            callback=login_callback,
            content_type='application/json'
        )

        responses.add_callback(
            responses.GET,
            DEFAULT_URL + '/actions/GetActionsByTargetGroup',
            callback=get_actions_by_target_group_callback,
            content_type='application/json'
        )

        client = Client('username', 'password')
        data = client.actions.get_actions_by_target_group(7, '2015-10-23')
        self.assertEqual(data, {
            1: 23,
            2: 27
        })

    @responses.activate
    def test_get_actions_by_target_group_with_empty_date(self):
        responses.add_callback(
            responses.POST,
            DEFAULT_URL + '/general/login',
            callback=login_callback,
            content_type='application/json'
        )

        responses.add_callback(
            responses.GET,
            DEFAULT_URL + '/actions/GetActionsByTargetGroup',
            callback=get_actions_by_target_group_callback,
            content_type='application/json'
        )

        client = Client('username', 'password')
        self.assertRaises(Exception, client.actions.get_actions_by_target_group, 7, None)

    @responses.activate
    def test_get_actions_by_target_group_with_wrong_date(self):
        responses.add_callback(
            responses.POST,
            DEFAULT_URL + '/general/login',
            callback=login_callback,
            content_type='application/json'
        )

        responses.add_callback(
            responses.GET,
            DEFAULT_URL + '/actions/GetActionsByTargetGroup',
            callback=get_actions_by_target_group_callback,
            content_type='application/json'
        )

        client = Client('username', 'password')
        data = client.actions.get_actions_by_target_group(7, '3015-10-23')
        self.assertFalse(data)

    @responses.activate
    def test_get_promo_codes(self):
        responses.add_callback(
            responses.POST,
            DEFAULT_URL + '/general/login',
            callback=login_callback,
            content_type='application/json'
        )

        responses.add_callback(
            responses.GET,
            DEFAULT_URL + '/actions/GetPromoCodes',
            callback=get_promo_codes_callback,
            content_type='application/json'
        )

        client = Client('username', 'password')
        data = client.actions.get_promo_codes('2015-02-20')
        self.assertEqual(data, [
            {'target_group_id': 9, 'recipient_group_id': 1, 'action_id': 24, 'promo_code': 'HEP-FEB'},
            {'target_group_id': 9, 'recipient_group_id': 2, 'action_id': 25, 'promo_code': 'HEP-FCC'},
            {'target_group_id': 13, 'recipient_group_id': 1, 'action_id': 65, 'promo_code': 'GDG-FAL'}
        ])

    @responses.activate
    def test_get_promo_codes_with_empty_date(self):
        responses.add_callback(
            responses.POST,
            DEFAULT_URL + '/general/login',
            callback=login_callback,
            content_type='application/json'
        )

        responses.add_callback(
            responses.GET,
            DEFAULT_URL + '/actions/GetPromoCodes',
            callback=get_promo_codes_callback,
            content_type='application/json'
        )

        client = Client('username', 'password')
        self.assertRaises(Exception, client.actions.get_promo_codes, None)

    @responses.activate
    def test_get_promo_codes_with_wrong_date(self):
        responses.add_callback(
            responses.POST,
            DEFAULT_URL + '/general/login',
            callback=login_callback,
            content_type='application/json'
        )

        responses.add_callback(
            responses.GET,
            DEFAULT_URL + '/actions/GetPromoCodes',
            callback=get_promo_codes_callback,
            content_type='application/json'
        )

        client = Client('username', 'password')
        data = client.actions.get_promo_codes('3015-02-20')
        self.assertFalse(data)

    @responses.activate
    def test_get_promo_codes_by_campaign(self):
        responses.add_callback(
            responses.POST,
            DEFAULT_URL + '/general/login',
            callback=login_callback,
            content_type='application/json'
        )

        responses.add_callback(
            responses.GET,
            DEFAULT_URL + '/actions/GetPromoCodesByCampaign',
            callback=get_promo_codes_by_campaign_callback,
            content_type='application/json'
        )

        client = Client('username', 'password')
        data = client.actions.get_promo_codes_by_campaign(721)
        self.assertEqual(data, [
            {'campaign_id': 721, 'recipient_group_id': 1, 'action_id': 24, 'promo_code': 'HEP-75-FEB'},
            {'campaign_id': 721, 'recipient_group_id': 2, 'action_id': 65, 'promo_code': 'GDG-50-FRT'}
        ])

    @responses.activate
    def test_get_promo_codes_by_campaign_with_empty_campaign_id(self):
        responses.add_callback(
            responses.POST,
            DEFAULT_URL + '/general/login',
            callback=login_callback,
            content_type='application/json'
        )

        responses.add_callback(
            responses.GET,
            DEFAULT_URL + '/actions/GetPromoCodesByCampaign',
            callback=get_promo_codes_by_campaign_callback,
            content_type='application/json'
        )

        client = Client('username', 'password')
        self.assertRaises(Exception, client.actions.get_promo_codes_by_campaign, None)

    @responses.activate
    def test_get_promo_codes_by_campaign_with_wrong_campaign_id(self):
        responses.add_callback(
            responses.POST,
            DEFAULT_URL + '/general/login',
            callback=login_callback,
            content_type='application/json'
        )

        responses.add_callback(
            responses.GET,
            DEFAULT_URL + '/actions/GetPromoCodesByCampaign',
            callback=get_promo_codes_by_campaign_callback,
            content_type='application/json'
        )

        client = Client('username', 'password')
        data = client.actions.get_promo_codes_by_campaign(127)
        self.assertFalse(data)

    @responses.activate
    def test_get_promo_codes_by_target_group(self):
        responses.add_callback(
            responses.POST,
            DEFAULT_URL + '/general/login',
            callback=login_callback,
            content_type='application/json'
        )

        responses.add_callback(
            responses.GET,
            DEFAULT_URL + '/actions/GetPromoCodesByTargetGroup',
            callback=get_promo_codes_by_target_group_callback,
            content_type='application/json'
        )

        client = Client('username', 'password')
        data = client.actions.get_promo_codes_by_target_group(41, '2015-09-23')
        self.assertEqual(data, [
            {'target_group_id': 41, 'recipient_group_id': 1, 'action_id': 24, 'promo_code': 'HEP-FEB'},
            {'target_group_id': 41, 'recipient_group_id': 2, 'action_id': 25, 'promo_code': 'HEP-FCC'},
            {'target_group_id': 41, 'recipient_group_id': 1, 'action_id': 65, 'promo_code': 'GDG-FAL'}
        ])

    @responses.activate
    def test_get_promo_codes_by_target_group_with_empty_date(self):
        responses.add_callback(
            responses.POST,
            DEFAULT_URL + '/general/login',
            callback=login_callback,
            content_type='application/json'
        )

        responses.add_callback(
            responses.GET,
            DEFAULT_URL + '/actions/GetPromoCodesByTargetGroup',
            callback=get_promo_codes_by_target_group_callback,
            content_type='application/json'
        )

        client = Client('username', 'password')
        self.assertRaises(Exception, client.actions.get_promo_codes_by_target_group, 41, None)

    @responses.activate
    def test_get_promo_codes_by_target_group_with_wrong_date(self):
        responses.add_callback(
            responses.POST,
            DEFAULT_URL + '/general/login',
            callback=login_callback,
            content_type='application/json'
        )

        responses.add_callback(
            responses.GET,
            DEFAULT_URL + '/actions/GetPromoCodesByTargetGroup',
            callback=get_promo_codes_by_target_group_callback,
            content_type='application/json'
        )

        client = Client('username', 'password')
        data = client.actions.get_promo_codes_by_target_group(41, '3015-09-23')
        self.assertFalse(data)

    @responses.activate
    def test_get_action_details_by_target_group(self):
        responses.add_callback(
            responses.POST,
            DEFAULT_URL + '/general/login',
            callback=login_callback,
            content_type='application/json'
        )

        responses.add_callback(
            responses.GET,
            DEFAULT_URL + '/actions/GetActionDetailsByTargetGroup',
            callback=get_action_details_by_target_group_callback,
            content_type='application/json'
        )

        client = Client('username', 'password')
        data = client.actions.get_action_details_by_target_group(9, '2015-11-11')
        self.assertEqual(data, [
            {'target_group_id': 9, 'recipient_group_id': 1, 'action_id': 65,
             'duration': 7, 'lead_time': 0, 'channel_id': 1},
            {'target_group_id': 9, 'recipient_group_id': 1, 'action_id': 78,
             'duration': 7, 'lead_time': 0, 'channel_id': 3},
        ])

    @responses.activate
    def test_get_action_details_by_target_group_with_empty_date(self):
        responses.add_callback(
            responses.POST,
            DEFAULT_URL + '/general/login',
            callback=login_callback,
            content_type='application/json'
        )

        responses.add_callback(
            responses.GET,
            DEFAULT_URL + '/actions/GetActionDetailsByTargetGroup',
            callback=get_action_details_by_target_group_callback,
            content_type='application/json'
        )

        client = Client('username', 'password')
        self.assertRaises(Exception, client.actions.get_action_details_by_target_group, 9, None)

    @responses.activate
    def test_get_action_details_by_target_group_with_wrong_date(self):
        responses.add_callback(
            responses.POST,
            DEFAULT_URL + '/general/login',
            callback=login_callback,
            content_type='application/json'
        )

        responses.add_callback(
            responses.GET,
            DEFAULT_URL + '/actions/GetActionDetailsByTargetGroup',
            callback=get_action_details_by_target_group_callback,
            content_type='application/json'
        )

        client = Client('username', 'password')
        data = client.actions.get_action_details_by_target_group(9, '3015-11-11')
        self.assertFalse(data)

    @responses.activate
    def test_get_executed_campaign_details(self):
        responses.add_callback(
            responses.POST,
            DEFAULT_URL + '/general/login',
            callback=login_callback,
            content_type='application/json'
        )

        responses.add_callback(
            responses.GET,
            DEFAULT_URL + '/actions/GetExecutedCampaignDetails',
            callback=get_executed_campaign_details_callback,
            content_type='application/json'
        )

        client = Client('username', 'password')
        data = client.actions.get_executed_campaign_details('2015-06-19')
        self.assertEqual(data, {
            221: {
                'target_group_id': 15,
                'campaign_type': 'Test/Control',
                'duration': 7,
                'lead_time': 3,
                'notes': '',
                'is_multi_channel': False,
                'is_recurrence': False,
                'status': 'Successful',
                'error': '',
            },
            81: {
                'target_group_id': 40,
                'campaign_type': 'Test/Control',
                'duration': 10,
                'lead_time': 0,
                'notes': '',
                'is_multi_channel': True,
                'is_recurrence': True,
                'status': 'Failed',
                'error': 'ESP unavailable',
            }
        })

    @responses.activate
    def test_get_executed_campaign_details_with_empty_date(self):
        responses.add_callback(
            responses.POST,
            DEFAULT_URL + '/general/login',
            callback=login_callback,
            content_type='application/json'
        )

        responses.add_callback(
            responses.GET,
            DEFAULT_URL + '/actions/GetExecutedCampaignDetails',
            callback=get_executed_campaign_details_callback,
            content_type='application/json'
        )

        client = Client('username', 'password')
        self.assertRaises(Exception, client.actions.get_executed_campaign_details, None)

    @responses.activate
    def test_get_executed_campaign_details_with_wrong_date(self):
        responses.add_callback(
            responses.POST,
            DEFAULT_URL + '/general/login',
            callback=login_callback,
            content_type='application/json'
        )

        responses.add_callback(
            responses.GET,
            DEFAULT_URL + '/actions/GetExecutedCampaignDetails',
            callback=get_executed_campaign_details_callback,
            content_type='application/json'
        )

        client = Client('username', 'password')
        data = client.actions.get_executed_campaign_details('3015-06-19')
        self.assertFalse(data)

    @responses.activate
    def test_get_campaign_details(self):
        responses.add_callback(
            responses.POST,
            DEFAULT_URL + '/general/login',
            callback=login_callback,
            content_type='application/json'
        )

        responses.add_callback(
            responses.GET,
            DEFAULT_URL + '/actions/GetCampaignDetails',
            callback=get_campaign_details_callback,
            content_type='application/json'
        )

        client = Client('username', 'password')
        data = client.actions.get_campaign_details(21)
        self.assertEqual(data, {'campaign_id': 21, 'target_group_id': 15, 'campaign_type': 'Test/Control',
                                'duration': 7, 'lead_time': 3, 'notes': '', 'is_multi_channel': False,
                                'is_recurrence': False, 'status': 'Successful', 'error': ''})

    @responses.activate
    def test_get_campaign_details_with_empty_campaign_id(self):
        responses.add_callback(
            responses.POST,
            DEFAULT_URL + '/general/login',
            callback=login_callback,
            content_type='application/json'
        )

        responses.add_callback(
            responses.GET,
            DEFAULT_URL + '/actions/GetCampaignDetails',
            callback=get_campaign_details_callback,
            content_type='application/json'
        )

        client = Client('username', 'password')
        self.assertRaises(Exception, client.actions.get_campaign_details, None)

    @responses.activate
    def test_get_campaign_details_with_wrong_campaign_id(self):
        responses.add_callback(
            responses.POST,
            DEFAULT_URL + '/general/login',
            callback=login_callback,
            content_type='application/json'
        )

        responses.add_callback(
            responses.GET,
            DEFAULT_URL + '/actions/GetCampaignDetails',
            callback=get_campaign_details_callback,
            content_type='application/json'
        )

        client = Client('username', 'password')
        data = client.actions.get_campaign_details(12)
        self.assertFalse(data)

    @responses.activate
    def test_get_execution_channels(self):
        responses.add_callback(
            responses.POST,
            DEFAULT_URL + '/general/login',
            callback=login_callback,
            content_type='application/json'
        )

        responses.add_callback(
            responses.GET,
            DEFAULT_URL + '/actions/GetExecutionChannels',
            callback=get_execution_channels_callback,
            content_type='application/json'
        )

        client = Client('username', 'password')
        data = client.actions.get_execution_channels()
        self.assertEqual(data, {
            1: 'Silverpop',
            2: 'ExactTarget',
            3: 'Lobby Banner',
            4: 'Call Center',
        })

    @responses.activate
    def test_get_executed_campaign_channel_details(self):
        responses.add_callback(
            responses.POST,
            DEFAULT_URL + '/general/login',
            callback=login_callback,
            content_type='application/json'
        )

        responses.add_callback(
            responses.GET,
            DEFAULT_URL + '/actions/GetExecutedCampaignChannelDetails',
            callback=get_executed_campaign_channel_details_callback,
            content_type='application/json'
        )

        client = Client('username', 'password')
        data = client.actions.get_executed_campaign_channel_details(9214, 35)
        self.assertEqual(data, [{'campaign_id': 9214, 'channel_id': 35, 'list_id': 12,
                                'send_id': 'YTGF3C', 'template_id': 520, 'scheduled_time': '2015-12-30 08:00:00'},
                                {'campaign_id': 9214, 'channel_id': 35, 'send_id': '', 'template_id': 27,
                                 'scheduled_time': '2016-08-23 16:00:00'},
                                {'campaign_id': 9214, 'channel_id': 35, 'send_id': '', 'template_id': 1321,
                                 'scheduled_time': '2016-08-23 18:00:00'}])

    @responses.activate
    def test_get_executed_campaign_channel_details_empty_channel_id(self):
        responses.add_callback(
            responses.POST,
            DEFAULT_URL + '/general/login',
            callback=login_callback,
            content_type='application/json'
        )

        responses.add_callback(
            responses.GET,
            DEFAULT_URL + '/actions/GetExecutedCampaignChannelDetails',
            callback=get_executed_campaign_channel_details_callback,
            content_type='application/json'
        )

        client = Client('username', 'password')
        self.assertRaises(Exception, client.actions.get_executed_campaign_channel_details, 9214, None)

    @responses.activate
    def test_get_executed_campaign_channel_details_wrong_channel_id(self):
        responses.add_callback(
            responses.POST,
            DEFAULT_URL + '/general/login',
            callback=login_callback,
            content_type='application/json'
        )

        responses.add_callback(
            responses.GET,
            DEFAULT_URL + '/actions/GetExecutedCampaignChannelDetails',
            callback=get_executed_campaign_channel_details_callback,
            content_type='application/json'
        )

        client = Client('username', 'password')
        data = client.actions.get_executed_campaign_channel_details(9214, 34)
        self.assertFalse(data)

    @responses.activate
    def test_get_executed_campaigns_by_channel(self):
        responses.add_callback(
            responses.POST,
            DEFAULT_URL + '/general/login',
            callback=login_callback,
            content_type='application/json'
        )

        responses.add_callback(
            responses.GET,
            DEFAULT_URL + '/actions/GetExecutedCampaignsByChannel',
            callback=get_executed_campaigns_by_channel_callback,
            content_type='application/json'
        )

        client = Client('username', 'password')
        data = client.actions.get_executed_campaigns_by_channel(35, '2016-02-20')
        self.assertEqual(data, [12, 16, 17, 19])

    @responses.activate
    def test_get_executed_campaigns_by_channel_empty_date(self):
        responses.add_callback(
            responses.POST,
            DEFAULT_URL + '/general/login',
            callback=login_callback,
            content_type='application/json'
        )

        responses.add_callback(
            responses.GET,
            DEFAULT_URL + '/actions/GetExecutedCampaignsByChannel',
            callback=get_executed_campaigns_by_channel_callback,
            content_type='application/json'
        )

        client = Client('username', 'password')
        self.assertRaises(Exception, client.actions.get_executed_campaigns_by_channel, 35, None)

    @responses.activate
    def test_get_executed_campaigns_by_channel_wrong_date(self):
        responses.add_callback(
            responses.POST,
            DEFAULT_URL + '/general/login',
            callback=login_callback,
            content_type='application/json'
        )

        responses.add_callback(
            responses.GET,
            DEFAULT_URL + '/actions/GetExecutedCampaignsByChannel',
            callback=get_executed_campaigns_by_channel_callback,
            content_type='application/json'
        )

        client = Client('username', 'password')
        data = client.actions.get_executed_campaigns_by_channel(35, '3016-02-20')
        self.assertFalse(data)
