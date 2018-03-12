import requests
from future.utils import with_metaclass


class BaseToggle(object):
    def __init__(self, url, token):
        self._url = url
        self._token = token


"""
class ToggleTimeEntries(with_metaclass(_Toggl)):
    def get_time_entries(self, start_date="", end_date=""):
        if start_date and end_date:
            return self._get_time_entries_with_start_end_date(start_date=start_date, end_date=end_date)
        elif start_date and not end_date:
            return self._get_time_entries_with_start_date(start_date=start_date)
        elif end_date and not start_date:
            return self._get_time_entries_with_end_date(end_date=end_date)
        elif not start_date and not end_date:
            return self._get_time_entries_default()

    def _get_time_entries_default(self):
        return requests.get(
            "{}time_entries?".format(config.TOGGL_URL), auth=(self._token, "api_token")).json()

    def _get_time_entries_with_start_date(self, start_date):
        return requests.get(
            "{}time_entries?start_date={start}T15%3A42%3A46%2B02%3A00".format(config.TOGGL_URL,
                                                                              start=start_date),
            auth=(self._token, "api_token")).json()

    def _get_time_entries_with_end_date(self, end_date):
        return requests.get(
            "{}time_entries?end_date={end}T15%3A42%3A46%2B02%3A00".format(config.TOGGL_URL,
                                                                          end=end_date),
            auth=(self._token, "api_token")).json()

    def _get_time_entries_with_start_end_date(self, start_date, end_date):
        return requests.get(
            "{}time_entries?start_date={start}T15%3A42%3A46%2B02%3A00&end_date={end}T15%3A42%3A46%2B02%3A00".format(
                config.TOGGL_URL,
                start=start_date, end=end_date),
            auth=(self._token, "api_token")).json()
"""