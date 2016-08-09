# -*- coding: utf-8 -*-
from __future__ import unicode_literals


from datetime import datetime, timedelta

import requests

from general import General
from model import Model
from segments import Segments


class Client:

    token = None
    expire = None

    def __init__(self, username=None, password=None):
        self.general = General(self)
        self.model = Model(self)
        self.segments = Segments(self)

        if username and password:
            self.general.login(username, password)

    def _headers(self):
        headers = {
            'Accept': 'application/JSON',
            'Content-type': 'application/JSON'
        }

        if self.token:
            headers['Authorization-Token'] = self.token

        return headers

    def refresh_token(self):
        if (self.expire - datetime.utcnow()).seconds >= 20 * 60:
            self.general.login(self.general.username, self.general.password)
        return

    def get(self, url, payload=None, headers=None):
        self.refresh_token()

        headers = headers if headers else self._headers()
        response = requests.get(url, params=payload, headers=headers)

        return response if response.status_code == requests.codes.ok else False

    def post(self, url, payload=None, headers=None):
        self.refresh_token()

        headers = headers if headers else self._headers()
        response = requests.post(url, payload, headers)

        return response if response.status_code == requests.codes.ok else False

    def bad_request(self):
        pass

    def unauthorized(self):
        pass

    def method_not_allowed(self):
        pass

    def internal_server_error(self):
        pass
