import optparse
import os
from configparser import ConfigParser, NoSectionError
from typing import Tuple, List, Any, Dict

import bs4
import requests

from bin_terminal_translater import setting
from bin_terminal_translater.public import errors


def file_check(func):
    def run(path, *argv, **kwargs):
        if os.access(path, os.F_OK) and os.access(path, os.R_OK):
            return func(path, *argv, **kwargs)
        raise errors.FileError(
            F'没有找到配置文件，或文件不可访问： \n{path}'
        )

    return run


@file_check
def read_inf(path: str) -> Dict[str, Dict[str, str]]:
    # """读取配置文件""" b  m,
    cp = ConfigParser()
    cp.read(path, encoding='UTF-8')
    s = {i: dict(cp.items(i)) for i in cp.sections()}

    # s = dict([(i, dict(cp.items(i))) for i in cp.sections()])
    return s


def save_ini(path: str, data_table: Dict[str, Dict[str, str]]):
    cp = ConfigParser()
    cp.read(path, encoding='UTF-8')

    for section in data_table.keys():
        for option in data_table[section].keys():
            try:
                cp.set(section, option, data_table[section][option])
            except NoSectionError:
                cp.add_section(section)
                cp.set(section, option, data_table[section][option])

    with open(path, 'w', encoding='UTF-8') as f:
        cp.write(f)


def parser(argv: list) -> Tuple[Any, List[str]]:
    parser_conf = read_inf(setting.CONF_PARSER)

    p = optparse.OptionParser()
    for option in parser_conf.keys():
        p.add_option(
            *(F'-{option[0]}', F'--{option}'),
            **parser_conf[option]
        )
    return p.parse_args(argv)


def translator(text: str, language_code: str = '') -> str:
    conf = read_inf(setting.CONF_PATH)
    conf['data']['text'] = text
    # url 数据结构问题 “url” 需要单独提取
    url = conf.pop('server').pop('translation_engine')
    if language_code:
        conf['data']['to'] = language_code
    response = requests.post(url, **conf)
    try:
        # TODO 写死的读取路径，可能引发错误
        return response.json()[0]['translations'][0]['text']
    except KeyError as error:
        raise KeyError(F'KEY:{str(error)} not found in {response.json()}')


def update_language_code():
    """语言代码更新"""
    conf_table = read_inf(setting.CONF_PATH)

    soup = bs4.BeautifulSoup(
        requests.get(conf_table['server']['home_page']).text,
        'html.parser'
    )
    all_language = soup.find(id='t_tgtAllLang').find_all('option')

    data = {i.attrs['value']: {'text': i.text} for i in all_language}

    save_ini(setting.LANGUAGE_CODE_PATH, data)


class Translator:
    """必应翻译"""

    def __init__(self,
                 language_code: str,
                 text: str = None,
                 split: str = None,
                 insert: str = None
                 ):
        self.text = text
        self.__split = split
        self.__insert = insert

        if language_code in read_inf(setting.LANGUAGE_CODE_PATH):
            self.language_code = language_code
        else:
            raise errors.TargetLanguageNotSupported(
                F"不支持的语言:{language_code}"
            )

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def __str__(self):
        if self.text:
            return self.translator(self.text, self.__split, self.__insert)
        return self.__repr__()

    def __repr__(self):
        return str(F"<Translator {self.language_code}>")

    def translator(self,
                   text: str = "",
                   split: str = None,
                   insert: str = None
                   ) -> str:
        if not text.strip():
            raise errors.EmptyTextError(F'无效的字符串:"{text}"')

        return translator(
            text.strip().replace(split or '', insert or ''),
            self.language_code)
