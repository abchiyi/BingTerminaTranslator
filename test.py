import unittest
from bin_terminal_translater import core, setting, entrance
import requests


class Main_test(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def transelator(self, text, lang_code):
        """使用简单的方式直接实现翻译"""
        try:
            dtb = setting.data_table.copy()
            dtb["data"]["text"] = text
            dtb["data"]["to"] = lang_code
            res = requests.post(**dtb).json()
            return res[0]['translations'][0]['text']
        except KeyError as er:
            print(res)
            raise er

    def test_translator(self):
        r_text = 'Hello'
        lang_code = 'zh-Hans'

        # 使用核心内函数进行翻译请求
        t1 = core.translator(setting, r_text, lang_code)

        # 使用同样的参数配置手动请求
        t2 = self.transelator(r_text, lang_code)

        self.assertEqual(t1, t2)

    def test_entrance(self):
        lang_code = 'zh-Hans'
        argv = ['Hello', "world", F'-l {lang_code}']

        # 测试入口
        text = entrance(argv)

        # 手动实现
        parser = core.parser_generator(setting)
        o, a = parser.parse_args(argv)

        self.assertEqual(text, self.transelator(' '.join(a), lang_code))


if __name__ == "__main__":
    unittest.main()
