# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from . import constants


class Integrations(object):
    client = None

    METRIC_SENT = 0
    METRIC_DELIVERED = 1
    METRIC_OPENED = 2
    METRIC_CLICKED = 3
    METRIC_UNSUBSCRIBED = 4

    def __init__(self, client):
        self.client = client

    def add_promotions(self, promotions):
        """Adds promo codes and associated names that will be available for selection when running a campaign."""
        if not promotions:
            raise Exception('No PromoCode and PromotionName provided')

        if len(promotions) > 100:
            raise Exception('Too much PromoCode and PromotionName provided')

        data = [{
            'PromoCode': item,
            'PromotionName': promotions[item]
        } for item in promotions]

        response = self.client.post(self.client.get_url(), data)
        return bool(response)

    def get_promotions(self):
        """Returns an array of all defined promo codes and associated names."""
        response = self.client.get(self.client.get_url())

        results = {}
        for item in response.json():
            results[item['PromoCode']] = item['PromotionName']

        return results

    def delete_promotions(self, promotions):
        """Removes previously-added promo codes."""
        if not promotions:
            raise Exception('No PromoCode provided')

        if len(promotions) > 100:
            raise Exception('Too much PromoCode provided')

        data = [
            {
                'PromoCode': item
            } for item in promotions
        ]

        response = self.client.post(self.client.get_url(), data)
        return bool(response)

    def add_channel_templates(self, channel_id, templates):
        """Adds template IDs and associated names that will be associated with a specified channel ID."""
        if not channel_id or not templates:
            raise Exception('No ChannelID, TemplateID and TemplateName provided')

        if len(templates) > 100:
            raise Exception('Too much TemplateID and TemplatesName provided')

        data = list()
        for item in templates:
            _data = {
                'TemplateID': item['id'],
                'TemplateName': item['name']
            }
            if 'app_id' in item:
                _data['AppID'] = item['app_id']

            data.append(_data)

        url = '%s?ChannelID=%d' % (self.client.get_url(), channel_id)
        response = self.client.post(url, data)
        return bool(response)

    def get_channel_templates(self, channel_id):
        """Returns an array of template IDs and associated names for a particular channel."""
        if not channel_id:
            raise Exception('No ChannelID provided')

        data = {
            'ChannelID': channel_id
        }

        response = self.client.get(self.client.get_url(), data)
        if not response:
            return False

        results = {}
        for item in response.json():
            results[item['TemplateID']] = item['TemplateName']

        return results

    def delete_channel_templates(self, templates):
        """Removes previously-added channel templates."""
        if not templates:
            raise Exception('No ChannelID and TemplateID provided')

        if len(templates) > 100:
            raise Exception('Too much ChannelID and TemplateID provided, max 100')

        data = [
            {
                'ChannelID': item['channel_id'],
                'TemplateID': item['template_id']
            } for item in templates
        ]

        response = self.client.post(self.client.get_url(), data)
        return bool(response)

    def add_channel_apps(self, channel_id, applications):
        """Adds app IDs and associated names that will be available for selection when running a campaign via the
        specified channel (typically required when using push notification channels)."""
        if not channel_id or not applications:
            raise Exception('No ChannelID, AppID and AppName provided')

        if len(applications) > 100:
            raise Exception('Too much AppID and AppName provided, max 100')

        data = [
            {
                'AppID': item,
                'AppName': applications[item]
            } for item in applications
        ]

        url = '%s?ChannelID=%d' % (self.client.get_url(), channel_id)
        response = self.client.post(url, data)
        return bool(response)

    def delete_channel_apps(self, applications):
        """Removes previously-added apps."""
        if not applications:
            raise Exception('No ChannelID and AppID provided')

        if len(applications) > 100:
            raise Exception('Too much ChannelID and AppID provided')

        data = [
            {
                'ChannelID': item['channel_id'],
                'AppID': item['app_id']
            } for item in applications
        ]

        response = self.client.post(self.client.get_url(), data)
        return bool(response)

    def update_campaign_metrics(self, metrics):
        if not metrics:
            raise Exception('No ChannelID, CampaignID, TemplateID, MetricID and MetricValue provided')

        if len(metrics) > 100:
            raise Exception('Too much ChannelID, CampaignID, TemplateID, MetricID and MetricValue provided')

        data = [{
            'ChannelID': item['channel_id'],
            'CampaignID': item['campaign_id'],
            'TemplateID': item['template_id'],
            'MetricID': item['metric'],
            'MetricValue': item['value']
        } for item in metrics]

        response = self.client.post(self.client.get_url(), data)
        return bool(response)

