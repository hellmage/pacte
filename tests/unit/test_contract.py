# Copyright (c) 2018 App Annie Inc. All rights reserved.
import unittest as ut

from pacte import VERSION
from pacte.contract import Contract
from pacte.interaction import Interaction


class TestContract(ut.TestCase):

    def test_mock_service_serialize_json(self):
        contract = Contract('provider', 'consumer')
        contract.given("Test").upon_receiving("a request").with_request(
            method="get",
            path="/path",
            headers={"Custom-Header": "value"},
        ).will_respond_with(
            status=200,
            headers={"Content-Type": "text/html"},
            body={"key": "value"}
        )

        expected_contract = {
            'provider': {'name': 'provider'},
            'consumer': {'name': 'consumer'},
            "metadata": {
                "pacte": {
                    "version": VERSION
                }
            },
            "interactions": [
                {
                    "providerState": "Test",
                    "description": "a request",
                    "request": {
                        "method": "GET",
                        "path": "/path",
                        "headers": {"Custom-Header": "value"},
                    },

                    "response": {
                        "status": 200,
                        "headers": {
                            "Content-Type": "text/html"
                        },
                        "body": {"key": "value"}
                    }
                }
            ],
        }
        actual_contract = contract.to_dict()
        self.assertDictEqual(actual_contract, expected_contract)

    def test_mock_service_serialize_text(self):
        contract = Contract('provider', 'consumer')
        contract.given("Test").upon_receiving("a request").with_request(
            method="get",
            path="/path",
            headers={"Custom-Header": "value"},
        ).will_respond_with(
            status=200,
            headers={"Content-Type": "text/html"},
            body="Test String Response"
        )

        expected_contract = {
            'provider': {'name': 'provider'},
            'consumer': {'name': 'consumer'},
            "metadata": {
                "pacte": {
                    "version": VERSION
                }
            },
            "interactions": [
                {
                    "providerState": "Test",
                    "description": "a request",
                    "request": {
                        "method": "GET",
                        "path": "/path",
                        "headers": {"Custom-Header": "value"},
                    },

                    "response": {
                        "status": 200,
                        "headers": {
                            "Content-Type": "text/html"
                        },
                        "body": "Test String Response"
                    }
                }
            ],
        }
        actual_contract = contract.to_dict()
        self.assertDictEqual(actual_contract, expected_contract)

    def test_mock_service_multi_interactions_serialize(self):
        contract = Contract('provider', 'consumer')
        contract.given("Test").upon_receiving("a request").with_request(
            method="get",
            path="/path",
            headers={"Custom-Header": "value"},
        ).will_respond_with(
            status=200,
            headers={"Content-Type": "text/html"},
            body="Test String Response"
        )

        contract.given("Test2").upon_receiving("a request2").with_request(
            method="post",
            path="/path",
            query="name=ron&status=good",
            headers={"Custom-Header": "value"},
        ).will_respond_with(
            status=200,
            headers={"Content-Type": "text/html"},
            body={"key": "value"}
        )

        expected_contract = {
            'provider': {'name': 'provider'},
            'consumer': {'name': 'consumer'},
            "metadata": {
                "pacte": {
                    "version": VERSION
                }
            },
            "interactions": [
                {
                    "providerState": "Test",
                    "description": "a request",
                    "request": {
                        "method": "GET",
                        "path": "/path",
                        "headers": {"Custom-Header": "value"},
                    },

                    "response": {
                        "status": 200,
                        "headers": {
                            "Content-Type": "text/html"
                        },
                        "body": "Test String Response"
                    }
                },
                {
                    "providerState": "Test2",
                    "description": "a request2",
                    "request": {
                        "method": "POST",
                        "path": "/path",
                        "query": "name=ron&status=good",
                        "headers": {"Custom-Header": "value"},
                    },

                    "response": {
                        "status": 200,
                        "headers": {
                            "Content-Type": "text/html"
                        },
                        "body": {"key": "value"}
                    }
                }
            ],
        }
        actual_contract = contract.to_dict()
        self.assertDictEqual(actual_contract, expected_contract)

    def test_from_dict(self):
        contract = Contract.from_dict({
            'provider': {'name': 'provider'},
            'consumer': {'name': 'consumer'},
            "metadata": {
                "pacte": {
                    "version": VERSION
                }
            },
            "interactions": [
                {
                    "providerState": "Test",
                    "description": "a request",
                    "request": {
                        "method": "GET",
                        "path": "/path",
                        "headers": {"Custom-Header": "value"},
                    },

                    "response": {
                        "status": 200,
                        "headers": {
                            "Content-Type": "text/html"
                        },
                        "body": "Test String Response"
                    }
                },
                {
                    "providerState": "Test2",
                    "description": "a request2",
                    "request": {
                        "method": "POST",
                        "path": "/path",
                        "query": "name=ron&status=good",
                        "headers": {"Custom-Header": "value"},
                    },

                    "response": {
                        "status": 200,
                        "headers": {
                            "Content-Type": "text/html"
                        },
                        "body": {"key": "value"}
                    }
                }
            ],
        })
        self.assertEqual('consumer', contract.consumer)
        self.assertEqual('provider', contract.provider)
        self.assertEqual(2, len(contract.interactions))

    def test_add_interaction(self):
        contract = Contract('provider', 'consumer')
        interaction = Interaction()
        interaction.given("Test").upon_receiving("a request").with_request(
            method="get",
            path="/path",
            headers={"Custom-Header": "value"},
        ).will_respond_with(
            status=200,
            headers={"Content-Type": "text/html"},
            body={"key": "value"}
        )
        contract.add_interaction(interaction)
        contract.add_interaction(interaction)
        self.assertEqual(1, len(contract.interactions))

