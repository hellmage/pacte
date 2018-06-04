# Copyright (c) 2017 App Annie Inc. All rights reserved.
import json
import logging
try:
    from urlparse import urlunsplit  # py2
except:
    from urllib.parse import urlunsplit  # py3

import requests_mock
from six import string_types

from pacte.exceptions import PacteServiceException

logger = logging.getLogger(__name__)


class MockAPI(object):

    def __init__(self, contract, scheme='http', domain='localhost', port=80):
        self.port = port
        self.stopped = True
        self.scheme = scheme
        self.contract = contract
        if self.scheme.upper() == 'HTTP' and port == 80:
            self.netloc = domain
        elif self.scheme.upper() == 'HTTPS' and port == 443:
            self.netloc = domain
        else:
            self.netloc = '{}:{}'.format(domain, port)

    def mock(self, mocker):
        for interaction in self.contract.interactions:
            method = {
                "GET": mocker.get,
                "POST": mocker.post,
            }.get(interaction.request["method"].upper())
            path = interaction.request["path"]
            query = interaction.request.get('query')
            uri = urlunsplit((self.scheme, self.netloc, path, query, None))
            body = interaction.response.get('body')
            if isinstance(body, dict) or isinstance(body, list):
                body_str = json.dumps(body)
            elif isinstance(body, string_types):
                body_str = body
            else:
                raise PacteServiceException("body provide unsupported format")
            method(uri, content=body_str.encode('utf-8'), headers=interaction.response.get('headers', {}))

    def get_service_host(self):
        return "{}://{}".format(self.scheme, self.netloc)


class MockServices(object):
    """
    Interface to interact with pact mock server.
    """

    def __init__(self, mock_apis):
        """
        :param mock_apis: one or a list of MockAPI objects
        """
        if not isinstance(mock_apis, list):
            mock_apis = [mock_apis]
        self.mock_apis = mock_apis
        self.m = requests_mock.mock()
        self.stopped = True

    def start(self):
        """
        Start the mock service, loading the interactions into the pact server.
        """
        if not self.stopped:
            raise PacteServiceException(
                "Cannot start already started MockService.")

        for mock_api in self.mock_apis:
            mock_api.mock(self.m)
        self.m.start()
        self.stopped = False

    def end(self):
        """
        End the mock service, verifing the interactions with the pact server.
        """
        if self.stopped:
            raise PacteServiceException(
                    "Cannot end already ended MockService.")

        self.m.stop()
        self.stopped = True

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, type, value, traceback):
        self.end()
