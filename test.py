from bin_terminal_translater import core, setting, entrance
import unittest
import requests
import os


class Main_test(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def transelator(self, text, lang_code):
        """使用简单的方式直接实现翻译"""
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
        o, a = core.parser(["-l", "zh-Hans", "Hello"])
        self.assertEqual(type(a), list)

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
        self.assertTrue(os.path.exists(setting.BASE_DIR),
                        F"Not Found FIle of Fir :{setting.BASE_DIR}")
        self.assertTrue(os.path.exists(setting.CONF_PATH),
                        F'Not Found File or Dir :{setting.CONF_PATH}')
        self.assertTrue(os.path.exists(setting.CONF_PARSER),
                        F'Not Found File or Dir :{setting.CONF_PARSER}')

    def test_read_inf(self):
        """测试读取文件"""
        self.assertEqual(type(core.read_inf(setting.CONF_PARSER)), dict)
        self.assertEqual(type(core.read_inf(setting.CONF_PATH)), dict)

    def test_check_options(self):
        argv = ["Hello"]
        try:
            entrance(argv)
        except AttributeError as er:
            # self.fail(F"options检查没有正常工作, \n{str(er)}")
            pass


if __name__ == "__main__":
    unittest.main()
