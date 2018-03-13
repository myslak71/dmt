import unittest
import requests_mock
from dmt.toggl_interface import TogglInterface
from tests.fixtures.responses import fixed_time_entries


class TestBaseToggl(unittest.TestCase):
    def setUp(self):
        self.toggl = TogglInterface('https://www.toggl.com/api/v8/', 'token')


@requests_mock.Mocker()
class TestToggl(TestBaseToggl):
    def test_get_time_entries_response(self, response_mock):
        response_mock.register_uri('GET', 'https://www.toggl.com/api/v8/time_entries?start_date=&end_date=',
                                   json=fixed_time_entries, status_code=200)
        time_entries = self.toggl.get_time_entries()
        self.assertEqual(fixed_time_entries, time_entries)

    def test_tag_time_entries_response(self, response_mock):
        response_mock.register_uri('POST', 'https://www.toggl.com/api/v8/time_entries/814800050',
                                   status_code=200)
        self.toggl.tag_time_entry(fixed_time_entries[0]['id'])
