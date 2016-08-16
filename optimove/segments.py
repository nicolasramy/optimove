# -*- coding: utf-8 -*-
from __future__ import unicode_literals


from . import URLBuilder


class Segments(URLBuilder):
    client = None

    def __init__(self, client):
        self.client = client

    def get_value_segment_name(self, segment_id):
        """Returns the value segment name associated with a particular value segment ID."""
        if not segment_id:
            raise Exception('No ValueSegmentID provided')

        data = {
            'ValueSegmentID': segment_id
        }

        response = self.client.get(self._get_url(), data)
        return response.json()['ValueSegmentName'] if response else False

    def get_value_segment_id(self, segment_name):
        """Returns the value segment ID associated with a particular value segment name."""
        if not segment_name:
            raise Exception('No ValueSegmentName provided')

        data = {
            'ValueSegmentName': segment_name
        }

        response = self.client.get(self._get_url(), data)
        return response.json()['ValueSegmentID'] if response else False

    def get_value_segments(self):
        """Returns all defined value segment names and IDs."""
        response = self.client.get(self._get_url())

        results = {}
        for item in response.json():
            results[item['ValueSegmentID']] = item['ValueSegmentName']

        return results

    def get_customers_by_value_segment(self, segment_id, date, attributes=None, delimiter=';'):
        """Returns the list of customer IDs associated with a particular value segment on a particular date."""
        if not segment_id or not date:
            raise Exception('No ValueSegmentID and Date provided')

        data = {
            'ValueSegmentID': segment_id,
            'Date': date
        }

        if attributes and type(attributes) == list:
            data['CustomerAttributes'] = ';'.join(attributes)

            if delimiter:
                if delimiter in self.AUTHORIZED_DELIMITERS and delimiter not in self.UNAUTHORIZED_DELIMITERS:
                    data['CustomerAttributesDelimiter'] = delimiter
                else:
                    raise Exception('Invalid delimiter')

        response = self.client.get(self._get_url(), data)
        if not response:
            return False

        if attributes and type(attributes) == list:
            results = {}
            for item in response.json():
                results[item['CustomerID']] = {}
                customer_attributes = item['CustomerAttributes'].split(delimiter)
                for index, attribute in enumerate(attributes):
                    results[item['CustomerID']][attribute] = customer_attributes[index]

        else:
            results = [item['CustomerID'] for item in response.json()]

        return results

    def get_value_segment_changers(self, start_date, end_date, attributes=None, delimiter=';'):
        """Returns all customer IDs in the database which changed value segments during a particular date range, along
        with their before and after value segment IDs."""
        if not start_date or not end_date:
            raise Exception('No StartDate and EndDate provided')

        data = {
            'StartDate': start_date,
            'EndDate': end_date
        }

        if attributes and type(attributes) == list:
            data['CustomerAttributes'] = ';'.join(attributes)

            if delimiter:
                if delimiter in self.AUTHORIZED_DELIMITERS and delimiter not in self.UNAUTHORIZED_DELIMITERS:
                    data['CustomerAttributesDelimiter'] = delimiter
                else:
                    raise Exception('Invalid delimiter')

        response = self.client.get(self._get_url(), data)
        if not response:
            return False

        results = []
        for item in response.json():
            result = {
                'customer_id': item['CustomerID'],
                'initial_value_segment': item['InitialValueSegmentID'],
                'final_value_segment': item['FinalValueSegmentID']
            }
            if attributes and type(attributes) == list:
                result['attributes'] = {}
                customer_attributes = item['CustomerAttributes'].split(delimiter)
                for index, attribute in enumerate(attributes):
                    result['attributes'][attribute] = customer_attributes[index]
            results.append(result)

        return results
