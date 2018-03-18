import json
import requests
from requests.adapters import HTTPAdapter


class TogglInterface(object):
    def __init__(self, api_url, token):
        self.toggl = Toggl().setup_toggl(api_url, token)

    def get_time_entries(self, start_time='', end_time=''):
        return self.toggl.get_time_entries(start_time=start_time, end_time=end_time)

    def tag_time_entry(self, entry_id, tag):
        return self.toggl.tag_time_entry(entry_id, tag)


class Toggl(object):
    def setup_toggl(self, api_url, token):
        self.api_url = api_url
        self.token = token
        self._set_session()
        return self

    def get_time_entries(self, start_time='', end_time=''):
        start_date = self._format_datetime(start_time)
        end_date = self._format_datetime(end_time)
        url = self._build_url(start_date=start_date, end_date=end_date, category='time_entries', separate_sign='?')
        response = self.session.get(url)
        response.raise_for_status()
        return response.json()

    def tag_time_entry(self, entry_id, tag):
        url = self._build_url(entry_id=entry_id, category='time_entries', separate_sign='/')
        data = {'time_entry': {"tags": [tag], 'tag_action': 'add'}}
        response = self.session.put('{url}'.format(url=url), data=json.dumps(data), auth=(self.token, 'api_token'))
        response.raise_for_status()
        return response

    def _set_session(self):
        session = requests.Session()
        session.auth = (self.token, 'api_token')
        session.mount(self.api_url, HTTPAdapter(max_retries=5))
        self.session = session

    def _build_url(self, **kwargs):
        category = kwargs.pop('category')
        separate_sign = kwargs.pop('separate_sign')
        parameters = self._get_parameters(separate_sign, **kwargs)
        url = '{base_url}{cat}{params}'.format(base_url=self.api_url, cat=category, params=parameters)
        return url

    @staticmethod
    def _format_datetime(datetime):
        if datetime:
            grouped_datetime = datetime.split('T')
            formated_time = grouped_datetime[-1].replace(':', '%3A').replace('+', '%2B').replace('-', '%2D')
            return '{date}T{time}'.format(date=grouped_datetime[0], time=formated_time)
        return ''

    @staticmethod
    def _get_parameters(separate_sign, **kwargs):
        if separate_sign == '/':
            return '/{entry_id}'.format(entry_id=kwargs.pop('entry_id', ''))
        elif separate_sign == '?':
            return '?' + '&'.join(['{key}={value}'.format(key=kwarg, value=kwargs[kwarg]) for kwarg in kwargs])
