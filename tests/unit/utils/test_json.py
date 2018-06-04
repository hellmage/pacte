# Copyright (c) 2017 App Annie Inc. All rights reserved.
import unittest as ut

import datetime
import simplejson as json
from pacte.utils.json import DateTimeEncoder, datetime_decoder


class JsonDatetimeTest(ut.TestCase):

    def test_datetime_encoder(self):
        self.assertEqual(
            '{"d": "2018-01-11"}',
            json.dumps({'d': datetime.date(2018, 1, 11)}, cls=DateTimeEncoder)
        )
        self.assertEqual(
            '{"dt": "2018-01-11T17:08:25"}',
            json.dumps({'dt': datetime.datetime(2018, 1, 11, 17, 8, 25)}, cls=DateTimeEncoder)
        )
        self.assertEqual(
            '{"dts": "2018-01-11T17:08:25.188424"}',
            json.dumps({'dts': datetime.datetime(2018, 1, 11, 17, 8, 25, 188424)}, cls=DateTimeEncoder)
        )
        self.assertEqual(
            '["2018-01-01"]',
            json.dumps([datetime.date(2018, 1, 1)], cls=DateTimeEncoder)
        )

    def test_datetime_decoder(self):
        self.assertDictEqual(
            {
                'a': 1,
                'datetime': {
                    'd': datetime.date(2018, 1, 11),
                    'dt': datetime.datetime(2018, 1, 11, 17, 8, 25),
                    'dts': datetime.datetime(2018, 1, 11, 17, 8, 25, 188424),
                },
                's': 'hello'
            },
            json.loads(
                '{"a": 1, "s": "hello", "datetime": {"dts": "2018-01-11T17:08:25.188424", '
                '"dt": "2018-01-11T17:08:25", "d": "2018-01-11"}}',
                object_pairs_hook=datetime_decoder
            )
        )
        self.assertEqual(
            ['2018-01-01'],  # not able to deserialize to [datetime.date(2018, 1, 1)]
            json.loads('["2018-01-01"]', object_pairs_hook=datetime_decoder)
        )
