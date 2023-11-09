from armor import Armor, Shield
from weapon import Weapon
from weapon import WeaponProperties

from typing import List, Optional, Union

class CannotEquipWeapon(Exception):
    def __init__(self, slot: str, equipment_name: str):
        self.slot = slot
        self.equipment_name = equipment_name

    def __str__(self):
        return f"Could not equip {self.equipment_name} to {self.slot}. Please check that slot is empty."


# TODO: Versatile weapons. : (
class EquipmentManager:
    def __init__(self, weapons: List[Weapon] = None, armors: List[Armor] = None, main_hand_equipment: Weapon = None,
                 off_hand_equipment: Union[Weapon, Shield] = None, armor_equipped: Armor = None):
        self.main_hand_equipment = main_hand_equipment
        self.off_hand_equipment = off_hand_equipment
        self.armor_equipped = armor_equipped
        self.weapons = weapons if weapons is not None else []
        self.armors = armors if armors is not None else []

    # TODO: Handle case where equipment is not in equipment?
    def can_equip(self, equipment: Union[Armor, Weapon], equip_offhand: bool=False) -> bool:
        if type(equipment) is Weapon:
            if not equip_offhand and self.main_hand_equipment is not None:
                return False
            if ((equip_offhand and self.off_hand_equipment is not None) or
                    (self.main_hand_equipment and WeaponProperties.TWOHANDED in self.main_hand_equipment.properties)):
                return False
            if WeaponProperties.TWOHANDED in equipment.properties and (self.main_hand_equipment or self.off_hand_equipment):
                return False
        elif type(equipment) is Shield:
            if not equip_offhand or self.main_hand_equipment is not None:
                return False
        elif type(equipment) is Armor:
            return not self.armor_equipped
        return True

    def equip_equipment(self, equipment: Union[Armor, Weapon], equip_offhand: bool=False) -> None:
        equipment_type = type(equipment)
        if not self.can_equip(equipment, equip_offhand):
            slot = "armor"
            if equipment_type in [Weapon, Shield]:
                slot = "offhand" if equip_offhand else "main_hand"
            raise CannotEquipWeapon(slot=slot, equipment_name=equipment.name)
        if equipment_type in [Weapon, Shield]:
            if equip_offhand:
                self.off_hand_equipment = equipment
            else:
                self.main_hand_equipment = equipment
        elif equipment_type == Armor:
            self.armor_equipped = equipment

    def unequip_slot(self, slot: str) -> None:
        if slot == "main hand":
            self.main_hand_equipment = None
        if slot == "off hand":
            self.off_hand_equipment = None
        if slot == "armor":
            self.armor_equipped = None

    def get_total_ac_bonus(self) -> int:
        ac_bonus = 0
        if self.armor_equipped:
            ac_bonus += self.armor_equipped.get_ac_bonus()
        if self.off_hand_equipment and type(self.off_hand_equipment) is Shield:
            ac_bonus += self.off_hand_equipment.get_ac_bonus()
        return ac_bonus

    def get_max_ac_dex_bonus(self) -> int:
        return self.armor_equipped.get_max_ac_dex_bonus() if self.armor_equipped else float('inf')

    def get_equipped_weapons(self) -> List[Weapon]:
        return [self.main_hand_equipment, self.off_hand_equipment]
