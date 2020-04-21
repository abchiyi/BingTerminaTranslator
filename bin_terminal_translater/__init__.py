from bin_terminal_translater import core, setting
from pyperclip import paste, copy


def entrance(argv) -> str:
    parser = core.parser_generator(setting)
    options, args = parser.parse_args(argv)

    # 没有提供文本时从剪贴板获取
    r_text = ' '.join(args) if ' '.join(args) else paste()

    text = core.translator(setting, r_text, options.language.strip())

    if options.copy:
        copy(text)
    return text
