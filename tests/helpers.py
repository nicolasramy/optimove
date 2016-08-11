# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
from urlparse import parse_qs

from constants import TOKEN, HEADERS


def login_callback(request):
    payload = parse_qs(request.body)
    if payload['Username'][0] == 'username' and payload['Password'][0] == 'password':
        resp_body = TOKEN
        return 200, HEADERS['json'], json.dumps(resp_body)

    else:
        return 401, HEADERS['text'], 'Wrong user / password combination'


def token_required(funcname):
    def token_required_wrapper(*args, **kwargs):
        if 'Authorization-Token' not in args[0].headers:
            return 401, HEADERS['text'], 'Missing Authorization-Token'

        if args[0].headers['Authorization-Token'] != TOKEN:
            return 403, HEADERS['text'], 'Unauthorized User'

        return funcname(*args, **kwargs)

    return token_required_wrapper
