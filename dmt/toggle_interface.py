import requests
from requests.adapters import HTTPAdapter


class ToggleInterface(object):
    def __init__(self, api_url, token):
        self.toggl = BaseToggl().setup_toggl(api_url, token)

    def get_time_entries(self, start_time='', end_time=''):
        return self.toggl.get_time_entries(start_time=start_time, end_time=end_time)

    def tag_time_entry(self, time_entries):
        return self.toggl.tag_time_entry(time_entries)


class BaseToggl(object):
    def setup_toggl(self, api_url, token):
        self.api_url = api_url
        self.token = token
        self._set_session()
        return self

    def get_time_entries(self, start_time='', end_time=''):
        start_date = self._format_datetime(start_time)
        end_date = self._format_datetime(end_time)
        url = self._build_url(start_date=start_date, end_date=end_date, category='time_entries', separate_sign='?')
        print(url, 'chuj')
        return self.session.get(url).json()

    def tag_time_entry(self, id):
        url = self._build_url(id=id, category='time_entries', separate_sign='/')
        return requests.post('{url}'.format(url=url))

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

    def _format_datetime(self, datetime):
        if datetime:
            grouped_datetime = datetime.split('T')
            formated_time = grouped_datetime[-1].replace(':', '%3A').replace('+', '%2B').replace('-', '%2D')
            return '{date}T{time}'.format(date=grouped_datetime[0], time=formated_time)
        return ''

    def _get_parameters(self, separate_sign, **kwargs):
        if separate_sign == '/':
            return '/{id}'.format(id=kwargs.pop('id', ''))
        elif separate_sign == '?':
            return '?' + '&'.join(['{key}={value}'.format(key=kwarg, value=kwargs[kwarg]) for kwarg in kwargs])

