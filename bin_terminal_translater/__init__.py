from pyperclip import paste, copy
from bin_terminal_translater.core import Translator
from bin_terminal_translater.public import errors
from bin_terminal_translater import core


def entrance(argv: list):
    name_spece = core.parser(argv)
    # 翻译块
    if name_spece.language:
        # 没有提供文本时从剪贴板获取
        tgt_lang, *r_text = name_spece.language.split()
        long_text = ' '.join(r_text) if r_text else paste()
        try:
            text = str(
                Translator(
                    tgt_lang,
                    long_text,
                    name_spece.split
                )
            )
        except errors.EmptyTextError:
            return "空文本"
        except errors.TargetLanguageNotSupported:
            return "不受支持的目标语言，你可以尝试更新语言代码"
        if name_spece.copy:
            copy(text)
        return text

    elif not name_spece.update:
        return "你需要指定 -l language 参数来翻译到该语言"

    # 语言代码更新块
    if name_spece.update:
        core.update_language_code()
        return "更新完毕"
