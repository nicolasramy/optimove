# -*- coding: utf-8 -*-
from __future__ import unicode_literals


from . import URLBuilder


class General(URLBuilder):
    client = None

    def __init__(self, client):
        self.client = client

    def login(self, username, password):
        data = {
            'Username': username,
            'Password': password
        }
        response = self.client.post(self._get_url(), data)
        self.client.token = response.json() if response else None
        return self.client.token

    def get_last_data_update(self):
        response = self.client.get(self._get_url())
        return response.json() if response else None
