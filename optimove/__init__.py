# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from inspect import currentframe, getouterframes

__version__ = "0.0.0"


class URLBuilder(object):

    API_BASE_URL = 'https://api.optimove.net/'
    API_VERSION = 'v3.0'

    def _get_url(self):
        method_name = getouterframes(currentframe(), 2)[1][3]

        if '_' in method_name:
            method_name_splitted = method_name.split('_')
            action_name_list = [method_name_splitted[0].lower(), ]
            action_name_list += [part.capitalize() for part in method_name_splitted[1:]]
            action_name = ''.join(action_name_list)

        else:
            action_name = method_name

        return '%s/%s/%s/%s' % (self.API_BASE_URL, self.API_VERSION, self.__class__.__name__.lower(), action_name)