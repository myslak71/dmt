import logging
import os
import sys
from logging import config

import yaml

if getattr(sys, 'frozen', False):
    DIR_PATH = sys._MEIPASS
else:
    DIR_PATH = os.path.dirname(os.path.abspath(__file__))

config.dictConfig(yaml.load(open(os.path.join(DIR_PATH, 'LOGGER.yaml'))))
LOGGER = logging.getLogger('dmt_logger')

TOGGL_API_URL = 'https://www.toggl.com/api/v8/'
