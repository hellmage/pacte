# Copyright (c) 2017 App Annie Inc. All rights reserved.
import importlib
import logging
import re
import string

import json
from pacte.utils.json import datetime_decoder

DEFAULT_CONTENT_TYPE = 'text/html'
logger = logging.getLogger(__name__)


def _description_to_test_class_name(desc):
    return string.capwords(
        re.sub(r'[^0-9A-Za-z\-_ ]', '', desc).replace('-', ' ').replace('_', ' ').strip()
    ).replace(' ', '')


def http_case_factory(app, state_cls, interaction, consumer_name):

    class ProviderTest(state_cls):
        maxDiff = None

        @staticmethod
        def _import_application(app_ref):
            module_name, attr_name = app_ref.rsplit('.', 1)
            py = importlib.import_module(module_name)
            return getattr(py, attr_name)

        def _compare_headers(self, expected_headers, resp_headers):
            normalized_headers = {k.lower(): v for k, v in resp_headers}
            for key, val in expected_headers.items():
                key = key.lower()
                if key not in normalized_headers or normalized_headers[key] != val:
                    raise self.failureException('Bad header: %s=%s' % (key, val))

        def runTest(self):
            logger.info('Run test from consumer %s (%s)', consumer_name, interaction.description)
            request = interaction.request
            response = interaction.response
            app_instance = self._import_application(app)
            app_instance.testing = True
            client = app_instance.test_client()
            method = request['method'].lower()
            if method == 'get':
                path = request['path']
                if request.get('query'):
                    path += '?' + request['query']
                resp = client.get(path, headers=request.get('headers'))
            elif method == 'post':
                headers = request.get('headers', {})
                content_type = headers.get('content-type') or headers.get('Content-Type') or 'plain/text'
                body = request['body']
                if content_type == 'application/json':
                    body = json.dumps(body)
                resp = client.post(request['path'], data=body, headers=headers, content_type=content_type)
            else:
                raise self.failureException('Unsupported http method: %s' % method)
            self.assertEqual(response['status'], resp.status_code)
            self._compare_headers(response.get('headers', {}), resp.headers)
            body = resp.get_data()
            content_type = resp.headers.get('Content-Type') or DEFAULT_CONTENT_TYPE
            if ';' in content_type:
                content_type = content_type.split(';', 1)[0]
            if content_type == 'application/json':
                body = json.loads(body, object_pairs_hook=datetime_decoder)
            elif content_type not in (DEFAULT_CONTENT_TYPE, 'text/plain'):
                raise self.failureException('Unsupported content type: %s' % content_type)
            if isinstance(body, dict):
                self.assertDictEqual(response['body'], body)
            else:
                self.assertEqual(response['body'], body.decode('UTF-8'))

    ProviderTest.__name__ = _description_to_test_class_name(interaction.description) + 'HTTPTest'
    return ProviderTest
