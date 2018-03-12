import unittest
import requests_mock
from dmt.toggl import Toggl
from tests.fixtures.responses import fixed_time_entries


class TestBaseToggle(unittest.TestCase):
    def setUp(self):
        self.toggle = Toggl('https://www.toggl.com/api/v8/', 'token')


@requests_mock.Mocker()
class TestToggleConnection(TestBaseToggle):
    def test_get_time_entries_response(self, response_mock):
        response_mock.register_uri('GET', 'https://www.toggl.com/api/v8/time_entries?start_date=&end_date=',
                                   json=fixed_time_entries, status_code=200)
        time_entries = self.toggle.get_time_entries()
        self.assertEqual(fixed_time_entries, time_entries)

    def test_tag_time_entries_response(self, response_mock):
        response_mock.register_uri('POST', 'https://www.toggl.com/api/v8/time_entries/814800050',
                                   status_code=200)
        self.toggle.tag_time_entries(fixed_time_entries)
