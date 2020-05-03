import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


CONF_PATH = os.path.join(BASE_DIR, 'ini/conf.ini')

CONF_PARSER = os.path.join(BASE_DIR, 'ini/parser.ini')

LANGUAGE_CODE_PATH = os.path.join(BASE_DIR, 'ini/language_code.ini')
