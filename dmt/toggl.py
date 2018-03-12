import requests


class Toggl(object):
    def __init__(self, api_url, token):
        self.toggl = BaseToggl().setup_toggl(api_url, token)

    def get_time_entries(self, start_time='', end_time=''):
        return self.toggl.get_time_entries(start_time=start_time, end_time=end_time)


class BaseToggl(object):
    def setup_toggl(self, api_url, token):
        self.api_url = api_url
        self.token = token
        self._set_session()
        return self

    def get_time_entries(self, start_time='', end_time=''):
        url = self._build_url(start_date=start_time, end_date=end_time, category='time_entries')
        return self.session.get(url).json()

    def _set_session(self):
        session = requests.Session()
        session.auth = (self.token, 'api_token')
        self.session = session

    def _build_url(self, **kwargs):
        category = kwargs.pop('category')
        parameters = '&'.join(['{}={}'.format(kwarg, self._format_date(kwargs[kwarg])) for kwarg in kwargs])
        url = '{base_url}{cat}?{params}'.format(base_url=self.api_url, cat=category, params=parameters)
        return url

    def _format_date(self, date):
        formated_date = date.replace(':', '%3A').replace('+', '%2B').replace('-', '%2D')
        return formated_date
