import unittest
from bin_terminal_translater import entrance
from pyperclip import copy, paste


class FunctionlTest(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_of_main(self):
        # help
        entrance(['-h'])
        # 翻译你好到英文
        argv = ['-l', 'en', '你好']
        print(entrance(argv))

        # 指定 “-c” 标志符来复制到剪贴板
        argv.append('-c')
        copy('')  # 确保剪贴板是空的
        text = entrance(argv)
        self.assertEqual(text, paste())

        # 没有指定文本时从剪贴板获取文本
        argv = ['-l', 'zh-Hans']
        print(entrance(argv))

        #


if __name__ == "__main__":
    unittest.main()
