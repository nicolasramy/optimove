# -*- coding: utf-8 -*-
from __future__ import unicode_literals


from . import URLBuilder


class Model(URLBuilder):
    client = None

    def __init__(self, client):
        self.client = client

    def get_customer_attribute_list(self):
        response = self.client.get(self._get_url())
        if not response:
            return None

        results = {}
        for item in response.json():
            results[item['RealFieldName']] = item['Description']

        return results

    def get_lifecycle_stage_list(self):
        response = self.client.get(self._get_url())
        if not response:
            return None

        results = {}
        for item in response.json():
            results[item['StageId']] = item['StageName']

        return results
