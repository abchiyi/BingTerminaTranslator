import unittest
from bin_terminal_translater import core, setting


class Main_test(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_translator(self):
        r_text = 'Hello'
        b_text = core.translator(setting, r_text, 'en')
        self.assertEqual(r_text, b_text)


if __name__ == "__main__":
    unittest.main()
