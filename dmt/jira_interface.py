from autologging import traced
from jira import JIRA

from dmt.config.config import LOGGER


@traced(LOGGER)
class JiraInterface(object):
    def __init__(self, jira_url, jira_user, jira_password):
        self.jira = Jira(jira_url, basic_auth=(jira_user, jira_password))

    def log_task_time(self, issue, seconds, comment=None):
        self.jira.log_task_time(issue, seconds, comment=comment)


@traced(LOGGER)
class Jira(JIRA):
    def log_task_time(self, issue, seconds, comment=None):
        self.add_worklog(issue, timeSpentSeconds=seconds, comment=comment)
