# Copyright (c) 2017 App Annie Inc. All rights reserved.
import datetime

import simplejson as json
from six import string_types

DATE_ISO_FORMAT = '%Y-%m-%d'
DATETIME_WITH_MILLISECOND_ISO_FORMAT = '%Y-%m-%dT%H:%M:%S.%f'
DATETIME_WITHOUT_MILLISECOND_ISO_FORMAT = '%Y-%m-%dT%H:%M:%S'


class DateTimeEncoder(json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj, datetime.datetime) or isinstance(obj, datetime.date):
            return obj.isoformat()
        return super(DateTimeEncoder, self).default(obj)


def datetime_decoder(pairs):
    d = {}
    for k, v in pairs:
        if isinstance(v, string_types):
            try:
                d[k] = datetime.datetime.strptime(v, DATE_ISO_FORMAT).date()
            except ValueError:
                try:
                    d[k] = datetime.datetime.strptime(v, DATETIME_WITH_MILLISECOND_ISO_FORMAT)
                except ValueError:
                    try:
                        d[k] = datetime.datetime.strptime(v, DATETIME_WITHOUT_MILLISECOND_ISO_FORMAT)
                    except ValueError:
                        d[k] = v
        else:
            d[k] = v
    return d
