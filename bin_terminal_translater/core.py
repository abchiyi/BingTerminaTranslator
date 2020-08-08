import argparse
import os
from configparser import ConfigParser, NoSectionError
from typing import Tuple, List, Any, Dict

import copy
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


def parser(argv: list) -> argparse.Namespace:
    parser_conf = read_inf(setting.CONF_PARSER)

    a_p = argparse.ArgumentParser()
    for option in parser_conf.keys():
        a_p.add_argument(
            *(F'-{option[0]}', F'--{option}'),
            **parser_conf[option]
        )
    return a_p.parse_args(argv)


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
    # 保存


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
            # 读取请求配置

            return conf
        self.text = text
        self.__split = split
        self.__conf__ = conf_seter()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def __str__(self, text=None, tgt_lang=None):
        if self.text:
            return self.translator(self.text or text, self.__split)
        return self.__repr__()

    def __repr__(self):
        return str(F"<Translator {self.__conf__['data']['to']}>")

    def __translator__(self, text: str) -> str:
        """翻译api"""
        conf = copy.deepcopy(self.__conf__)
        conf['data']['text'] = text
        # 请求翻译处理
        response = requests.post(**conf)
        try:
            # FIXME 固定读取路径，可能引发错误
            return response.json()[0]['translations'][0]['text']
        except KeyError as error:
            raise KeyError(F'KEY:{str(error)} not found in {response.json()}')

    def translator(self, text: str = "", split: str = None,) -> str:
        """翻译方法"""
        if text.strip():
            return self.__translator__(
                ' '.join(text.strip().split(split)),
            )
        raise errors.EmptyTextError(F'无效的字符串:"{text}"')

    def json(self):
        """返回字典"""
