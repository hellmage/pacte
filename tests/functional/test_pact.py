# Copyright (c) 2018 App Annie Inc. All rights reserved.
import os.path
import shutil
import unittest as ut

from click.testing import CliRunner

from pacte.pact import consumer, provider, CONSUMER_TEST_RESULT, PROVIDER_TEST_RESULT

PACT_PROVIDER = '.pact_provider'
PACT_CONSUMER = '.pact'


class PactTest(ut.TestCase):
    consumer_service = 'tests/functional/pact/consumer'
    provider_service = 'tests/functional/pact/provider'

    def _print_result(self, result):
        print('\n\n>' + '=' * 10 + 'buffered logs' + '=' * 10)
        print('> ' + result.output.replace('\n', '\n> '))
        print('>' + '=' * 13 + 'log end' + '=' * 13 + '\n')

    def setUp(self):
        if os.path.exists(PACT_PROVIDER):
            shutil.rmtree(PACT_PROVIDER)
        os.makedirs(PACT_PROVIDER)

    def tearDown(self):
        if os.path.exists(PACT_CONSUMER):
            shutil.rmtree(PACT_CONSUMER)
        if os.path.exists(PACT_PROVIDER):
            shutil.rmtree(PACT_PROVIDER)
        if os.path.exists(CONSUMER_TEST_RESULT):
            os.remove(CONSUMER_TEST_RESULT)
        if os.path.exists(PROVIDER_TEST_RESULT):
            os.remove(PROVIDER_TEST_RESULT)

    def test_consumer(self):
        runner = CliRunner()

        # Run consumer tests, generate contract of mcdonald for provider "chicken-farm"
        result = runner.invoke(consumer, ['--contract', 'tests/functional/consumer/mcdonald/'],
                               catch_exceptions=False)
        self.assertTrue(os.path.exists(CONSUMER_TEST_RESULT))
        shutil.copy(os.path.join(PACT_CONSUMER, 'chicken-farm.json'),
                    os.path.join(PACT_PROVIDER, 'mcdonald.json'))
        self._print_result(result)

        # Run provider test
        result = runner.invoke(provider, [
            '--statedir', 'tests/functional/provider/states/',
            '--app', 'tests.functional.provider.app.app',
            PACT_PROVIDER
        ], catch_exceptions=False)
        self.assertTrue(os.path.exists(PROVIDER_TEST_RESULT))
        self._print_result(result)
