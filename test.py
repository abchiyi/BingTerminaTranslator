import unittest
from bin_terminal_translater import core, setting
import requests


class Main_test(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_translator(self):
        r_text = 'Hello'
        lang_code = 'zh-Hans'

        # 使用核心内函数进行翻译请求
        t1 = core.translator(setting, r_text, lang_code)

        # 使用同样的参数配置手动请求
        dtb = setting.data_table.copy()
        dtb["data"]["text"] = r_text
        dtb["data"]["to"] = lang_code
        t2 = requests.post(**dtb).json()[0]['translations'][0]['text']

        self.assertEqual(t1, t2)


if __name__ == "__main__":
    unittest.main()
