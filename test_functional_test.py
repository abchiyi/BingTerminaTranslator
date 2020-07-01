import unittest
from bin_terminal_translater import entrance
from pyperclip import copy, paste


class FunctionlTest(unittest.TestCase):
    """功能测试"""

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
        self.assertEqual(text, paste(), '未能复制翻译文本到剪贴板')

        # 没有指定文本时从剪贴板获取文本
        argv = ['-l', 'zh-Hans']
        print(entrance(argv))

        # 使用者忘记添加语言参数,会话给出提示
        print(entrance(["Hello"]))

        # 通过--update 来获取受支持的语言码表
        print(entrance(['--update']))

    def test_not_suport_language_code(self):
        # 语言代码验证功能，指出不支持该语言代码
        text = '不受支持的目标语言，你可以尝试更新语言代码'
        self.assertEqual(text, entrance(['-l sssssssss', 'some']))


if __name__ == "__main__":
    unittest.main()
