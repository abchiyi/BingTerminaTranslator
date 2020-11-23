import unittest

from bing_translator import entrance
from pyperclip import copy, paste


class MainTest(unittest.TestCase):

    def tearDown(self) -> None:
        # 清理剪贴板
        copy('')

    def test_copy_option(self):
        """测试是否能正确读写剪贴板"""

        repr_text = 'hello world'
        # 向剪贴板写入待读取文本
        copy(repr_text)
        # 参数中不给出文本参数，以便从剪贴板读取
        text = entrance(['zh-Hans','-c','-d'])

        self.assertNotEqual(text, paste())

    def test_list_option(self):
        entrance(['zh-Hans', '-l'])


    def test_error_language_tag(self):
        entrance(['abc','hello'])


















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
