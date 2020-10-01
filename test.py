import unittest
from bin import entrance
from pyperclip import copy, paste


class Entrance(unittest.TestCase):
    """old test"""

    def setUp(self):
        self.argv = ["zh-Hans Hello world"]

    def test_can_copy_it(self):
        """测试是否能正确读写剪贴板"""
        or_text = 'hello copy program'
        # 向剪贴板写入待读取文本
        copy(or_text)
        # 从剪贴板读取,并将结果写回剪贴板
        entrance('zh-Hans -c'.split())
        # 清空剪贴板
        self.assertNotEqual(paste(), or_text)

    def test_split_string(self):
        text = ['hello', 'world']
        self.assertEqual(
            entrance(['en ', '><'.join(text), '-s', '> ', ' <']),
            ' '.join(text)
        )

if __name__ == "__main__":
    unittest.main()
