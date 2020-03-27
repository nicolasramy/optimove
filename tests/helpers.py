# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

import json

from tests.constants import TOKEN, HEADERS


def login_callback(request):
    payload = json.loads(request.body)
    if payload['Username'] == 'username' and payload['Password'] == 'password':
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
