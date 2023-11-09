from armor import Armor, ArmorType, Shield
from damage import DamageType
from equipment_manager import EquipmentManager
from weapon import Weapon, WeaponProperties, WeaponType

import unittest


class TestEquipmentManager(unittest.TestCase):
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
        self.light_armor = Armor(name="Leather Armor", ac_bonus=1, armor_type=ArmorType.LIGHT)
        self.heavy_armor = Armor(name="Ring Mail", ac_bonus=4, armor_type=ArmorType.HEAVY)
        self.shield = Shield(name="Shield", ac_bonus=2)

        self.equipment_manager = EquipmentManager()

    def test_equip_weapon_works(self):
        self.equipment_manager.equip_equipment(self.light_armor)
        self.equipment_manager.equip_equipment(self.bow)
        self.assertEqual(self.equipment_manager.main_hand_equipment, self.bow)
        self.assertEqual(self.equipment_manager.armor_equipped, self.light_armor)


if __name__ == '__main__':
    unittest.main()
