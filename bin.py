from bin_terminal_translater import core, public
from pyperclip import paste, copy

import argparse
import os


def parser(args) -> argparse.Namespace:
    a_p = argparse.ArgumentParser()
    # 位置参数
    a_p.add_argument('tgt_lang', help='Target tgt_lang')
    a_p.add_argument('text', nargs='*', default=None, help='some texts')
    # 可选参数
    a_p.add_argument('-c', '--copy', action='store_true',
                     help='Copy to the clipboard')
    a_p.add_argument('-d', '--debug', action='store_true',
                     help='DeBug Mode')
    a_p.add_argument('-s', '--split', nargs='*',
                     help='Specifies the text split character')

    return a_p.parse_args(args)


def entrance(argv: list):
    name_spece = parser(argv)
    if name_spece.debug:
        print(F'DeBugMode:\n\t{name_spece}')

    def f_translator():
        try:
            text = str(
                core.Translator(
                    name_spece.tgt_lang.strip(),
                    ' '.join(name_spece.text) or paste(),
                    name_spece.split
                )
            )
        except public.errors.EmptyTextError:
            return "待翻译文本为空!"
        # except public.errors.TargetLanguageNotSupported:
        #     return "不受支持的目标语言，你可以尝试更新语言代码"
        if name_spece.copy:
            copy(text)
        return text

    try:
        return f_translator()
    except public.errors.TargetLanguageNotSupported:
        # 假设语言标签不存在本地文件中，联网更新，重试
        core.update_language_code()
        print(F'不受支持的语言:< {name_spece.tgt_lang} >\n正在获取联网支持')
        return f_translator()


if __name__ == "__main__":
    print(entrance(os.sys.argv[1:]))
