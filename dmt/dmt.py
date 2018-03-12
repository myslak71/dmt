import datetime

from dmt.toggl import ToggleInterface
from dmt.jira import JiraInterface
from dmt.config.config import TOGGLE_API_URL

class Dmt(object):
    def __init__(self, token, jira_url, jira_user, jira_password):
        self.toggle = ToggleInterface(TOGGLE_API_URL, token)
        self.jira = JiraInterface()

    def log_time(self, days):
        start_date = datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc).isoformat()
        toggle_time_entries = self.toggle.get_time_entries()
