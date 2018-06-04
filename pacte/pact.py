"""
Copyright (c) 2017 App Annie Inc. All rights reserved.

WARNING: logic in this file is not covered in any test!
"""
import logging
import os
import os.path
import sys

import click
import nose
import simplejson as json

from pacte import contract_factory
from pacte.case_builder import http_case_factory
from pacte.contract import Contract
from pacte.exceptions import PacteServiceException
from pacte.states import load_states
from pacte.utils.json import datetime_decoder

logger = logging.getLogger('pacte.pact')
PROVIDER_TEST_RESULT = 'nosetests-ctp.xml'
CONSUMER_TEST_RESULT = 'nosetests-ctc.xml'


def _render_http_testsuite(app, contracts, states):
    provider_testcases = []
    for contract in contracts:
        for interaction in contract.interactions:
            state_cls = states.get(interaction.provider_state)
            if not state_cls:
                raise PacteServiceException('State "%s" is not prepared' % interaction.provider_state)
            provider_testcases.append(http_case_factory(app, state_cls, interaction)())
    return provider_testcases


@click.command()
@click.option('--statedir', help='Directory for state preparation scripts. Defaults to "tests/contract/provider"',
              default='tests/contract/provider')
@click.option(
    '--app', help='The Flask application instance. Defaults to "app.app"', default='app.app'
)
@click.argument(
    'contract', type=click.Path(exists=True),
)
def provider(statedir, app, contract):
    if os.path.exists(PROVIDER_TEST_RESULT):
        os.remove(PROVIDER_TEST_RESULT)
    if not os.path.exists(contract):
        logger.error('Contract file %s does not exist', contract)
        sys.exit(1)
    contracts = []
    if os.path.isdir(contract):
        for dirpath, dirnames, filenames in os.walk(contract):
            for filename in filenames:
                with open(os.path.join(dirpath, filename)) as f:
                    contract = Contract.from_dict(json.loads(f.read(), object_pairs_hook=datetime_decoder))
                    contracts.append(contract)
    else:
        with open(contract) as f:
            contract = Contract.from_dict(json.loads(f.read(), object_pairs_hook=datetime_decoder))
            contracts.append(contract)
    if not contracts:
        logger.info('No contract found')
        sys.exit()

    states = load_states(statedir)
    # It's important to provide all test cases in a list so that nosetests can
    # generate a proper xunit result summary file.
    test_cases = _render_http_testsuite(app, contracts, states)
    nose.run(
        argv=[__file__, '-sv', '--logging-level=INFO', '--with-xunit', '--xunit-file=' + PROVIDER_TEST_RESULT],
        suite=test_cases,
    )


@click.command()
@click.option(
    '--pact',
    help='Path to the directory to save contract files. It will be created if not exists. Defaults to ".pact"',
    default='.pact'
)
@click.option(
    '--contract',
    help='Path to the consumer contract tests. Defaults to "tests/contract/consumer"',
    default='tests/contract/consumer'
)
def consumer(pact, contract):
    if os.path.exists(CONSUMER_TEST_RESULT):
        os.remove(CONSUMER_TEST_RESULT)
    if not os.path.exists(contract):
        logger.warn('Contract file %s does not exist', contract)
        sys.exit()  # exit with success, to be compatible with services with no provider state prepared
    contract_factory.reset_factory(pact)
    nose.run(argv=[__file__, '-sv', '--with-xunit', '--xunit-file=' + CONSUMER_TEST_RESULT, contract])
    contract_factory.serialize(pact)
