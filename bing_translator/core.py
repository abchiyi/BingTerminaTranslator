from bing_translation_for_python import core, public, setting
from pyperclip import paste, copy

import argparse
import tqdm
import os


def parser(args) -> argparse.Namespace:
    a_p = argparse.ArgumentParser(
        prog='bin',
        usage='%(prog)s lang_tag [text] [optionals]',
    )
    # 位置参数 #
    # 语言类型
    a_p.add_argument('lang_tag', help='Target lang_tag', default='zh-Hans')
    # 文本，接受多个参数
    a_p.add_argument('text', nargs='*', default=None, help='some texts')

    # 可选参数 #
    # 复制输出内容
    a_p.add_argument('-c', '--copy', action='store_true',
                     help='Copy to the clipboard')
    # 以当前指定语言模式列出所有语言标签
    a_p.add_argument('-l', '--list_all_ltgt', action='store_true',
                     help='List all languages')
    # de bug 模式
    a_p.add_argument('-d', '--debug', action='store_true',
                     help='DeBug Mode')

    return a_p.parse_args(args)

def translator(name_spece):
    lang_tag = name_spece.lang_tag.strip()
    # 分别从name_spece 和 paste中获取文本，name_space 优先
    reper_text = ' '.join(name_spece.text) or paste()

    try:
        # 文本主体
        text_obj = core.Translator(lang_tag).translator(reper_text)
        try:
            # 如果文本是一个单词就能够获取到它的详细释义
            semantic = text_obj.semantic()

        # 需要在这里注意等同语言错误,在把英语翻译到英语这样的情况时它会出现
        # 你无法获取英语翻译为英语的解释意思
        except public.errors.EqualTextLanguage:
                print(F"文本'{reper_text}'已是'{lang_tag}'类型，无需翻译")
        else:
            if semantic:
                return F"{str(text_obj)}\n{'-='*20}\n{semantic.text()}"

        return text_obj.text()

        if name_spece.copy:
            # copy选项仅翻译后的文本
            copy(text_obj.text())


    # 这出现在控制台和终端都没有获取到有效的文本时
    except public.errors.EmptyTextError:
        return "待翻译文本为空!"

def list_language_tag(name_spece):
    # FIXME 转换翻译过于耗时
    all_l_tgt = setting.Config().tgt_lang
    tqdm_keys = tqdm.tqdm(all_l_tgt.keys())
    base_language = name_spece.lang_tag.strip()
    temp = []

    for key in tqdm_keys:
        tqdm_keys.set_description(F'{key}>>>>>{base_language}')
        i18_tgt = core.Translator(base_language).translator(
            all_l_tgt[key]['text']
        )

        temp.append(F"language tgt:[{key}] {i18_tgt}\n")

    return ''.join(temp)

def default_help(argv):
    # 没有有效参数时,默认显示帮助信息
    if argv:
        return argv
    return ['-h']

def entrance(args: list = None):
    """翻译入口"""
    if not args:
        args = os.sys.argv[1:]
    name_spece = parser(default_help(args))

    # 列出所有语言标签
    if name_spece.list_all_ltgt:
        return list_language_tag(name_spece)
    # 翻译给出的文本
    try:
        return translator(name_spece)
    except public.errors.TargetLanguageNotSupported:
            print(F"不支持的语言:'{name_spece.lang_tag}'")
            print("你可以使用‘-l’选项查看语言支持列表")
    finally:
        # debug mode
        if name_spece.debug:
            print(F'DeBugMode:\n\t{name_spece}\n\tArgs:{args}')
            print(F'\tRunningPath:{os.getcwd()}')
