# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import traceback

import requests

from general import General

__all__ = ['Client']


class Client:

    token = None

    def __init__(self, username=None, password=None):
        self.general = General(self)

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

    def get(self, url, payload=None, headers=None):
        headers = headers if headers else self._headers()
        response = requests.get(url, params=payload, headers=headers)

        return response if response.status_code == requests.codes.ok else False

    def post(self, url, payload=None, headers=None):
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
