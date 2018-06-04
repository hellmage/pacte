# Copyright (c) 2017 App Annie Inc. All rights reserved.

from unittest import TestCase


class StateBar(TestCase):
    state = 'bar'

    def setup(self):
        pass

    def tearDown(self):
        pass


class StateBar1(object):
    """
    This class will not be collected because it's not a subclass of unittest.TestCase.
    """
    state = 'bar'

    def setup(self):
        pass

    def tearDown(self):
        pass
