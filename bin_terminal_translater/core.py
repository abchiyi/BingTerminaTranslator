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

    def __init__(self, response_obj: requests.Response):
        self.response = response_obj

    def __repr__(self):
        return self.text()

    def json(self):
        return self.response.json()

    def text(self):
        texts = []
        for item in self.response.json():
            for text_item in item['translations']:
                texts.append(text_item['text'])

        return ' '.join(texts)


class Translator:
    """必应翻译"""

    def __init__(self, tgt_lang: str, text: str = None, split: str = None,):
        def conf_seter():
            """处理数据模板"""
            # 读取配置
            conf = read_inf(setting.CONF_PATH)
            # 提取翻译接口地址
            conf['url'] = conf.pop('server').pop('translation_engine')
            if tgt_lang in read_inf(setting.LANGUAGE_CODE_PATH):
                conf['data']['to'] = tgt_lang
            else:
                raise errors.TargetLanguageNotSupported(
                    F"不支持的语言:{tgt_lang}"
                )
            return conf
        self.text = text
        self.response_type = '---'
        self.__split = []
        self.__sequence_str__(split)
        self.__conf__ = conf_seter()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def __str__(self):
        if self.text:
            return str(self.translator(self.text, self.__split))
        return self.__repr__()

    def __repr__(self):
        return str(
            F"<Translator {self.__conf__['data']['to']}-{self.response_type}>"
        )

    def __translator__(self, text: str) -> TextSeter:
        """翻译api"""
        conf = copy.deepcopy(self.__conf__)
        conf['data']['text'] = text

        # 请求翻译处理
        response = requests.post(**conf)
        self.response_type = response.status_code
        return TextSeter(response)

    def __sequence_str__(self, values):
        if values:
            values = [value.strip() for value in values]

            if isinstance(values, (list, tuple)):
                for value in values:
                    if value not in self.__split:
                        self.__split += list(value)
            else:
                if values not in self.__split:
                    self.__split.append(value)

    def translator(self,
                   text: str = "",
                   split: str = None,
                   ) -> str:
        """翻译方法"""
        def rep_str(value: str, srt: list) -> str:
            value_f = ' '.join(value.strip().split(srt.pop(0)))
            if srt:
                return rep_str(value_f, srt)
            return ' '.join(value_f.split())

        self.__sequence_str__(split)

        if text.strip():
            return self.__translator__(
                rep_str(text, self.__split.copy()) if self.__split else text)

        raise errors.EmptyTextError(F'无效的字符串:"{text}"')

    def json(self):
        """返回字典"""
        return self.translator(self.text, self.__split).json()
