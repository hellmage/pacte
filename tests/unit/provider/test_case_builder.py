# Copyright (c) 2017 App Annie Inc. All rights reserved.

from unittest import TestCase

import nose

from pacte.case_builder import http_case_factory
from pacte.interaction import Interaction


class State(TestCase):
    pass


class CaseBuilderTest(TestCase):

    def test_http_testcase_builder(self):
        interaction = Interaction.from_dict({
            "providerState": "World is good",
            "description": "a hello to the world",
            "request": {
                "method": "GET",
                "path": "/",
            },
            "response": {
                "status": 200,
                "body": "Hello, World!",
                "headers": {
                    'Content-Type': 'text/html; charset=utf-8',
                    'Content-Length': '13'
                }
            }
        })
        testcase_cls = http_case_factory('tests.unit.provider.mini_app.app', State, interaction, 'foo-consumer')
        self.assertEqual('AHelloToTheWorldHTTPTest', testcase_cls.__name__)
        self.assertTrue(nose.run(argv=[__file__], suite=[testcase_cls()]))

    def test_http_testcase_builder_of_get_json(self):
        interaction = Interaction.from_dict({
            "providerState": "Json is good",
            "description": "a hello to get json",
            "request": {
                "method": "GET",
                "path": "/json",
                "query": "key=device&val=iphone",
            },
            "response": {
                "status": 200,
                "body": {'device': 'iphone'},
                "headers": {
                    'Content-Type': 'application/json',
                    'Content-Length': '20',
                }
            }
        })
        testcase_cls = http_case_factory('tests.unit.provider.mini_app.app', State, interaction, 'foo-consumer')
        self.assertEqual('AHelloToGetJsonHTTPTest', testcase_cls.__name__)
        self.assertTrue(nose.run(argv=[__file__], suite=[testcase_cls()]))

    def test_http_testcase_builder_of_post_json(self):
        interaction = Interaction.from_dict({
            "providerState": "Json is good",
            "description": "a hello to post json",
            "request": {
                "method": "POST",
                "path": "/json",
                "body": {
                    "query": {
                        "facets": ["est_download"],
                        "filters": {
                            "product_ids": [
                                1000600000000005,
                                1000600000000006
                            ]
                        }
                    }
                },
                "headers": {
                    "Content-Type": "application/json"
                }
            },
            "response": {
                "status": 200,
                "body": {'length': 1},
                "headers": {
                    'Content-Type': 'application/json',
                }
            }
        })
        testcase_cls = http_case_factory('tests.unit.provider.mini_app.app', State, interaction, 'foo-consumer')
        self.assertEqual('AHelloToPostJsonHTTPTest', testcase_cls.__name__)
        self.assertTrue(nose.run(argv=[__file__], suite=[testcase_cls()]))

    def test_http_testcase_builder_of_headers(self):
        interaction = Interaction.from_dict({
            "providerState": "bingo and pango",
            "description": "ping pong",
            "request": {
                "method": "GET",
                "path": "/headers",
                "headers": {
                    "X-Pacte-Test": "bingo",
                }
            },
            "response": {
                "status": 200,
                "body": "bingo",
                "headers": {
                    'x-pacte-test': 'pango'
                }
            }
        })
        testcase_cls = http_case_factory('tests.unit.provider.mini_app.app', State, interaction, 'foo-consumer')
        self.assertEqual('PingPongHTTPTest', testcase_cls.__name__)
        self.assertTrue(nose.run(argv=[__file__], suite=[testcase_cls()]))
