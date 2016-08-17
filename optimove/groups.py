# -*- coding: utf-8 -*-
from __future__ import unicode_literals


from . import URLBuilder


class Groups(URLBuilder):
    client = None

    def __init__(self, client):
        self.client = client

    def get_target_group_name(self, target_group_id):
        """Returns the target group name associated with a particular target group ID."""
        if not target_group_id:
            raise Exception('No TargetGroupID provided')

        data = {
            'TargetGroupID': target_group_id
        }

        response = self.client.get(self._get_url(), data)
        return response.json()['TargetGroupName'] if response else False

    def get_target_group_id(self, target_group_name):
        """Returns the target group ID associated with a particular target group name."""
        if not target_group_name:
            raise Exception('No TargetGroupName provided')

        data = {
            'TargetGroupName': target_group_name
        }

        response = self.client.get(self._get_url(), data)
        return response.json()['TargetGroupID'] if response else False

    def get_target_groups_by_date(self, date):
        """Returns the list of target group IDs for which an acion was executed on a particular date."""
        if not date:
            raise Exception('No Date provided')

        data = {
            'Date': date
        }

        response = self.client.get(self._get_url(), data)
        return [item['TargetGroupID'] for item in response.json()] if response else False

    def get_target_group_details(self):
        """Returns an array of IDs, names and priorities for all defined target groups."""
        response = self.client.get(self._get_url())

        results = {}
        for item in response.json():
            results[item['TargetGroupID']] = {
                'name': item['TargetGroupName'],
                'priority': item['TargetGroupPriority']
            }

        return results
