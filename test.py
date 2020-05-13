from bin_terminal_translater import core, setting, entrance
from bin_terminal_translater.public import errors
from faker import Faker
import unittest
import requests
import time
import os
from typing import List
import optparse


class Main_test(unittest.TestCase):
    """old test"""

    def setUp(self):
        self.test_ini_path = os.path.join(setting.BASE_DIR_OUTSIDE, 'test.ini')

    def tearDown(self):
        pass

    def check_ini_data(self, data):
        if type(data.popitem()[1]) == dict:
            return True
        return False

    def transelator(self, text, lang_code):
        try:
            dtb = {
                "url": "https://cn.bing.com/ttranslatev3?isVertical=1&&IG=ECCC2E222205418FB249C51DB6C943BF&IID=translator.5028.1",
                "headers": {
                    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36 Edg/80.0.361.66"
                },
                'data': {
                    "fromLang": "auto-detect",
                    "to": "zh-Hans",
                    "text": None
                }
            }

            dtb["data"]["text"] = text
            dtb["data"]["to"] = lang_code
            res = requests.post(**dtb).json()
            return res[0]['translations'][0]['text']
        except KeyError as er:
            print(res)
            raise er

    def test_parser(self):
        argv = ["-l", "zh-Hans", "Hello"]
        parser = optparse.OptionParser()
        parser_conf = core.read_inf(setting.CONF_PARSER)
        for option in parser_conf:
            parser.add_option(
                *(F'-{option[0]}', F'--{option}'),
                **parser_conf[option]
            )
        o, a = parser.parse_args(argv)
        oo, aa = core.parser(argv)

        # 始终保持输出一致
        self.assertEqual(o, oo, oo)
        self.assertEqual(a, aa, aa)

    def test_translator(self):
        r_text = 'Hello'
        lang_code = 'zh-Hans'

        # 使用核心内函数进行翻译请求
        t1 = core.translator(r_text, lang_code)

        # 使用同样的参数配置手动请求
        t2 = self.transelator(r_text, lang_code)

        self.assertEqual(t1, t2)

    def test_entrance(self):
        lang_code = 'zh-Hans'
        argv = ['Hello', "world", F'-l {lang_code}']

        # 测试入口
        text = entrance(argv)

        # 手动实现
        o, a = core.parser(argv)

        self.assertEqual(text, self.transelator(' '.join(a), lang_code))

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

    def test_check_options(self):
        argv = ["Hello"]
        try:
            entrance(argv)
        except AttributeError as er:
            self.fail(F"options检查没有正常工作, \n{str(er)}")

    def test_update_language_code(self):
        self.assertEqual(type(core.read_inf(setting.LANGUAGE_CODE_PATH)), dict)
        c = core.update_language_code(debug=True)
        self.assertTrue(self.check_ini_data(c))

    def test_can_save_setting(self):
        try:
            path = self.test_ini_path
            data_table1 = {'test': {'test1': 'test2'}}
            core.save_ini(path, data_table1)
            self.assertEqual(data_table1, core.read_inf('test.ini'))

            data_table2 = {'test3': {'test4': 'test5'}}
            core.save_ini(path, data_table2)
            self.assertIn('test3', core.read_inf(path))
            self.assertIn('test', core.read_inf(path))

        finally:
            os.system(F'del {path}')


class TEST_NEW_TRANSLATER(unittest.TestCase):
    def setUp(self):
        self.default_language = 'en'
        self.faker_data = Faker(locale='zh_CN')

        self.some_text: List[str, ] = [self.faker_data.color_name()
                                       for i in range(5)]

    def tearDown(self):
        pass

    def test_translator_with(self):
        language_code = 'zh-Hans'
        with core.Translator(language_code=language_code) as t:
            for text in [self.faker_data.color_name() for i in range(2)]:
                self.assertEqual(
                    core.translator(text, language_code),
                    t.teranslater(text)
                )
                time.sleep(0.5)

    def test_not_support_error(self):
        """在给出不受支持的目标语言代码时抛出错误"""
        try:
            core.Translator(language_code='ssssssss')
        except errors.TargetLanguageNotSupported:
            pass
        else:
            self.fail('没有捕获到应该出现的错误')

    def test_self_string(self):
        """Translator对象自身可直接转化为字符串"""
        text = self.faker_data.name()
        self.assertEqual(
            str(core.translator(text, self.default_language)),
            str(core.Translator(self.default_language, text))
        )

    def test_split_string(self):
        """字符串包含翻译引擎无法识别的字符时,指定分割符"""
        texts = [self.faker_data.color_name() for i in range(5)]
        self.assertEqual(
            core.translator(' '.join(texts), self.default_language),
            str(core.Translator(self.default_language, "_".join(texts), split='_')
                )
        )

    def test_custom_insert_string(self):
        """定义分隔字符"""
        text = ' '.join(self.some_text)

        text1 = '_'.join(core.translator(
            text, self.default_language).split(' '))

        text2 = str(core.Translator(
            self.default_language, text, ' ', insert='_')
        )

        self.assertEqual(text1, text2)

    def test_empty_text_error(self):
        """在没有给出文本时的错误"""
        try:
            str(core.Translator(text='', language_code=self.default_language))
        except errors.EmptyTextError:
            pass
        else:
            self.fail("没有捕获到应出现的错误")

    def test_space_characters_400Code_error(self):
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
        """配置文件读写函数在找不到文件时抛出错误"""
        try:
            path = './test.ini'
            os.system(F'del {path}')
            core.read_inf(path)
            core.save_ini(path, {})
        except errors.FileError:
            pass
        else:
            self.fail('应该出现的错误')


class FunctionlTest(unittest.TestCase):
    """TODO 新入口未编写"""
    pass


if __name__ == "__main__":
    unittest.main()
