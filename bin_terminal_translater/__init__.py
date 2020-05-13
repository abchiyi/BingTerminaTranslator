from pyperclip import paste, copy
from bin_terminal_translater.core import Translator
from bin_terminal_translater.public import errors
from bin_terminal_translater import core


def entrance(argv: list):
    print(__file__)
    options, args = core.parser(argv)
    # 翻译块
    if options.language:
        # 没有提供文本时从剪贴板获取
        r_text = ' '.join(args) if ' '.join(args) else paste()
        language_code = options.language.strip()
        try:
            text = str(Translator(language_code, r_text))
        except errors.EmptyTextError:
            return "空文本"
        except errors.TargetLanguageNotSupported:
            return "不受支持的目标语言，你可以尝试更新语言代码"
        if options.copy:
            copy(text)
        return text

    elif not options.update:
        return "你需要指定 -l language 参数来翻译到该语言"

    # 语言代码更新块
    if options.update:
        core.update_language_code()
        return "更新完毕"
