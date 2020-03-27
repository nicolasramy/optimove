# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from datetime import datetime
from six.moves.urllib.parse import quote_plus


class General(object):
    client = None
    username = None
    password = None

    EVENT_TYPE_CAMPAIGN_PROCESSED = 1
    EVENT_TYPE_TODAY_CAMPAIGNS_HAS_BEEN_PROCESSED = 2
    EVENT_TYPE_DAILY_DATA_UPDATE_COMPLETED = 3
    EVENT_TYPE_CAMPAIGN_CANCELED = 4

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
        url = self.client.get_url()
        response = self.client.post(url, data, check_token=False)
        self.client.token = response.json() if response else False
        self.client.expire = datetime.utcnow() if self.client.token else None
        return self.client.token

    def get_last_data_update(self):
        """Returns the date of the most recently available customer data"""
        response = self.client.get(self.client.get_url())
        return response.json()['Date'] if response else False

    def register_event_listener(self, event_type_id, listener_url):
        """Specifies the URL of a listener to which Optimove will report events of the specified type (e.g., “campaign
        scheduled”)."""
        if not event_type_id or not listener_url:
            raise Exception('No EventTypeID and ListenerURL provided')

        data = {
            'EventTypeID': event_type_id,
            'ListenerURL': quote_plus(listener_url)
        }

        response = self.client.post(self.client.get_url(), data)
        return bool(response)

    def unregister_event_listener(self, event_type_id):
        """Instructs Optimove to stop reporting events of the specified event type
        to a previously-registered listener."""
        if not event_type_id:
            raise Exception('No EventTypeID provided')

        data = {
            'EventTypeID': event_type_id
        }

        response = self.client.post(self.client.get_url(), data)
        return bool(response)
