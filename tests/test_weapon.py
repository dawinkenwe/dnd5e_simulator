import unittest

from damage import DamageType
from weapon import Weapon, WeaponProperties, WeaponType

class TestWeapon(unittest.TestCase):
    def setUp(self):
        self.bow = Weapon(name="Longbow",
                          weapon_type=WeaponType.MARTIAL,
                          properties=[WeaponProperties.RANGED, WeaponProperties.AMMUNITION, WeaponProperties.TWOHANDED],
                          damage_dice="1d8",
                          damage_type=DamageType.PIERCING,
                          attack_range=(150, 600))
        self.short_sword = Weapon(name="Short Sword",
                          weapon_type=WeaponType.MARTIAL,
                          properties=[WeaponProperties.FINESSE, WeaponProperties.LIGHT],
                          damage_dice="1d6",
                          damage_type=DamageType.PIERCING,
                          attack_range=(5, 5))

    def test_can_hit_enemy_at_range(self):
        can_hit_at_max = self.bow.can_hit_enemy_at_range(600)
        can_hit_below_min = self.bow.can_hit_enemy_at_range(5)
        can_hit_above_max = self.bow.can_hit_enemy_at_range(601)
        self.assertEqual(can_hit_below_min, True)
        self.assertEqual(can_hit_at_max, True)
        self.assertEqual(can_hit_above_max, False)

    def test_has_disadvantage_at_range(self):
        has_disadvantage_below_first_increment = self.bow.has_disadvantage_at_range(5)
        has_disadvantage_at_first_increment = self.bow.has_disadvantage_at_range(150)
        has_disadvantage_above_first_increment = self.bow.has_disadvantage_at_range(151)
        self.assertEqual(has_disadvantage_below_first_increment, False)
        self.assertEqual(has_disadvantage_at_first_increment, False)
        self.assertEqual(has_disadvantage_above_first_increment, True)

if __name__ == '__main__':
    unittest.main()
