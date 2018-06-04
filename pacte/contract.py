# Copyright (c) 2017 App Annie Inc. All rights reserved.
# -*- coding: utf-8 -*-
import logging

import simplejson as json

from pacte.interaction import Interaction

logger = logging.getLogger(__name__)


class Contract(object):
    def __init__(self, provider, consumer):
        self.provider = provider
        self.consumer = consumer
        self.interactions = []

    def given(self, state):
        interaction = Interaction()
        self.add_interaction(interaction)
        return interaction.given(state)

    def add_interaction(self, interaction):
        """
        Add a new interaction to the mock service.
        Deduplicate interaction in this process.
        """
        for _interaction in self.interactions:
            if _interaction.equals(interaction):
                logger.warning(
                    'Found duplicate interaction:\n'
                    'provider=%s\nconsumer=%s\ninteraction1=%s\ninteraction2=%s',
                    self.provider, self.consumer,
                    json.dumps(_interaction.to_dict()), json.dumps(interaction.to_dict())
                )
                return
        self.interactions.append(interaction)

    def to_dict(self):
        from pacte import VERSION
        return dict({
            "provider": {
                "name": self.provider,
            },
            "consumer": {
                "name": self.consumer,
            },
            "interactions": [interaction.to_dict() for interaction in self.interactions],
            "metadata": {
                "pacte": {
                    "version": VERSION
                }
            }
        })

    @classmethod
    def from_dict(cls, pact):
        contract = cls(pact['provider']['name'], pact['consumer']['name'])
        for interaction_in_pact in pact.setdefault('interactions', []):
            interaction = Interaction.from_dict(interaction_in_pact)
            contract.add_interaction(interaction)
        return contract
