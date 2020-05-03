from bin_terminal_translater import setting

from typing import Tuple, List, Any, Dict
from bs4 import BeautifulSoup as bs
import configparser
import optparse
import requests


def read_inf(path: str) -> Dict[str, Dict[str, str]]:
    """读取配置文件"""
    cp = configparser.ConfigParser()
    cp.read(path)

    return dict([(i, dict(cp.items(i))) for i in cp.sections()])


def save_ini(path: str, data_table: Dict[str, Dict[str, str]]):
    cp = configparser.ConfigParser()

    for i in data_table.keys():
        cp[i] = data_table[i]

    with open(path, 'w') as f:
        cp.write(f)


def parser(argv: list) -> Tuple[Any, List[str]]:
    parser_conf = read_inf(setting.CONF_PARSER)

    parser = optparse.OptionParser()
    for option in parser_conf.keys():
        parser.add_option(
            *(F'-{option[0]}', F'--{option}'),
            **parser_conf[option]
        )
    return parser.parse_args(argv)


def translator(text: str, language_code: str = '') -> str:
    conf = read_inf(setting.CONF_PATH)
    conf['data']['text'] = text
    # url 数据结构问题 “url” 需要单独提取
    url = conf.pop('server').pop('url')
    if language_code:
        conf['data']['to'] = language_code

    try:
        response = requests.post(
            url=url,
            **conf
        )
        # TODO 写死的读取路径，可能引发错误
        return response.json()[0]['translations'][0]['text']
    except KeyError as er:
        raise KeyError(F'KEY:{str(er)}\n{response.json()}')


def update_language_code() -> Dict[str, Dict[str, str]]:
    """语言代码更新"""
    language_code_table = read_inf(setting.LANGUAGE_CODE_PATH)
    soup = bs(
        requests.get(language_code_table['url']['url']).text,
        'html.parser'
    )
    all_language = soup.find(id='t_tgtAllLang').find_all('option')

    return dict([(i.attrs['value'], dict([('text', i.text)])) for i in all_language])
