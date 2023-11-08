import unittest

from stats import Stat, StatBlock

class TestStatBlock(unittest.TestCase):
    def setUp(self):
        self.stat_block = StatBlock(str_val=4, dex_val=6, con_val=8, int_val=10, wis_val=13, cha_val=20)
    def test_get_modifier_for_stat(self):
        expected_values = [-3, -2,  -1, 0, 1, 5]
        stats = ["str", "dex", "con", "int", "wis", "cha"]
        for i in range(len(stats)):
            self.assertEqual(self.stat_block.get_modifier_for_stat(stats[i]), expected_values[i])

if __name__ == '__main__':
    unittest.main()