# -*- coding: utf-8 -*-
from __future__ import unicode_literals


from datetime import datetime, timedelta

from . import URLBuilder


class General(URLBuilder):
    client = None
    username = None
    password = None

    def __init__(self, client):
        self.client = client

    def login(self, username, password):
        """Returns the authentication token required for all other functions during a particular session"""
        if not username or not password:
            raise Exception('No credentials provided')

        self.username = username
        self.password = password

        data = {
            'Username': self.username,
            'Password': self.password
        }

        response = self.client.post(self._get_url(), data, check_token=False)
        self.client.token = response.json() if response else False
        self.client.expire = datetime.utcnow() if self.client.token else None
        return self.client.token

    def get_last_data_update(self):
        """Returns the date of the most recently available customer data"""
        response = self.client.get(self._get_url())
        return response.json()['Date'] if response else False
