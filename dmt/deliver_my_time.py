import datetime

from dmt.config.config import TOGGLE_API_URL
from dmt.jira_interface import JiraInterface
from dmt.toggle_interface import ToggleInterface


class Dmt(object):
    def __init__(self, token, jira_url, jira_user, jira_password, tag='logged'):
        self.toggle = ToggleInterface(TOGGLE_API_URL, token)
        self.jira = JiraInterface(jira_url, basic_auth=(jira_user, jira_password))
        self.tag = tag

    def log_time_entries(self, days):
        start_date = self._get_start_datetime(days)
        toggle_time_entries = self.toggle.get_time_entries(start_date)
        for time_entry in toggle_time_entries:
            self.jira.log_task_time(time_entry['description'], time_entry['duration'], comment='logged time by dmt')
            self.toggle.tag_time_entry(time_entry['id'])

    def _get_start_datetime(self, days):
        now = datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc)
        start_datetime = now - datetime.timedelta(days=days)
        return start_datetime.isoformat()
