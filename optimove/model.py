# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from constants import AUTHORIZED_DELIMITERS, UNAUTHORIZED_DELIMITERS


class Model(object):
    client = None

    def __init__(self, client):
        self.client = client

    def get_customer_attribute_list(self):
        """Returns all the available customer attribute names (which can be passed to certain other functions
        as an input parameter) and a description of each."""
        response = self.client.get(self.client.get_url())

        results = {}
        for item in response.json():
            results[item['RealFieldName']] = item['Description']

        return results

    def get_lifecycle_stage_list(self):
        """Returns all available lifecycle stages (for use in other functions, e.g., GetCustomerFutureValues)."""
        response = self.client.get(self.client.get_url())

        results = {}
        for item in response.json():
            results[item['StageID']] = item['StageName']

        return results

    def get_microsegment_list(self):
        """Returns an dict containing the details of all microsegments."""
        response = self.client.get(self.client.get_url())

        results = {}
        for item in response.json():
            results[item['MicrosegmentID']] = {
                'name': item['MicrosegmentName'],
                'stage_id': item['LifecycleStageID'],
                'future_value': item['FutureValue'],
                'churn_rate': item['ChurnRate'],
            }

        return results

    def get_microsegment_changers(self, start, end, attributes=None, delimiter=';'):
        """Returns an array of customer IDs, and their before and after micro-segment IDs,
        for customers whose micro-segment changed during a particular date range."""
        if not start or not end:
            raise Exception('No StartDate and EndDate provided')

        data = {
            'StartDate': start,
            'EndDate': end
        }

        if attributes and type(attributes) == list:
            data['CustomerAttributes'] = ';'.join(attributes)

            if delimiter:
                if delimiter in AUTHORIZED_DELIMITERS and delimiter not in UNAUTHORIZED_DELIMITERS:
                    data['CustomerAttributesDelimiter'] = delimiter
                else:
                    raise Exception('Invalid delimiter')

        response = self.client.get(self.client.get_url(), data)
        if not response:
            return False

        results = list()
        for item in response.json():
            result = {
                'customer_id': item['CustomerID'],
                'initial': item['InitialMicrosegmentID'],
                'final': item['FinalMicrosegmentID']
            }
            if attributes and type(attributes) == list:
                result['attributes'] = {
                    key: value for key, value in zip(attributes, item['CustomerAttributes'])
                }
            results.append(result)

        return results
