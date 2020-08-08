import os
import time
import unittest
from typing import List

import requests
from faker import Faker
from pyperclip import copy, paste

from bin_terminal_translater import core, setting, entrance
from bin_terminal_translater.public import errors


class Entrance(unittest.TestCase):
    """old test"""

    def setUp(self):
        self.argv = ["-l", "zh-Hans Hello world"]

    def test_can_copy_it(self):
        """测试是否能正确读写剪贴板"""
        or_text = 'hello copy program'
        # 向剪贴板写入待读取文本
        copy(or_text)
        # 从剪贴板读取,并将结果写回剪贴板
        entrance('-l zh-Hans -c '.split())
        # 清空剪贴板
        self.assertNotEqual(paste(), or_text)

    def test_not_support_language_code(self):
        # 语言代码验证功能，指出不支持该语言代码
        text = '不受支持的目标语言，你可以尝试更新语言代码'
        self.assertEqual(text, entrance(['-l sssssssss']))

    def test_split_string(self):
        text = ['hello', 'world']
        self.assertEqual(
            entrance(['-l', 'en ' + '_'.join(text), '-s_']),
            ' '.join(text)
        )


class Translate(unittest.TestCase):
    def setUp(self):
        self.default_language = 'en'
        self.faker_data = Faker(locale='zh_CN')

        self.some_text: List[str, ] = [self.faker_data.color_name()
                                       for i in range(5)]

    def tearDown(self):
        pass

    def test_translator_with(self):
        tgt_lang = 'zh-Hans'
        with core.Translator(tgt_lang=tgt_lang) as translator:
            for text in [self.faker_data.color_name() for i in range(2)]:
                self.assertTrue(
                    isinstance(translator.translator(text), str)
                )
                time.sleep(0.5)

    def test_not_support_error(self):
        """在给出不受支持的目标语言代码时抛出错误"""
        try:
            core.Translator(tgt_lang='ssssssss')
        except errors.TargetLanguageNotSupported:
            pass
        else:
            self.fail('没有捕获到应该出现的错误')

    def test_self_string(self):
        """Translator对象自身可直接转化为字符串"""
        text = self.faker_data.name()
        str(core.Translator(self.default_language, text))

    def test_split_string(self):
        """
        字符串包含翻译引擎无法识别的字符时,指定分割符,
        以及确保对象方法的参数有效
        """
        text = ' '.join([self.faker_data.color_name() for i in range(5)])
        self.assertEqual(
            text,
            str(
                core.Translator(
                    'en',
                    text.replace(' ', '_'),
                    '_'
                )
            )
        )

        text = text.replace(' ', '_')
        translater = core.Translator('en', text, '_')
        self.assertNotEqual(
            translater,
            translater.translator(text, ' ')
        )

    def test_empty_text_error(self):
        """在没有给出文本时的错误"""
        try:
            print(
                core.Translator(
                    tgt_lang=self.default_language
                ).translator('  '))
        except errors.EmptyTextError:
            pass
        else:
            self.fail("没有捕获到应出现的错误")

    def test_space_characters(self):
        """字符为一个空格时的处理方式应按照无效字符处理"""
        text = " "
        if text:
            try:
                str(core.Translator('zh-Hans', text))
            except errors.EmptyTextError:
                pass
            else:
                self.fail("未捕获到应该出现的错误")


class ErrorsTest(unittest.TestCase):

    def test_file_notfound(self):
        """配置文件读函数在找不到文件时抛出错误"""
        try:
            path = './sr.ini'
            os.system(F'del {path}')
            core.read_inf(path)
        except errors.FileError:
            pass
        else:
            self.fail('应该出现的错误')


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
        self.assertTrue(os.path.exists(setting.CONF_PARSER),
                        F'Not Found File or Dir :{setting.CONF_PARSER}')

    def test_read_inf(self):
        self.assertEqual(type(core.read_inf(setting.CONF_PARSER)), dict)
        self.assertEqual(type(core.read_inf(setting.CONF_PATH)), dict)

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
