# Copyright (c) 2017 App Annie Inc. All rights reserved.

from unittest import TestCase


class StateFoo(TestCase):
    state = 'foo'

    def setup(self):
        pass

    def tearDown(self):
        pass


class StateFoo1(TestCase):
    """
    This class will not be collected because the "state" class attribute is missing.
    """

    def setUp(self):
        pass

    def tearDown(self):
        pass


class NonState(TestCase):
    """
    This class will not be collected because the class name does not start with "State".
    """

    def setUp(self):
        pass

    def tearDown(self):
        pass


class StateFoo2(TestCase):
    """
    This class will also be collected.
    """
    state = 'foo2'

    def setup(self):
        pass

    def tearDown(self):
        pass
