import optparse
import requests


def parser_generator(setting) -> optparse.OptionParser:
    parser = optparse.OptionParser()
    for option in setting.parser_conf.keys():
        parser.add_option(
            *(F'-{option[0]}', F'--{option}'),
            **setting.parser_conf[option]
        )
    return parser


def translator(setting, text, language_code) -> str:
    dtb = setting.data_table.copy()
    dtb['data']['to'] = language_code
    dtb['data']['text'] = text

    try:
        response = requests.post(**dtb)
        return response.json()[0]['translations'][0]['text']
    except KeyError as er:
        raise KeyError(F'KEY:{str(er)}\n{response.json()}')
