from bin_terminal_translater.core import Semantic
from typing import Text
from bin_terminal_translater import core, public
from pyperclip import paste, copy
from pathlib import Path

import argparse
import tqdm
import os


def parser(args) -> argparse.Namespace:
    a_p = argparse.ArgumentParser(
        prog='bin',
        usage='%(prog)s tgt_lang [text] [optionals]',
    )
    # 位置参数 #
    # 语言类型
    a_p.add_argument('tgt_lang', help='Target tgt_lang', default='zh-Hans')
    # 文本，接受多个参数
    a_p.add_argument('text', nargs='*', default=None, help='some texts')
    # 可选参数 #
    # 复制输出内容
    a_p.add_argument('-c', '--copy', action='store_true',
                     help='Copy to the clipboard')
    # de bug 模式
    a_p.add_argument('-d', '--debug', action='store_true',
                     help='DeBug Mode')
    # 移除指定字符串， 接受多个参数
    a_p.add_argument('-s', '--split', nargs='*',
                     help='Specifies the text split character')
    # 以当前指定语言模式列出所有语言标签
    a_p.add_argument('-l', '--list_all_ltgt', action='store_true',
                     help='List all languages')

    a_p.add_argument("--script", action='store_true', help='make script')

    return a_p.parse_args(args)


def make_script(tgt_lang):
    file_path = F'./scripts/{tgt_lang}.ps1'
    # FIXME 当前仅对windows做支持
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(F'bin {tgt_lang} $args')

    if not Path(file_path).is_file():
        raise Exception(F"Fall Make Script {tgt_lang}")


def f_translator(name_spece):
    tra = core.Translator(name_spece.tgt_lang.strip())
    try:
        # 文本主体
        text_obj = tra.translator(
            # 分别从name_spece 和 paste中获取文本，name_space 优先
            ' '.join(name_spece.text) or paste(),
            name_spece.split
        )

        # 详细释义
        semantic = text_obj.semantic()

        if semantic:
            text = F"{str(text_obj)}\n{'-='*20}\n{semantic.text()}"
        else:
            text = text_obj.text()

        if name_spece.copy:
            copy(text)

        return text

    except public.errors.EmptyTextError:
        return "待翻译文本为空!"
    except public.errors.EqualTextLanguage:
        # 在获取 semantic 时可能出现的错误
        pass


def all_tgt(name_spece):
    all_l_tgt = core.Conf.read_inf(core.setting.LANGUAGE_CODE_PATH)
    tqdm_keys = tqdm.tqdm(all_l_tgt.keys())
    base_language = name_spece.tgt_lang.strip()
    temp = []

    for key in tqdm_keys:
        tqdm_keys.set_description(F'{key}>>>>>{base_language}')
        i18_tgt = core.Translator(base_language).translator(
            all_l_tgt[key]['text']
        )

        temp.append(F"language tgt:[{key}] {i18_tgt}\n")

    return ''.join(temp)


def entrance(argv: list):
    """翻译入口"""
    name_spece = parser(argv)
    # debug mode
    if name_spece.debug:
        print(F'DeBugMode:\n\t{name_spece}')
    # 列出所有语言标签
    if name_spece.list_all_ltgt:
        return all_tgt(name_spece)
    # 制作单一

    if name_spece.script:
        return make_script(name_spece.tgt_lang.strip())

    # 翻译给出的文本
    try:
        return f_translator(name_spece)
    except public.errors.TargetLanguageNotSupported:
        # 假设语言标签不存在本地文件中，联网更新，重试
        print(
            F'不受支持的语言:<{name_spece.tgt_lang}>\n正在获取联网支持...'
        )
        core.update_language_code()
        try:
            return f_translator(name_spece)
        except public.errors.TargetLanguageNotSupported:
            return F"不支持的语言:‘{name_spece.tgt_lang}’\n你可以使用‘-l’选项查看语言支持列表"


if __name__ == "__main__":
    if len(os.sys.argv) < 2:
        entrance(['-h'])
    else:
        print(entrance(os.sys.argv[1:]))
