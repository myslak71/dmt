import unittest

import requests_mock
from ddt import ddt, data

from dmt.deliver_my_time import Dmt
from tests.fixtures.local_entries import no_entries, unlogged_entries, logged_and_untagged_entries
from tests.fixtures.responses import fixed_time_entries


# TODO:Make this pretty...
@ddt
@requests_mock.Mocker()
class TestDmt(unittest.TestCase):
    @data(no_entries, unlogged_entries, logged_and_untagged_entries)
    def test_log_time_entries(self, local_entries, response_mock):
        response_mock.register_uri('GET', 'https://www.jira_url.example/rest/api/2/serverInfo',
                                   json={'versionNumbers': [1, 2, 3]}, status_code=200)
        response_mock.register_uri('GET', 'https://www.jira_url.example/rest/api/2/field',
                                   status_code=200)
        response_mock.register_uri('POST', 'https://www.jira_url.example/rest/api/2/issue/task-1/worklog',
                                   status_code=200)
        response_mock.register_uri('POST', 'https://www.jira_url.example/rest/api/2/issue/task-2/worklog',
                                   status_code=200)
        response_mock.register_uri('POST', 'https://www.jira_url.example/rest/api/2/issue/task-3/worklog',
                                   status_code=200)
        response_mock.register_uri('GET', 'https://www.toggl.com/api/v8/time_entries?start_date=&end_date=',
                                   json=fixed_time_entries, status_code=200)
        response_mock.register_uri('POST', 'https://www.toggl.com/api/v8/time_entries/1',
                                   status_code=200)
        response_mock.register_uri('POST', 'https://www.toggl.com/api/v8/time_entries/2',
                                   status_code=200)
        response_mock.register_uri('POST', 'https://www.toggl.com/api/v8/time_entries/3',
                                   status_code=200)
        response_mock.register_uri('POST', 'https://www.jira_url.example/rest/api/2/issue/TAT-2019/worklog',
                                   status_code=200)
        dmt = Dmt('token', 'https://www.jira_url.example', 'jira_user', 'jira_pass')
        dmt.local_entries = local_entries
        dmt.log_time_to_jira(6)
