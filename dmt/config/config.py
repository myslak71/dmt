import logging
import os
from logging import config

import yaml

DIR_PATH = os.path.dirname(os.path.abspath(__file__))

config.dictConfig(yaml.load(open(os.path.join(DIR_PATH, 'LOGGER.yaml'))))
LOGGER = logging.getLogger('dmt_logger')

TOGGL_API_URL = 'https://www.toggl.com/api/v8/'
