from bin_terminal_translater import setting

from typing import Tuple, List, Any, Dict
import configparser
import optparse
import requests
import os


def options_check(func):
    def run(argv: list):
        options, args = func(argv)
        if not options.language:
            print('language 参数为空，你需要通过-l 开关来指定它')
            # 修正装饰器，该退出方法可能引发错错误
            os._exit(1)
        else:
            return options, args
    return run


def read_inf(path: str) -> Dict[str, Dict[str, str]]:
    """读取配置文件"""
    cp = configparser.ConfigParser()
    cp.read(path)

    return dict([(i, dict(cp.items(i))) for i in cp.sections()])


@ options_check
def parser(argv: list) -> Tuple[Any, List[str]]:
    parser_conf = read_inf(setting.CONF_PARSER)

    parser = optparse.OptionParser()
    for option in parser_conf.keys():
        parser.add_option(
            *(F'-{option[0]}', F'--{option}'),
            **parser_conf[option]
        )
    return parser.parse_args(argv)


def translator(text: str, language_code: str = '') -> str:
    conf = read_inf(setting.CONF_PATH)
    conf['data']['text'] = text
    # url 数据结构问题 “url” 需要单独提取
    url = conf.pop('server').pop('url')
    if language_code:
        conf['data']['to'] = language_code

    try:
        response = requests.post(
            url=url,
            **conf
        )
        # TODO 写死的读取路径，可能引发错误
        return response.json()[0]['translations'][0]['text']
    except KeyError as er:
        raise KeyError(F'KEY:{str(er)}\n{response.json()}')
