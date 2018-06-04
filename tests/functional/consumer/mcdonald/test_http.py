"""
Copyright (c) 2018 App Annie Inc. All rights reserved.

WARNING: This test is not supposed to be run by `nosetests`
It is run by tests/functional/pact/test_pact.py
"""
import unittest as ut

from pacte import contract_factory
from pacte.mockings import MockServices, MockAPI
from tests.functional.consumer.mcdonald.mcdonald import mcdonald


class HTTPTest(ut.TestCase):

    def test_http(self):
        contract = contract_factory.register('chicken-farm', 'McDonald')
        contract.given("10k-healthy-chickens").upon_receiving("one-thousand-buy-request").with_request(
            'GET', '/buy-chicken', query='n=1000'
        ).will_respond_with(200, body='success')
        with MockServices(MockAPI(contract, scheme='http', domain='www.chicken-farm.com')):
            result = mcdonald()
            self.assertEqual('buy 1k chicken: success', result)
