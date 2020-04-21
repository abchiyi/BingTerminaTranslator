from bin_terminal_translater import core, setting


def entrance(argv) -> str:
    parser = core.parser_generator(setting)
    # parser.add_option('-l', '--language', action='store')

    options, args = parser.parse_args(argv)

    return core.translator(setting, ' '.join(args), options.language.strip())
