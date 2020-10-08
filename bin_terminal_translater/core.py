import os
from configparser import ConfigParser, NoSectionError
from typing import Dict
import collections

import bs4
import requests

from bin_terminal_translater import setting
from .public import errors


def file_check(func):
    def run(path, *argv, **kwargs):
        if os.access(path, os.F_OK) and os.access(path, os.R_OK):
            return func(path, *argv, **kwargs)
        raise errors.FileError(
            F'没有找到配置文件，或文件不可访问： \n{path}'
        )

    return run


def language_check(func):
    """检查语言是否在支持列表内"""

    def run(self, tolang, *args, **kwargs):
        if tolang not in Conf.read_inf(setting.LANGUAGE_CODE_PATH):
            raise errors.TargetLanguageNotSupported(tolang)
        return func(self, tolang, *args, **kwargs)

    return run


def save_ini(path: str, data_table: Dict[str, Dict[str, str]]):
    c_p = ConfigParser()
    c_p.read(path, encoding='UTF-8')

    for section in data_table.keys():
        for option in data_table[section].keys():
            try:
                c_p.set(section, option, data_table[section][option])
            except NoSectionError:
                c_p.add_section(section)
                c_p.set(section, option, data_table[section][option])

    with open(path, 'w', encoding='UTF-8') as file:
        c_p.write(file)


def update_language_code():
    """语言代码更新"""
    # 读取配置
    conf_table = Conf.read_inf(setting.CONF_PATH)
    # 读取页面，并获取所有语言标签
    tgt_all_lang = bs4.BeautifulSoup(
        requests.get(conf_table['server']['home_page']).text,
        'html.parser'
    ).find(id='t_tgtAllLang').find_all('option')

    # 格式化为标准字典
    data = {i.attrs['value']: {'text': i.text} for i in tgt_all_lang}
    save_ini(setting.LANGUAGE_CODE_PATH, data)
    return data


class Conf:

    def __init__(self):
        self.__conf__ = self.read_inf(setting.CONF_PATH)

    @staticmethod
    @file_check
    def read_inf(path: str) -> Dict[str, Dict[str, str]]:
        """读取配置文件"""
        c_p = ConfigParser()
        c_p.read(path, encoding='UTF-8')

        return {i: dict(c_p.items(i)) for i in c_p.sections()}

    @staticmethod
    def save_ini(path: str, data_table: Dict[str, Dict[str, str]]):
        c_p = ConfigParser()
        c_p.read(path, encoding='UTF-8')

        for section in data_table.keys():
            for option in data_table[section].keys():
                try:
                    c_p.set(section, option, data_table[section][option])
                except NoSectionError:
                    c_p.add_section(section)
                    c_p.set(section, option, data_table[section][option])

        with open(path, 'w', encoding='UTF-8') as file:
            c_p.write(file)

    def template_of_translator(self, fromlang, tolang, text) -> dict:
        return {
            'url': self.__conf__['server']['translator'],
            'headers': self.__conf__['headers'],
            'params': self.__conf__['params'],
            'data': {
                'fromLang': fromlang,
                'to': tolang,
                'text': text,
            }
        }

    def template_of_semantic(self, fromlang, tolang, text):
        return {
            'url': self.__conf__['server']['semantic'],
            'headers': self.__conf__['headers'],
            'params': self.__conf__['params'],
            'data': {
                'from': fromlang,
                'to': tolang,
                'text': text,
            }
        }


SemanticItem = collections.namedtuple('SemanticItem', ['text', 'semantic'])


class Semantic:

    def __init__(self, from_lang, to_lang, reper_text):
        self.reper_text = reper_text
        self.from_lang = from_lang
        self.to_lang = to_lang

        template = Conf().template_of_semantic(
            fromlang=from_lang,
            text=reper_text,
            tolang=to_lang,
        )

        self.__data__ = requests.post(
            **template
        ).json()[0]['translations']

    def __repr__(self):
        return F'"{self.reper_text}"({self.from_lang})-->({self.to_lang})'

    def text(self) -> str:
        data = self.json()['semantic']
        text = '\n'.join([F'{k}:{",".join(v)}' for k, v in data.items()])
        return text

    def json(self) -> dict:
        semantics = {}
        for i in self.__data__:
            temp = []
            for i_i in i['backTranslations']:
                temp.append(i_i['displayText'])
            semantics[i['displayTarget']] = temp
        return {
            'from': self.from_lang,
            'semantic': semantics,
            'to': self.to_lang
        }

    def __getitem__(self, key):
        item = self.__data__[key]
        return SemanticItem(
            item['displayTarget'],
            [i['displayText'] for i in item['backTranslations']]
        )


class Text:

    def __init__(self, tra, reper_text):
        self.__tra__: Translator = tra
        self.reper_text = reper_text

    def __repr__(self):
        return self.text()

    def json(self) -> dict:
        return self.__tra__.response.json()

    def text(self) -> str:
        texts = []
        for item in self.__tra__.response.json():
            for text_item in item['translations']:
                texts.append(text_item['text'])

        return ' '.join(texts)

    def semantic(self) -> Semantic:
        return Semantic(
            self.json()[0]['detectedLanguage']['language'],
            self.__tra__.tolang,
            self.reper_text
        )


class Translator:
    """必应翻译"""
    @ language_check
    def __init__(self, tolang: str, fromlang='auto-detect'):
        self.tolang = tolang
        self.fromlang = fromlang
        self.response = requests.Response()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def __repr__(self):
        return str(
            F"<Translator({self.tolang})>"
        )

    def __net_post__(self, data):
        try:
            self.response = requests.post(**data)
        except requests.ConnectionError:
            raise ConnectionError('连接错误-请检查你的网络')

    def translator(self,
                   text: str = '',
                   exclude_s: [str, list, tuple] = None) -> Text:
        """翻译方法"""

        def format_text(strings, texts) -> str:
            """格式化字符串"""

            if isinstance(strings, str):
                strings = [strings.strip()]
            elif isinstance(strings, (list, tuple)):
                strings = [value.strip()
                           for value in strings if isinstance(value, str)]
            else:
                strings = []

            for i in strings:
                texts = ' '.join(texts.replace(i, ' ').split())
            return texts

        if text.strip():

            self.__net_post__(
                Conf().template_of_translator(
                    text=format_text(exclude_s, text),
                    fromlang=self.fromlang,
                    tolang=self.tolang,
                ))

            return Text(self, text)

        raise errors.EmptyTextError(F'无效的字符串:"{text}"')
