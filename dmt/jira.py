from jira import JIRA


class JiraInterface(JIRA):
    def log_task_time(self, issue, seconds, comment=None):
        self.add_worklog(issue, timeSpentSeconds=seconds, comment=comment)
