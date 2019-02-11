# Copyright (c) 2017 App Annie Inc. All rights reserved.
import os.path
from unittest import TestCase
from pacte.states import load_states


class StateCollectorTest(TestCase):

    def test_collect(self):
        """
        tests/states/state*.py
        """
        states = load_states(os.path.join(os.path.dirname(__file__), 'states'))
        self.assertEqual(4, len(states))
        self.assertTrue('foo' in states)
        self.assertTrue('foo2' in states)
        self.assertTrue('bar' in states)
        self.assertTrue('subbaz' in states)
        foo_state = states['foo']
        self.assertEqual('StateFoo', foo_state.__name__)
