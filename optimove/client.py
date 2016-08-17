# -*- coding: utf-8 -*-
from __future__ import unicode_literals


from datetime import datetime, timedelta
import json

import requests

from general import General
from model import Model
from actions import Actions
from groups import Groups
from customers import Customers
from segments import Segments
from integrations import Integrations


class Client:
    token = None
    expire = None

    def __init__(self, username=None, password=None):
        self.general = General(self)
        self.model = Model(self)
        self.actions = Actions(self)
        self.groups = Groups(self)
        self.customers = Customers(self)
        self.segments = Segments(self)
        self.integrations = Integrations(self)

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
        if not self.expire or (self.expire - datetime.utcnow()).seconds >= 1200:
            self.general.login(self.general.username, self.general.password)
        return

    def get(self, url, payload=None, headers=None, check_token=True):
        if check_token:
            self.refresh_token()

        headers = headers if headers else self._headers()
        response = requests.get(url, params=payload, headers=headers)
        return self.dispatch_response(response)

    def post(self, url, payload=None, headers=None, check_token=True):
        if check_token:
            self.refresh_token()

        headers = headers if headers else self._headers()
        response = requests.post(url, data=json.dumps(payload), headers=headers)
        return self.dispatch_response(response)

    @staticmethod
    def bad_request():
        raise Exception('Bad Request')

    @staticmethod
    def unauthorized():
        raise Exception('Unauthorized')

    @staticmethod
    def method_not_allowed():
        raise Exception('Method Not allowed')

    @staticmethod
    def internal_server_error():
        raise Exception('Internal Server error')

    def dispatch_response(self, response):
        if response.status_code == 200:
            return response
        elif response.status_code == 400:
            return self.bad_request()
        elif response.status_code == 401:
            return self.unauthorized()
        elif response.status_code == 405:
            return self.method_not_allowed()
        elif response.status_code == 500:
            return self.internal_server_error()
        else:
            return False
