from pyperclip import paste, copy
from bin_terminal_translater import core


def entrance(argv) -> str:
    parser = core.parser_generator()
    options, args = parser.parse_args(argv)

    # 没有提供文本时从剪贴板获取
    r_text = ' '.join(args) if ' '.join(args) else paste()

    text = core.translator(r_text, options.language.strip())

    # 命令参数执行
    if options.copy:
        copy(text)
    return text
