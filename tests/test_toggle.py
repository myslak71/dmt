import unittest
import requests_mock
from dmt.toggl import Toggl
from tests.fixtures.responses import response


class TestBaseToggle(unittest.TestCase):
    def setUp(self):
        self.toggle = Toggl('https://www.toggl.com/api/v8/', 'token')


@requests_mock.Mocker()
class TestToggleConnection(TestBaseToggle):
    def test_response(self, response_mock):
        response_mock.register_uri('GET', 'https://www.toggl.com/api/v8/time_entries?start_date=&end_date=',
                                   json=response, status_code=200)
        time_entries = self.toggle.get_time_entries()
        self.assertEqual(response, time_entries)
