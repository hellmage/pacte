# Copyright (c) 2017 App Annie Inc. All rights reserved.

from unittest import TestCase


class StateBaz(TestCase):
    """
    This class will not be collected because the filename does not start with "state_".
    """
    state = 'baz'

    def setup(self):
        pass

    def tearDown(self):
        pass
