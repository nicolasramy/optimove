# -*- coding: utf-8 -*-
from __future__ import unicode_literals


from . import URLBuilder


class General(URLBuilder):
    client = None

    def __init__(self, client):
        self.client = client

    def login(self, username, password):
        """Returns the authentication token required for all other functions during a particular session"""
        if not username or not password:
            raise Exception('No credentials provide')

        data = {
            'Username': username,
            'Password': password
        }
        response = self.client.post(self._get_url(), data)
        self.client.token = response.json() if response else False
        return self.client.token

    def get_last_data_update(self):
        """Returns the date of the most recently available customer data"""
        response = self.client.get(self._get_url())
        return response.json() if response else False
