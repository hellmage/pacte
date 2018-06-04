# Copyright (c) 2017 App Annie Inc. All rights reserved.
import unittest

import requests
from requests_mock import NoMockAddress

from pacte.contract import Contract
from pacte.mockings import MockAPI, MockServices


class TestMockServices(unittest.TestCase):
    maxDiff = None

    def test_base(self):
        contract = Contract("test_provider", "test_consumer")
        contract.given("Test").upon_receiving("a request").with_request(
            method="get",
            path="/path",
            headers={"Custom-Header": "value"},
        ).will_respond_with(
            status=200,
            headers={"Custom-Header": "value"},
            body={"key": "value"}
        )
        with MockServices(MockAPI(contract)) as service:
            response = requests.get('{}/path'.format(service.mock_apis[0].get_service_host()))
            self.assertEqual(response.status_code, 200)
            self.assertDictEqual(response.json(), {"key": "value"})

    def test_multi_interactions(self):
        contract = Contract("test_provider", "test_consumer")
        contract.given("Test").upon_receiving("a request").with_request(
            method="get",
            path="/path",
            headers={"Custom-Header": "value"}, ).will_respond_with(
            status=200,
            headers={"Custom-Header": "value"},
            body={"key": "value"})
        with MockServices(MockAPI(contract)) as service:
            response = requests.get('{}/path'.format(service.mock_apis[0].get_service_host()))
            self.assertEqual(response.status_code, 200)
            self.assertDictEqual(response.json(), {"key": "value"})

        contract2 = Contract("test_provider2", "test_consumer")
        contract2.given("Test").upon_receiving("a request").with_request(
            method="get",
            path="/path2",
            headers={"Custom-Header": "value"}, ).will_respond_with(
            status=200,
            headers={"Custom-Header": "value"},
            body={"key": "value2"})

        with MockServices(MockAPI(contract2)) as service2:
            response = requests.get('{}/path2'.format(service2.mock_apis[0].get_service_host()))
            self.assertEqual(response.status_code, 200)
            self.assertDictEqual(response.json(), {"key": "value2"})

        contract3 = Contract("test_provider2", "test_consumer")
        contract3.given("Test").upon_receiving("a request").with_request(
            method="get",
            path="/path3",
            headers={"Custom-Header": "value"}, ).will_respond_with(
            status=200,
            headers={"Custom-Header": "value"},
            body={"key": "value3"})

        with MockServices(MockAPI(contract3)) as service3:
            response = requests.get('{}/path3'.format(service3.mock_apis[0].get_service_host()))
            self.assertEqual(response.status_code, 200)
            self.assertDictEqual(response.json(), {"key": "value3"})

    def test_mock_service_functional_json(self):
        contract = Contract('provider', 'consumer')
        contract.given("Test").upon_receiving("a request").with_request(
            method="get",
            path="/path",
            headers={"Custom-Header": "value"},
        ).will_respond_with(
            status=200,
            headers={"Custom-Header": "value"},
            body={"key": "value"}
        )

        with MockServices(MockAPI(contract, port=1234)):
            response = requests.get('http://localhost:1234/path')
            self.assertEqual(response.status_code, 200)
            self.assertDictEqual(response.json(), {"key": "value"})

    def test_mock_service_multi_functional(self):
        contract = Contract('provider', 'consumer')
        contract.given("Test").upon_receiving("a request").with_request(
            method="get",
            path="/get_json",
            headers={"Custom-Header": "value"},
        ).will_respond_with(
            status=200,
            headers={"Custom-Header": "value"},
            body={"key": "value"}
        )

        contract.given("Test2").upon_receiving("second request").with_request(
            method="get",
            path="/get_str",
            headers={"Custom-Header": "value"},
        ).will_respond_with(
            status=200,
            headers={"Content-Type": "text/html"},
            body="Test String Response"
        )

        with MockServices(MockAPI(contract, port=1234)):
            response = requests.get('http://localhost:1234/get_json')
            self.assertEqual(response.status_code, 200)
            self.assertDictEqual(response.json(), {"key": "value"})

            response = requests.get('http://localhost:1234/get_str')
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.text, "Test String Response")

    def test_mock_service_functional_str(self):
        contract = Contract('provider', 'consumer')
        contract.given("Test").upon_receiving("a request").with_request(
            method="get",
            path="/path",
            headers={"Custom-Header": "value"},
        ).will_respond_with(
            status=200,
            headers={"Custom-Header": "value"},
            body="Test String Response"
        )

        with MockServices(MockAPI(contract, port=1234)):
            response = requests.get('http://localhost:1234/path')
            assert response.status_code == 200
            self.assertEqual(response.text, "Test String Response")

    def test_mock_service_get_querystr(self):
        contract = Contract('provider', 'consumer')
        contract.given("Test").upon_receiving("a request").with_request(
            method="get",
            path="/path",
            query="date=2017-11-21",
        ).will_respond_with(
            status=200,
            headers={"content-type": "application/json", 'X-Request-ID': '9v7uygi2hop'},
            body={"key": "value"}
        )

        with MockServices(MockAPI(contract, port=1234)):
            with self.assertRaises(NoMockAddress):
                requests.get('http://localhost:1234/path')
            with self.assertRaises(NoMockAddress):
                requests.get('http://localhost:1234/path?date=2017-11-22')
            response = requests.get('http://localhost:1234/path?date=2017-11-21')
            self.assertEqual(response.status_code, 200)
            self.assertDictEqual({"key": "value"}, response.json())
            self.assertEqual('application/json', response.headers['Content-Type'])
            self.assertEqual('9v7uygi2hop', response.headers['X-Request-ID'])

    def test_mock_service_post_querystr(self):
        contract = Contract('provider', 'consumer')
        contract.given("Test2").upon_receiving("a request2").with_request(
            method="post",
            path="/path",
            headers={"Custom-Header": "value"},
        ).will_respond_with(
            status=200,
            headers={"Content-Type": "application/json"},
            body={"key": "value"}
        )

        with MockServices(MockAPI(contract, port=1234)):
            with self.assertRaises(NoMockAddress):
                requests.get('http://localhost:1234/path')
            with self.assertRaises(NoMockAddress):
                requests.get('http://localhost:1234/path?date=2017-11-22')
            response = requests.post('http://localhost:1234/path', data={"test": "data"})
            self.assertEqual(response.status_code, 200)
            self.assertDictEqual({"key": "value"}, response.json())
            self.assertEqual('application/json', response.headers['Content-Type'])

    def test_mock_service_multi_interactions_requests(self):
        contract_get = Contract('provider_get', 'consumer')
        contract_get.given("Test").upon_receiving("a request").with_request(
            method="get",
            path="/path",
            query="date=2017-11-21",
        ).will_respond_with(
            status=200,
            headers={"content-type": "application/json", 'X-Request-ID': '9v7uygi2hop'},
            body={"key": "value"}
        )
        contract_post = Contract('provider_post', 'consumer')
        contract_post.given("Test2").upon_receiving("a request2").with_request(
            method="post",
            path="/path",
            headers={"Custom-Header": "value"},
        ).will_respond_with(
            status=200,
            headers={"Content-Type": "application/json"},
            body={"key": "value"}
        )

        with MockServices(MockAPI(contract_get, domain='domain_get', port=1234)):
            response_get = requests.get('http://domain_get:1234/path?date=2017-11-21')
            self.assertEqual(response_get.status_code, 200)
            self.assertDictEqual({"key": "value"}, response_get.json())
            self.assertEqual('application/json', response_get.headers['Content-Type'])
            self.assertEqual('9v7uygi2hop', response_get.headers['X-Request-ID'])

        with MockServices(MockAPI(contract_post, domain='domain_post', port=1234)):
            response_post = requests.post('http://domain_post:1234/path', data={"test": "data"})
            self.assertEqual(response_post.status_code, 200)
            self.assertDictEqual({"key": "value"}, response_post.json())
            self.assertEqual('application/json', response_post.headers['Content-Type'])

    def test_mock_multiple_services(self):
        contract_get = Contract('provider_get', 'consumer')
        contract_get.given("Test").upon_receiving("a request").with_request(
            method="get",
            path="/path",
            query="date=2017-11-21",
        ).will_respond_with(
            status=200,
            headers={"content-type": "application/json", 'X-Request-ID': '9v7uygi2hop'},
            body={"key": "value"}
        )
        mock_get_api = MockAPI(contract_get, domain='domain_get', port=1234)
        contract_post = Contract('provider_post', 'consumer')
        contract_post.given("Test2").upon_receiving("a request2").with_request(
            method="post",
            path="/path",
            headers={"Custom-Header": "value"},
        ).will_respond_with(
            status=200,
            headers={"Content-Type": "application/json"},
            body={"key": "value"}
        )
        mock_post_api = MockAPI(contract_post, domain='domain_post', port=1234)

        with MockServices([mock_get_api, mock_post_api]):
            response_get = requests.get('http://domain_get:1234/path?date=2017-11-21')
            self.assertEqual(response_get.status_code, 200)
            self.assertDictEqual({"key": "value"}, response_get.json())
            self.assertEqual('application/json', response_get.headers['Content-Type'])
            self.assertEqual('9v7uygi2hop', response_get.headers['X-Request-ID'])

            response_post = requests.post('http://domain_post:1234/path', data={"test": "data"})
            self.assertEqual(response_post.status_code, 200)
            self.assertDictEqual({"key": "value"}, response_post.json())
            self.assertEqual('application/json', response_post.headers['Content-Type'])
