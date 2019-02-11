# Copyright (c) 2017 App Annie Inc. All rights reserved.

from unittest import TestCase


class StateSubBaz(TestCase):
    """
    This class in sub directory will also be collected
    """
    state = 'subbaz'

    def setup(self):
        pass

    def tearDown(self):
        pass
