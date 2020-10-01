import unittest
from .. import core, public


class ErrorsTest(unittest.TestCase):

    def test_file_notfound(self):
        """配置文件读函数在找不到文件时抛出错误"""
        try:
            path = './sr.ini'
            core.Conf.read_inf(path)
        except public.errors.FileError:
            pass
        else:
            self.fail('Not captured:FileError')

    def test_not_support_error(self):
        """在给出不受支持的目标语言代码时抛出错误"""
        try:
            core.Translator(tolang='abc')
        except public.errors.TargetLanguageNotSupported:
            pass
        else:
            self.fail('Not captured:TargetLanguageNotSupported')

    def test_empty_text_error(self):
        """在没有给出文本时的错误"""
        try:
            # 确保字符串仅包含空格时也作为空处理
            core.Translator(tolang='en').translator('  ')
        except public.errors.EmptyTextError:
            pass
        else:
            self.fail('Not captured:EmptyTextError')


if __name__ == "__main__":
    unittest.main()
