# Copyright (c) 2017 App Annie Inc. All rights reserved.
import os
import os.path
import shutil
import unittest

import simplejson as json

from pacte import VERSION, contract_factory
from pacte.exceptions import PacteServiceException


class TestContractFactory(unittest.TestCase):
    maxDiff = None

    def setUp(self):
        contract_factory.reset_factory()

    def test_register(self):
        contract_factory.register('test_provider', 'test_consumer1')
        with self.assertRaises(PacteServiceException):
            contract_factory.register('test_provider', 'test_consumer2')

    def test_serialize(self):
        TEMP_PACT_DIR = '.test-pacts'
        contract_factory.reset_factory(TEMP_PACT_DIR)

        contract = contract_factory.register("test_provider1", "test_consumer")
        contract.given("Test").upon_receiving("a request").with_request(
            method="get",
            path="/path",
            headers={"Custom-Header": "value"}, ).will_respond_with(
            status=200,
            headers={"Custom-Header": "value"},
            body={"key": "value"})
        contract = contract_factory.register("test_provider1", "test_consumer")
        contract.given("Test").upon_receiving("a request").with_request(
            method="get",
            path="/path1",
            headers={"Custom-Header": "value1"}, ).will_respond_with(
            status=200,
            headers={"Custom-Header": "value1"},
            body={"key": "value1"})
        contract = contract_factory.register("test_provider2", "test_consumer")
        contract.given("Test").upon_receiving("a request").with_request(
            method="post",
            path="/path",
            headers={"Custom-Header": "value_post"}, ).will_respond_with(
            status=200,
            headers={"Custom-Header": "value_post"},
            body={"key": "value_post"})
        contract = contract_factory.register("test_provider1", "test_consumer")  # duplicated contract will be removed
        contract.given("another test").upon_receiving("another request").with_request(
            method="get",
            path="/path1",
            headers={"Custom-Header": "value1"}, ).will_respond_with(
            status=200,
            headers={"Custom-Header": "value1"},
            body={"key": "value1"})
        contract_factory.serialize(TEMP_PACT_DIR)

        # created two contract files with three contracts
        self.assertTrue(os.path.exists(os.path.join(TEMP_PACT_DIR, 'test_provider1.json')))
        self.assertTrue(os.path.exists(os.path.join(TEMP_PACT_DIR, 'test_provider2.json')))

        # merged two contracts of the same provider
        with open(os.path.join(TEMP_PACT_DIR, 'test_provider1.json')) as f:
            actual_contract = json.loads(f.read())
        expected_contract = {
            "provider": {
                "name": "test_provider1"
            },
            "consumer": {
                "name": "test_consumer"
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
                        "headers": {"Custom-Header": "value"},
                        "body": {"key": "value"}
                    }
                },
                {
                    "providerState": "Test",
                    "description": "a request",
                    "request": {
                        "method": "GET",
                        "path": "/path1",
                        "headers": {"Custom-Header": "value1"},
                    },
                    "response": {
                        "status": 200,
                        "headers": {"Custom-Header": "value1"},
                        "body": {"key": "value1"}
                    }
                },
            ],
            "metadata": {
                "pacte": {
                    "version": VERSION
                }
            },
        }
        self.assertDictEqual(actual_contract, expected_contract)

        shutil.rmtree(TEMP_PACT_DIR)
