import arrow

from dmt.config.config import TOGGL_API_URL
from dmt.jira_interface import JiraInterface
from dmt.toggl_interface import TogglInterface


class Dmt(object):
    def __init__(self, token, jira_url, jira_user, jira_password, tag='logged'):
        self.toggl = TogglInterface(TOGGL_API_URL, token)
        self.jira = JiraInterface(jira_url, jira_user, jira_password)
        self.tag = tag

    def log_time_to_jira(self, days=30, comment='time logged by dmt'):
        """
        Collect time entries from toggl. Log every entry without tag to jira and tag entry on toggl side.

        :param days: days span
        :param comment: description for time logs in jira
        :return:
        """
        start_date = self._get_start_datetime(days)
        toggl_time_entries = self.toggl.get_time_entries(start_date)
        filtered_toggl_time_entries = self._filter_toggl_time_entries(toggl_time_entries)
        for time_entry in [entry for entry in filtered_toggl_time_entries]:
            self.jira.log_task_time(time_entry['description'], time_entry['duration'], comment=comment)
            self.toggl.tag_time_entry(time_entry['id'])

    @staticmethod
    def _get_start_datetime(days):
        now = arrow.utcnow()
        start_datetime = now.shift(days=-days)
        return start_datetime.format('YYYY-MM-DDTHH:mm:ssZZ')

    def _filter_toggl_time_entries(self, toggl_time_entries):
        return [time_entry for time_entry in toggl_time_entries if
                "tags" not in time_entry or self.tag not in time_entry.get("tags", [])]
