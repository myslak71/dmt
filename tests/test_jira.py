import unittest

import requests_mock

from dmt.jira_interface import JiraInterface


@requests_mock.Mocker()
class TestBaseJira(unittest.TestCase):
    pass


@requests_mock.Mocker()
class TestJira(TestBaseJira):
    def test_jira_connection(self, response_mock):
        response_mock.register_uri('GET', 'https://www.jira_url.example/rest/api/2/serverInfo',
                                   json={'versionNumbers': [1, 2, 3]}, status_code=200)
        response_mock.register_uri('GET', 'https://www.jira_url.example/rest/api/2/field'
                                   , status_code=200)
        self.jira = JiraInterface('https://www.jira_url.example', 'kedod', 'kedod')

    def test_add_worklog(self, response_mock):
        response_mock.register_uri('GET', 'https://www.jira_url.example/rest/api/2/serverInfo',
                                   json={'versionNumbers': [1, 2, 3]}, status_code=200)
        response_mock.register_uri('GET', 'https://www.jira_url.example/rest/api/2/field'
                                   , status_code=200)
        response_mock.register_uri('POST', 'https://www.jira_url.example/rest/api/2/issue/issue/worklog'
                                   , status_code=200)
        self.jira = JiraInterface('https://www.jira_url.example', 'kedod', 'kedod')
        self.jira.log_task_time('issue', 100, comment='test')
