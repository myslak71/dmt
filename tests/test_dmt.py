import unittest
import requests_mock
from dmt.deliver_my_time import Dmt
from tests.fixtures.responses import fixed_time_entries


@requests_mock.Mocker()
class TestDmt(unittest.TestCase):
    def test_log_time_entries(self, response_mock):
        response_mock.register_uri('GET', 'https://www.jira_url.example/rest/api/2/serverInfo',
                                   json={'versionNumbers': [1, 2, 3]}, status_code=200)
        response_mock.register_uri('GET', 'https://www.jira_url.example/rest/api/2/field'
                                   , status_code=200)
        response_mock.register_uri('POST', 'https://www.jira_url.example/rest/api/2/issue/issue/worklog'
                                   , status_code=200)
        response_mock.register_uri('GET', 'https://www.toggl.com/api/v8/time_entries?start_date=&end_date=',
                                   json=fixed_time_entries, status_code=200)
        response_mock.register_uri('POST', 'https://www.toggl.com/api/v8/time_entries/814800050',
                                   status_code=200)
        response_mock.register_uri('POST', 'https://www.jira_url.example/rest/api/2/issue/TAT-2019/worklog',
                                   status_code=200)
        dmt = Dmt('token', 'https://www.jira_url.example','jira_user', 'jira_pass')
        dmt.log_time_entries(6)
