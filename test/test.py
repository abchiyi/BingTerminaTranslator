import unittest
import re

from bing_translation_for_python import setting

from bing_translator import entrance
from pyperclip import copy, paste


class MainTest(unittest.TestCase):

    def tearDown(self) -> None:
        # 清理剪贴板
        copy('')

    def test_copy_option(self):
        """测试写剪贴板"""
        repr_text = 'hello world'

        # 复制到剪贴版
        entrance(['en', repr_text, '-c'])

        self.assertEqual(repr_text, paste())

    def test_read_from_the_clipboard(self):
        """测试读剪贴板"""
        repr_text = 'hello world'

        # 向剪贴板写入待读取文本
        copy(repr_text)

        # 从剪贴板读取文本
        entrance(['en', '-c'])

        self.assertEqual(repr_text, paste())

    def test_list_option(self):
        lang_tag = setting.Config().tgt_lang
        texts = entrance(['en', '-l'])

        for text in texts.split('\n'):
            tag = re.search("'.*'", text).group().replace("'", "")
            text = text.split(':')[0]
            self.assertEqual(lang_tag[tag]['text'], text)

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
