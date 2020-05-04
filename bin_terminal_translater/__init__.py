from pyperclip import paste, copy
from bin_terminal_translater import core


def entrance(argv: list):
    options, args = core.parser(argv)
    # 翻译块
    if options.language:
        # 没有提供文本时从剪贴板获取
        r_text = ' '.join(args) if ' '.join(args) else paste()
        text = core.translator(r_text, options.language.strip())
        if options.copy:
            copy(text)
        return text

    elif not options.update:
        return "你需要指定 -l language 参数来翻译到该语言"

    # 语言代码更新块
    if options.update:
        core.update_language_code()
