import unittest

from bing_translator import entrance
from pyperclip import copy, paste
from pathlib import Path
import os


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

    #  TODO 暂时不支持
    # def test_make_script(self):
    #     """测试能否正常制作脚本"""
    #     base_path = f'{os.getenv("BTT_HOME")}/scripts/'
    #     tgt_lang = 'zh-Hans'
    #     entrance([tgt_lang, "--script"])

    #     if not Path(F'{base_path}{tgt_lang}.ps1').is_file():
    #         self.fail('脚本未被创建')

    #     # 删除测试脚本
    #     for file in os.listdir(base_path):
    #         os.remove(F'{base_path}{file}')


if __name__ == "__main__":
    unittest.main()
