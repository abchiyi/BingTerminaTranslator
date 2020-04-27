from bin_terminal_translater import setting

import configparser
import optparse
import requests


def __open_ini__(path) -> configparser.ConfigParser:
    cp = configparser.ConfigParser()
    cp.read(path)
    return cp


def parser_generator() -> optparse.OptionParser:
    cp = __open_ini__(setting.CONF_PARSER)
    parser_conf = dict([[i, dict(cp.items(i))] for i in cp.sections()])

    parser = optparse.OptionParser()
    for option in parser_conf.keys():
        parser.add_option(
            *(F'-{option[0]}', F'--{option}'),
            **parser_conf[option]
        )
    return parser


def translator(text, language_code=None) -> str:

    cp = __open_ini__(setting.CONF_PATH)

    dtb = dict([[i, dict(cp.items(i))] for i in cp.sections()])

    dtb['url'] = dtb.pop('server')['url']
    dtb['data']['text'] = text

    if language_code:
        dtb['data']['to'] = language_code

    try:
        response = requests.post(**dtb)
        return response.json()[0]['translations'][0]['text']
    except KeyError as er:
        raise KeyError(F'KEY:{str(er)}\n{response.json()}')


def options_check(func) -> str:
    def run(options):

        if not options.language:
            print('language 参数为空，你需要通过-l 开关来指定它')
        else:
            func(options)
    return run
