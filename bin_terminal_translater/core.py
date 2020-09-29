from bin_terminal_translater.public import errors
from bin_terminal_translater import setting
import requests
import bs4
import copy
import os
from configparser import ConfigParser, NoSectionError
from typing import Dict


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
    """读取配置文件"""
    c_p = ConfigParser()
    c_p.read(path, encoding='UTF-8')

    return {i: dict(c_p.items(i)) for i in c_p.sections()}


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
    conf_table = read_inf(setting.CONF_PATH)
    # 读取页面，并获取所有语言标签
    tgt_all_lang = bs4.BeautifulSoup(
        requests.get(conf_table['server']['home_page']).text,
        'html.parser'
    ).find(id='t_tgtAllLang').find_all('option')

    # 格式化为标准字典
    data = {i.attrs['value']: {'text': i.text} for i in tgt_all_lang}
    save_ini(setting.LANGUAGE_CODE_PATH, data)
    return data


class TextSeter:

    def __init__(self, tra):
        self.__tra__: Translator = tra

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

    def semantic(self) -> dict:
        return self.__tra__.__sematinc__(
            self.json()[0]['detectedLanguage']['language'], self.text()
        )


class Translator:
    """必应翻译"""

    def __init__(self, tgt_lang: str):
        def conf_seter():
            """处理数据模板"""
            # 读取配置
            conf = read_inf(setting.CONF_PATH)
            # 提取翻译接口地址
            conf['url'] = conf.pop('server').pop('translation_engine')
            if tgt_lang in read_inf(setting.LANGUAGE_CODE_PATH):
                conf['data']['to'] = tgt_lang
            else:
                raise errors.TargetLanguageNotSupported(tgt_lang)
            return conf
        self.language = tgt_lang
        self.__conf__ = conf_seter()
        self.response = requests.Response()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def __repr__(self):
        return str(
            F"<Translator({self.language})>"
        )

    def __net_post__(self, data):
        try:
            self.response = requests.post(**data)
            # FIXME 捕获所有错误
        except Exception:
            # FIXME 捕获错误后无动作
            pass

    def __sequence_str__(self, values: [str, list, tuple]) -> list:
        if values:
            if isinstance(values, str):
                return [values.strip()]
            return [value.strip() for value in values if isinstance(value, str)]
        return []

    def __sematinc__(self, from_language: str, text: str) -> dict:

        template = {
            'url': 'https://cn.bing.com/tlookupv3',
            'data': {
                'text': text,
                'to': self.language,
                'from': from_language,
            }
        }

        response = requests.post(**template)

        return {'to': self.language,
                'from': from_language,
                'semantic': [(i['displayTarget'], i['transliteration'])
                             for i in response.json()[0]['translations']]
                }

    def translator(self, text: str = '', split: str = None,) -> TextSeter:
        """翻译方法"""

        def rep_str(value: str, srt: list) -> str:
            for i in srt:
                value = ' '.join(value.replace(i, ' ').split())
            return value

        if text.strip():
            conf = copy.deepcopy(self.__conf__)
            conf['data']['text'] = rep_str(text, self.__sequence_str__(split))

            # 请求翻译处理
            self.__net_post__(conf)
            return TextSeter(self)

        raise errors.EmptyTextError(F'无效的字符串:"{text}"')
