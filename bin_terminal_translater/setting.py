import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


CONF_PATH = os.path.join(BASE_DIR, 'ini/conf.ini')

CONF_PARSER = os.path.join(BASE_DIR, 'ini/parser.ini')

data_table = {
    "url": "https://cn.bing.com/ttranslatev3?isVertical=1&&IG=ECCC2E222205418FB249C51DB6C943BF&IID=translator.5028.1",
    "headers": {
           "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36 Edg/80.0.361.66"
    },
    'data': {
        "fromLang": "auto-detect",
        "to": "zh-Hans",
        "text": None
    }
}
