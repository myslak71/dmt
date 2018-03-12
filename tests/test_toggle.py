import unittest
from dmt.toggl import BaseToggle


class TestBaseToggle(unittest.TestCase):
    def setUp(self):
        self.toggle = BaseToggle('url', 'token')

class TestToggleConnection(TestBaseToggle):
    def test_establish_connection(self):
        pass

