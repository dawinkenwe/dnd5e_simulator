from armor import Armor, ArmorType, Shield

from unittest import TestCase
import unittest

class TestArmor(TestCase):
    def setUp(self):
        self.light_armor = Armor(name="Leather Armor", ac_bonus=1, armor_type=ArmorType.LIGHT)
        self.medium_armor = Armor(name="Chain Shirt", ac_bonus=3, armor_type=ArmorType.MEDIUM)
        self.heavy_armor = Armor(name="Ring Mail", ac_bonus=4, armor_type=ArmorType.HEAVY)

    def test_get_ac_bonus(self):
        lbonus = self.light_armor.get_ac_bonus()
        mbonus = self.medium_armor.get_ac_bonus()
        hbonus = self.heavy_armor.get_ac_bonus()
        self.assertEqual(lbonus, 1)
        self.assertEqual(mbonus, 3)
        self.assertEqual(hbonus, 4)

    def test_get_max_dex_bonus(self):
        lbonus = self.light_armor.get_max_ac_dex_bonus()
        mbonus = self.medium_armor.get_max_ac_dex_bonus()
        hbonus = self.heavy_armor.get_max_ac_dex_bonus()
        self.assertEqual(lbonus, float('inf'))
        self.assertEqual(mbonus, 2)
        self.assertEqual(hbonus, 0)

if __name__ == '__main__':
    unittest.main()