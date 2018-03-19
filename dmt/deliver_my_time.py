import re
import shelve

import arrow
from jira.exceptions import JIRAError
from requests.exceptions import RequestException

from dmt.config.config import LOGGER
from dmt.config.config import TOGGL_API_URL
from dmt.jira_interface import JiraInterface
from dmt.toggl_interface import TogglInterface

logger = LOGGER


class Dmt(object):
    def __init__(self, token, jira_url, jira_user, jira_password, tag='logged'):
        self.toggl = TogglInterface(TOGGL_API_URL, token)
        self.jira = JiraInterface(jira_url, jira_user, jira_password)
        self.tag = tag
        self.local_entries = shelve.open('dmt_local')

    def log_time_to_jira(self, days=30, pattern=r'.*', comment='time logged by dmt; entry {}'):
        """
        Collect time entries from toggl. Log every entry without tag to jira and tag entry on toggl side.

        :param days: days span
        :param pattern: log toggle entry when description matches pattern. then use matched part as task unique name
        :param comment: description for time logs in jira
        :return:
        """
        start_date = self._get_start_datetime(days)
        toggl_time_entries = self.toggl.get_time_entries(start_date)
        filtered_toggl_time_entries = self._filter_toggl_time_entries(toggl_time_entries, pattern)

        for time_entry in [entry for entry in filtered_toggl_time_entries]:

            if not self._local_entry_flag_exist(time_entry['id'], 'logged'):
                try:
                    self._log_task_time(comment, time_entry)
                except JIRAError:
                    self._flag_logged_in_local(time_entry, False)
                    continue

            if not self._local_entry_flag_exist(time_entry['id'], 'tagged'):
                try:
                    self._tag_time_entry(time_entry)
                except RequestException:
                    self._flag_tagged_in_local(time_entry, False)
                    continue

            self.local_entries.pop(str(time_entry['id']), None)

    def _log_task_time(self, comment, time_entry):
        self.jira.log_task_time(time_entry['jira_name'], time_entry['duration'],
                                comment=comment.format(time_entry['id']))
        logger.info('Logged time for entry {} to Jira'.format(time_entry['id']))

    def _flag_logged_in_local(self, time_entry, value):
        logger.error('Error during logging time for entry {} to Jira', exc_info=True)
        self.local_entries.setdefault(str(time_entry['id']), {})
        self.local_entries[str(time_entry['id'])]['logged'] = value
        logger.info('Set logged flag to false in local entries storage')

    def _tag_time_entry(self, time_entry):
        self.toggl.tag_time_entry(time_entry['id'], self.tag)
        logger.info('Tagged entry {} in Toggle'.format(time_entry['id']))

    def _flag_tagged_in_local(self, time_entry, value):
        logger.error('Error during tagging entry {} in Toggle', exc_info=True)
        self.local_entries.setdefault(str(time_entry['id']), {})
        self.local_entries[str(time_entry['id'])]['tagged'] = value
        logger.info('Set logged flag to False in local entries storage')

    @staticmethod
    def _get_start_datetime(days):
        now = arrow.utcnow()
        start_datetime = now.shift(days=-days)
        return start_datetime.format('YYYY-MM-DDTHH:mm:ssZZ')

    def _filter_toggl_time_entries(self, entries, pattern):
        filtered_entries = []
        for entry in entries:

            if self.tag in entry.get('tags', []):
                continue

            match = re.search(pattern, entry['description'], re.IGNORECASE)
            if match:
                entry['jira_name'] = match.group(0)
            else:
                continue

            if entry['duration'] < 60:
                continue

            filtered_entries.append(entry)
        return filtered_entries

    def _local_entry_flag_exist(self, entry_id, key):
        if self.local_entries.get(str(entry_id), {}).get(key, None):
            return True
