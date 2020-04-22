from bin_terminal_translater import setting

import configparser
import optparse
import requests
import json

cp = configparser.ConfigParser()


def parser_generator() -> optparse.OptionParser:
    cp.read(setting.CONF_PARSER)
    parser_conf = dict([[i, dict(cp.items(i))] for i in cp.sections()])

    parser = optparse.OptionParser()
    for option in parser_conf.keys():
        parser.add_option(
            *(F'-{option[0]}', F'--{option}'),
            **setting.parser_conf[option]
        )
    return parser


def translator(text, language_code) -> str:
    cp.read(setting.CONF_PATH)

    dtb = setting.data_table.copy()
    dtb['data']['to'] = language_code
    dtb['data']['text'] = text

    try:
        response = requests.post(**dtb)
        return response.json()[0]['translations'][0]['text']
    except KeyError as er:
        raise KeyError(F'KEY:{str(er)}\n{response.json()}')
