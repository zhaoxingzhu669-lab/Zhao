"""text_cleaner 的简单测试。运行：python3 -m unittest test_text_cleaner -v"""

import unittest

from text_cleaner import clean_text


class TestCleanText(unittest.TestCase):
    def test_removes_blank_lines(self):
        cleaned, stats = clean_text("你好\n\n\n世界\n")
        self.assertEqual(cleaned, "你好\n世界\n")
        self.assertEqual(stats["删除空行"], 2)

    def test_removes_duplicate_lines(self):
        cleaned, stats = clean_text("苹果\n香蕉\n苹果\n")
        self.assertEqual(cleaned, "苹果\n香蕉\n")
        self.assertEqual(stats["删除重复行"], 1)

    def test_trims_and_merges_spaces(self):
        cleaned, _ = clean_text("  你好   世界  \n")
        self.assertEqual(cleaned, "你好 世界\n")

    def test_fullwidth_space(self):
        cleaned, _ = clean_text("你好　世界\n")
        self.assertEqual(cleaned, "你好 世界\n")

    def test_keep_blank(self):
        cleaned, _ = clean_text("甲\n\n乙\n", keep_blank=True)
        self.assertEqual(cleaned, "甲\n\n乙\n")

    def test_keep_dupe(self):
        cleaned, _ = clean_text("甲\n甲\n", keep_dupe=True)
        self.assertEqual(cleaned, "甲\n甲\n")


if __name__ == "__main__":
    unittest.main()
