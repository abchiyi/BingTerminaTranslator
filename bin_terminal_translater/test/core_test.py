import os
import time
import unittest

import requests
from faker import Faker
# from pyperclip import copy, paste

from .. import core, setting


class Translate(unittest.TestCase):
    def setUp(self):
        self.default_language = 'en'
        self.faker_data = Faker(locale='zh_CN')
        self.tar = core.Translator(self.default_language)

        # texts
        self.text = 'Hello'
        self.some_text = [self.faker_data.color_name()
                          for i in range(5)]
        self.color_names = [self.faker_data.color_name() for i in range(5)]

    def tearDown(self):
        pass

    def test_translator_with(self):
        tgt_lang = 'zh-Hans'
        with core.Translator(tgt_lang=tgt_lang) as translator:
            for text in [self.faker_data.color_name() for i in range(2)]:
                self.assertTrue(
                    isinstance(translator.translator(text).text(), str)
                )
                time.sleep(0.5)

    def test_split_string(self):
        """
        字符串包含翻译引擎无法识别的字符时,指定分割符,
        以及确保对象方法的参数有效
        """

        # 分割参数接受字符串
        t_text = self.tar.translator(
            text='_'.join(self.color_names),
            split='_'
        )

        self.assertEqual(
            t_text.text(),
            ' '.join(self.color_names),
            '功能：分割参数接受字符功能被破坏'
        )

        # 分割参数接受一个序列
        t_text = self.tar.translator(
            text='><'.join(self.color_names),
            split=('>', '<')
        )

        self.assertEqual(
            t_text.text(),
            ' '.join(self.color_names),
            '功能：分割参数接受序列功能被破坏'
        )

    def test_json(self):
        """测试json方法是否有效"""
        t_text = self.tar.translator(self.text)

        # 实际调用返回对象的 ‘.json’方法
        # TODO 即将被修改的参数格式
        self.assertTrue(
            isinstance(t_text.json(), list),
            t_text.json()
        )

    def test_semantic(self):

        semantic = self.tar.translator(self.text).semantic()

        for item in semantic:
            for i in item:
                self.assertTrue(isinstance(i, str))


class UpdateTgtLang(unittest.TestCase):

    def test_update_language_code_and_save(self):
        """更新语言 tgt"""
        tgt_lan_of_net_work = core.update_language_code()
        tgt_lag_of_file = core.read_inf(setting.LANGUAGE_CODE_PATH)

        self.assertEqual(tgt_lag_of_file, tgt_lan_of_net_work)


class Core(unittest.TestCase):

    def setUp(self):
        self.test_ini_path = os.path.join(setting.BASE_DIR_OUTSIDE, 'test.ini')
        # 翻译函数请求数据
        self.d_t = {
            "url": ''.join(['https://cn.bing.com/',
                            'ttranslatev3?isVertical=1&',
                            '&IG=ECCC2E222205418FB249C51DB6C943BF&',
                            'IID=translator.5028.1'
                            ]),
            "headers": {
                "user-agent": ' '.join([
                    'Mozilla/5.0',
                    '(Windows NT 10.0; Win64; x64)',
                    'AppleWebKit/537.36',
                    '(KHTML, like Gecko)',
                    'Chrome/80.0.3987.132 Safari/537.36 Edg/80.0.361.66'
                ])
            },
            'data': {
                "fromLang": "auto-detect",
                "to": "zh-Hans",
                "text": None
            }
        }

    def translator(self, text, lang_code):
        """翻译函数接口"""
        self.d_t["data"]["text"] = text
        self.d_t["data"]["to"] = lang_code
        res = requests.post(**self.d_t).json()
        try:
            return res[0]['translations'][0]['text']
        except KeyError as error:
            print(res)
            raise error

    def test_base_dir_and_file(self):
        self.assertTrue(os.path.exists(setting.BASE_DIR_INSIDE),
                        F"Not Found FIle of Fir :{setting.BASE_DIR_INSIDE}")
        self.assertTrue(os.path.exists(setting.CONF_PATH),
                        F'Not Found File or Dir :{setting.CONF_PATH}')

    def test_read_inf(self):
        self.assertEqual(type(core.read_inf(setting.CONF_PATH)), dict)
        self.assertEqual(type(core.read_inf(setting.LANGUAGE_CODE_PATH)), dict)

    def test_can_save_setting(self):
        path = self.test_ini_path
        try:
            data_table1 = {'test': {'test1': 'test2'}}
            core.save_ini(path, data_table1)
            self.assertEqual(data_table1, core.read_inf('test.ini'))

            data_table2 = {'test3': {'test4': 'test5'}}
            core.save_ini(path, data_table2)
            self.assertIn('test3', core.read_inf(path))
            self.assertIn('test', core.read_inf(path))

        finally:
            os.system(F'del {path}')


if __name__ == "__main__":
    unittest.main()
