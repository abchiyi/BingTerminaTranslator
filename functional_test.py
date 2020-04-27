import unittest
from bin_terminal_translater import entrance
from pyperclip import copy, paste


class FunctionlTest(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_of_main(self):
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

        # 使用者忘记添加语言参数,会话给出提示
        print(entrance(["Hello"]))

        # 通过--update 来获取受支持的语言码表
        print(entrance(['--update']))


if __name__ == "__main__":
    unittest.main()
