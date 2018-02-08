# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from datetime import datetime
from inspect import currentframe, getouterframes
import json
import logging

import requests

from constants import DEFAULT_URL, TIMEOUT
from general import General
from model import Model
from actions import Actions
from groups import Groups
from customers import Customers
from segments import Segments
from integrations import Integrations


LOGGER = logging.getLogger(__name__)


class Client:
    token = None
    expire = None

    def __init__(self, username=None, password=None, timeout=TIMEOUT, url=DEFAULT_URL):
        self.general = General(self)
        self.model = Model(self)
        self.actions = Actions(self)
        self.groups = Groups(self)
        self.customers = Customers(self)
        self.segments = Segments(self)
        self.integrations = Integrations(self)
        self.timeout = timeout
        self._url = url

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

    def _refresh_token(self):
        if not self.expire or (self.expire - datetime.utcnow()).seconds >= 1200:
            self.general.login(self.general.username, self.general.password)
        return

    def get(self, url, payload=None, headers=None, check_token=True):
        if check_token:
            self._refresh_token()

        headers = headers if headers else self._headers()
        LOGGER.debug("GET request: url=%s, payload=%s, headers=%s", url, payload, headers)

        try:
            response = requests.get(url, params=payload, headers=headers, timeout=self.timeout)
        except requests.exceptions.Timeout as error:
            LOGGER.error("Timeout reached, error=%s", error)
            raise Exception('Timeout reached {}sec, url is {}'.format(self.timeout, url))

        LOGGER.debug("GET response: url=%s, response_data=%s", url, response.text)
        return self.dispatch_response(response)

    def post(self, url, payload=None, headers=None, check_token=True):
        if check_token:
            self._refresh_token()

        headers = headers if headers else self._headers()
        data = json.dumps(payload)
        LOGGER.debug("POST request: url=%s, data=%s, headers=%s", url, payload, headers)

        try:
            response = requests.post(url, data=data, headers=headers, timeout=self.timeout)
        except requests.exceptions.Timeout as error:
            LOGGER.error("Timeout reached, error=%s", error)
            raise Exception('Timeout reached {}sec, url is {}'.format(self.timeout, url))

        LOGGER.debug("POST response: url=%s, response_data=%s", url, response.text)
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

    def get_url(self):
        outer_frames = getouterframes(currentframe(), 2)[1]
        category_name = outer_frames[1].split('/')[-1].split('.')[0]
        method_name = outer_frames[3]
        if '_' in method_name:
            action_name_list = [part.upper() if part == 'id' else part.capitalize() for part in method_name.split('_')]
            action_name = ''.join(action_name_list)
        else:
            action_name = method_name
        return '%s/%s/%s' % (self._url, category_name, action_name)
