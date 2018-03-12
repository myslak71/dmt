import requests


class Toggl(object):
    def __init__(self, api_url, token):
        self.toggl = BaseToggl().setup_toggl(api_url, token)

    def get_time_entries(self, start_time='', end_time=''):
        return self.toggl.get_time_entries(start_time=start_time, end_time=end_time)

    def tag_time_entries(self, time_entries):
        return self.toggl.tag_time_entries(time_entries)


class BaseToggl(object):
    def setup_toggl(self, api_url, token):
        self.api_url = api_url
        self.token = token
        self._set_session()
        return self

    def get_time_entries(self, start_time='', end_time=''):
        start_date = self._format_date(start_time)
        end_date = self._format_date(end_time)
        url = self._build_url(start_date=start_date, end_date=end_date, category='time_entries', separate_sign='?')
        return self.session.get(url).json()

    def tag_time_entries(self, time_entries):
        for time_entry in time_entries:
            self._tag_time_entry(time_entry['id'])

    def _set_session(self):
        session = requests.Session()
        session.auth = (self.token, 'api_token')
        self.session = session

    def _build_url(self, **kwargs):
        category = kwargs.pop('category')
        separate_sign = kwargs.pop('separate_sign')
        parameters = self._get_parameters(separate_sign, **kwargs)
        url = '{base_url}{cat}{params}'.format(base_url=self.api_url, cat=category, params=parameters)
        return url

    def _format_date(self, date):
        formated_date = date.replace(':', '%3A').replace('+', '%2B').replace('-', '%2D')
        return formated_date

    def _get_parameters(self, separate_sign, **kwargs):
        if separate_sign == '/':
            return '/{id}'.format(id=kwargs.pop('id', ''))
        elif separate_sign == '?':
            return '?' + '&'.join(['{key}={value}'.format(key=kwarg, value=kwargs[kwarg]) for kwarg in kwargs])

    def _tag_time_entry(self, id):
        url = self._build_url(id=id, category='time_entries', separate_sign='/')
        return requests.post('{url}'.format(url=url))
