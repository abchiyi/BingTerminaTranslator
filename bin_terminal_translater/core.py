from bin_terminal_translater import setting
from bin_terminal_translater.public import errors

from configparser import ConfigParser, NoSectionError
from typing import Tuple, List, Any, Dict
from bs4 import BeautifulSoup as bs
import optparse
import requests
import os


def file_check(func):
    def run(path, *argv, **kwargs):
        if os.access(path, os.F_OK) and (
            os.access(path, os.R_OK) and os.access(path, os.W_OK)
        ):
            return func(path, *argv, **kwargs)
        else:
            raise errors.FileError('没有找到配置文件，或文件不可访问')
    return run


def read_inf(path: str) -> Dict[str, Dict[str, str]]:
    """读取配置文件"""
    cp = ConfigParser()
    cp.read(path, encoding='UTF-8')

    return dict([(i, dict(cp.items(i))) for i in cp.sections()])


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
    url = conf.pop('server').pop('translation_engine')
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


def update_language_code(debug=False):
    """语言代码更新"""
    conf_table = read_inf(setting.CONF_PATH)

    soup = bs(
        requests.get(conf_table['server']['home_page']).text,
        'html.parser'
    )
    all_language = soup.find(id='t_tgtAllLang').find_all('option')

    data = dict([
        (i.attrs['value'], dict([('text', i.text)]))
        for i in all_language
    ])

    save_ini(setting.LANGUAGE_CODE_PATH, data)

    if debug:
        return data


class Translator:

    def __init__(self,
                 language_code: str,
                 text: str = "",
                 split: str = "",
                 insert: str = ""
                 ):
        self.text = text
        self.__split = split
        self.__insert = insert
        self.language_code = self.__language_code_check__(language_code)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def __str__(self):
        return self.teranslater()

    def __repr__(self):
        return str(F"<Translator {self.language_code}>")

    def __language_code_check__(self, language_code) -> str:
        if language_code not in read_inf(setting.LANGUAGE_CODE_PATH):
            raise errors.TargetLanguageNotSupported(
                F"不支持的语言:{language_code}"
            )
        else:
            return language_code

    def __text_check__(self, text):
        text = text.strip()
        if (type(text) != str) or(not text):
            raise errors.EmptyTextError(
                F"参数类型不正确或者为空: text:'{self.text}'"
            )
        else:
            return text

    def teranslater(self,
                    text: str = "",
                    split: str = "",
                    insert: str = ""
                    ) -> str:
        # TODO 期待指定的额外参数只生效一次
        text = self.__text_check__(text if text else self.text)
        split = split if split else self.__split
        insert = insert if insert else self.__insert

        if (self.__split or self.__insert):
            return translator(
                text.replace(split, (insert or " ")),
                self.language_code)
        else:
            return translator(text, self.language_code)
