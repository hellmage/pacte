# Copyright (c) 2017 App Annie Inc. All rights reserved.
import os
import os.path

import shutil
import json

from pacte.contract import Contract
from pacte.exceptions import PacteServiceException
from pacte.utils.json import DateTimeEncoder

_contracts = {}
_consumer = None


def register(provider, consumer):
    global _contracts, _consumer
    if not _consumer:
        _consumer = consumer
    else:
        if _consumer != consumer:
            raise PacteServiceException('More than one consumers are registered: %s, %s', _consumer, consumer)
    contract = Contract(provider, consumer)
    contracts = _contracts.setdefault(provider, [])
    contracts.append(contract)
    return contract


def reset_factory(contract_dir='.pact'):
    global _contracts, _consumer
    _contracts = {}
    _consumer = None
    if os.path.exists(contract_dir):
        shutil.rmtree(contract_dir)


def _merge(contracts):
    """
    Merge contracts of the same provider and consumer
    """
    if not contracts:
        return []
    contract = contracts[0]
    for _contract in contracts[1:]:
        for _interaction in _contract.interactions:
            contract.add_interaction(_interaction)
    return contract


def serialize(contract_dir='.pact'):
    """
    <contract_dir>/
      - <provider service name>.json
    """
    if not os.path.exists(contract_dir):
        os.makedirs(contract_dir)
    for provider, contracts in _contracts.items():
        contract_name = os.path.join(contract_dir, provider + ".json")
        with open(contract_name, 'w') as contract_file:
            json.dump(
                _merge(contracts).to_dict(),
                contract_file,
                indent=4,
                sort_keys=True,
                cls=DateTimeEncoder
            )
