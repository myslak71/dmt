import unittest
from dmt.toggl import BaseToggle


class TestBaseToggle(unittest.TestCase):
    def setUp(self):
        self.toggle = BaseToggle('url', 'token')


class TestToggleConnection(TestBaseToggle):
    def test_connection_established(self):
        pass

