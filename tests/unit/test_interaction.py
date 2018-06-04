# Copyright (c) 2017 App Annie Inc. All rights reserved.
import unittest

from pacte.interaction import Interaction


class TestInteraction(unittest.TestCase):

    def test_to_dict(self):
        interaction = Interaction()
        interaction.given("a state").upon_receiving("a request").with_request(
            method="post",
            path="/path",
            query="foo=bar",
            headers={"Custom-Header": "value"},
            body={
                "alligator": {
                    "favouriteColours": ["red", "blue"]
                }
            }
        ).will_respond_with(
            status=200,
            headers={"Custom-Header": "value"},
            body={"key": "value"}
        )

        expected_json = {
            "description": "a request",
            "providerState": "a state",
            "request": {
                "method": "POST",
                "path": "/path",
                "query": "foo=bar",
                "headers": {
                    "Custom-Header": "value"
                },
                "body": {
                    "alligator": {
                        "favouriteColours": ["red", "blue"]
                    }
                }
            },
            "response": {
                "status": 200,
                "headers": {
                    "Custom-Header": "value"
                },
                "body": {
                    "key": "value"
                }
            }
        }
        self.assertDictEqual(expected_json, interaction.to_dict())

    def test_from_dict(self):
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
        self.assertEqual('World is good', interaction.provider_state)
        self.assertEqual('a hello to the world', interaction.description)
        self.assertDictEqual(
            {
                "method": "GET",
                "path": "/",
            }, interaction.request)
        self.assertEqual(
            {
                "status": 200,
                "body": "Hello, World!",
                "headers": {
                    'Content-Type': 'text/html; charset=utf-8',
                    'Content-Length': '13'
                }
            }, interaction.response
        )

    def test_equals(self):
        interaction1 = Interaction.from_dict({
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
        interaction2 = Interaction()
        interaction2.given("World is bad").upon_receiving("a curse to the world").with_request(
            method="get",
            path="/",
        ).will_respond_with(
            status=200,
            body="Hello, World!",
            headers={
                'Content-Type': 'text/html; charset=utf-8',
                'Content-Length': '13'
            }
        )
        self.assertTrue(interaction1.equals(interaction2))
