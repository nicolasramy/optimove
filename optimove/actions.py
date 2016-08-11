# -*- coding: utf-8 -*-
from __future__ import unicode_literals


from . import URLBuilder


class Actions(URLBuilder):
    client = None

    def __init__(self, client):
        self.client = client

    def get_action_name(self, action_id):
        """Returns the action name associated with a particular action ID"""
        if not action_id:
            raise Exception('No ActionID provided')

        data = {
            'ActionID': action_id
        }

        response = self.client.get(self._get_url(), data)
        return response.json()['ActionName'] if response else False

    def get_action_id(self, action_name):
        """Returns the action ID associated with a particular action name."""
        if not action_name:
            raise Exception('No ActionName provided')

        data = {
            'ActionName': action_name
        }

        response = self.client.get(self._get_url(), data)
        return response.json()['ActionID'] if response else False

    def get_all_actions(self):
        """Returns all defined action IDs and corresponding action names."""
        response = self.client.get(self._get_url())

        results = {}
        for item in response.json():
            results[item['ActionID']] = item['ActionName']

        return results

    def get_actions_by_target_group(self, target_group_id, date):
        """Returns all the recipient group IDs and action IDs associated with a particular target group on
        a particular date."""
        if not target_group_id or not date:
            raise Exception('No TargetGroupID or Date provided')

        data = {
            'TargetGroupID': target_group_id,
            'Date': date
        }

        response = self.client.get(self._get_url(), data)
        if not response:
            return False

        results = {}
        for item in response.json():
            results[item['RecipientGroupID']] = item['ActionID']

        return results

    def get_promo_codes(self, date):
        """Returns all target group IDs, action IDs and promo codes for a particular date."""
        if not date:
            raise Exception('No Date provided')

        data = {
            'Date': date
        }

        response = self.client.get(self._get_url(), data)
        if not response:
            return False

        results = [{
                'target_group_id': item['TargetGroupID'],
                'recipient_group_id': item['RecipientGroupID'],
                'action_id': item['ActionID'],
                'promo_code': item['PromoCode']
            } for item in response.json()]

        return results

    def get_promo_codes_by_campaign(self, campaign_id):
        """Returns the recipient group IDs, action IDs and promo codes for a particular campaign ID."""
        if not campaign_id:
            raise Exception('No CampaignID provided')

        data = {
            'CampaignID': campaign_id
        }

        response = self.client.get(self._get_url(), data)
        if not response:
            return False

        results = [{
                'campaign_id': campaign_id,
                'recipient_group_id': item['RecipientGroupID'],
                'action_id': item['ActionID'],
                'promo_code': item['PromoCode']
            } for item in response.json()]

        return results

    def get_promo_codes_by_target_group(self, target_group_id, date):
        """Returns all recipient group IDs, action IDs and promo codes associated with a given target group on a
        particular date."""
        if not target_group_id or not date:
            raise Exception('No TargetGroupID or Date provided')

        data = {
            'TargetGroupID': target_group_id,
            'Date': date
        }

        response = self.client.get(self._get_url(), data)
        if not response:
            return False

        results = [{
                'target_group_id': target_group_id,
                'recipient_group_id': item['RecipientGroupID'],
                'action_id': item['ActionID'],
                'promo_code': item['PromoCode']
            } for item in response.json()]

        return results

    def get_action_details_by_target_group(self, target_group_id, date):
        """Returns the action IDs, action duration (in days), lead time (in days) and the execution channels associated
        with a given target group on a particular date."""
        if not target_group_id or not date:
            raise Exception('No TargetGroupID or Date provided')

        data = {
            'TargetGroupID': target_group_id,
            'Date': date
        }

        response = self.client.get(self._get_url(), data)
        if not response:
            return False

        results = [{
                'target_group_id': target_group_id,
                'recipient_group_id': item['RecipientGroupID'],
                'action_id': item['ActionID'],
                'duration': item['Duration'],
                'lead_time': item['LeadTime'],
                'channel_id': item['ChannelID']
            } for item in response.json()]

        return results

    def get_executed_campaign_details(self, date):
        """Returns details of every campaign executed on a particular date."""
        if not date:
            raise Exception('No Date provided')

        data = {
            'Date': date
        }

        response = self.client.get(self._get_url(), data)
        if not response:
            return False

        results = {}
        for item in response.json():
            results[item['CampaignID']] = {
                'target_group_id': item['TargetGroupID'],
                'campaign_type': item['CampaignType'],
                'duration': item['Duration'],
                'lead_time': item['LeadTime'],
                'notes': item['Notes'],
                'is_multi_channel': item['IsMultiChannel'] == 'true',
                'is_recurrence': item['IsRecurrence'] == 'true',
                'status': item['Status'],
                'error': item['Error'],
            }

        return results

    def get_campaign_details(self, campaign_id):
        """Returns details of a particular campaign."""
        if not campaign_id:
            raise Exception('No Date provided')

        data = {
            'CampaignID': campaign_id
        }

        response = self.client.get(self._get_url(), data)
        if not response:
            return False

        item = response.json()
        return {
            'campaign_id': campaign_id,
            'target_group_id': item['TargetGroupID'],
            'campaign_type': item['CampaignType'],
            'duration': item['Duration'],
            'lead_time': item['LeadTime'],
            'notes': item['Notes'],
            'is_multi_channel': item['IsMultiChannel'] == 'true',
            'is_recurrence': item['IsRecurrence'] == 'true',
            'status': item['Status'],
            'error': item['Error'],
        }

    def get_execution_channels(self):
        """Returns all available execution channels."""
        response = self.client.get(self._get_url())

        results = {}
        for item in response.json():
            results[item['ChannelID']] = item['ChannelName']
        return results

    def get_executed_campaign_channel_details(self, campaign_id, channel_id):
        """Returns the details of a particular channel used in a particular executed campaign."""
        if not campaign_id or not channel_id:
            raise Exception('No CampaignID or ChannelID provided')

        data = {
            'CampaignID': campaign_id,
            'ChannelID': channel_id
        }

        response = self.client.get(self._get_url(), data)
        if not response:
            return False

        item = response.json()[0]
        return {
            'campaign_id': campaign_id,
            'channel_id': channel_id,
            'list_id': item['ListID'],
            'send_id': item['SendID'],
            'template_id': item['TemplateID'],
            'scheduled_time': item['ScheduledTime']
        }

    def get_executed_campaigns_by_channel(self, channel_id, date):
        """Returns the list of campaigns executed for a particular channel on a particular date."""
        if not channel_id or not date:
            raise Exception('No ChannelID or Date provided')

        data = {
            'ChannelID': channel_id,
            'Date': date
        }

        response = self.client.get(self._get_url(), data)
        return [item['CampaignID'] for item in response.json()] if response else False
