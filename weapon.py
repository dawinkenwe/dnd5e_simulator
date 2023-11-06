from damage import DamageType
from enum import Enum


class WeaponType(Enum):
    SIMPLE = 1
    MARTIAL = 2

class WeaponProperties(Enum):
    LIGHT = 1
    FINESSE = 2
    THROWN = 3
    TWOHANDED = 4
    VERSATILE = 5
    REACH = 6
    LOADING = 7
    TWOHANDED = 8
    HEAVY = 9
    SPECIAL = 10

class Weapon:
    def __init__(self, properties: List[WeaponProperties],
                 weapon_type: WeaponTypes,
                 damage_dice: str,
                 damage_type: DamageType,
                 versitile_damage_dice: str,
                 damage_roll_bonus: int = 0,
                 attack_roll_bonus: int = 0):
        self.properties = properties
        self.weapon_types = weapon_types
        self.damage_dice = damage_dice
        self.damage_type = damage_type
        self.versatile_damage_dice = versatile_damage_dice
        self.damage_roll_bonus = damage_roll_bonus
        self.attack_roll_bonus = attack_roll_bonus

    def get_damage_dice(self, is_two_handed: bool) -> str:
        if is_two_handed and VERSATILE in self.weapon_types:
            return self.versatile_damage_dice
        return self.damage_dice

    def get_damage_type(self) -> DamageType:
        return self.damage_type

    def get_attack_roll_bonus(self) -> int:
        return self.attack_roll_bonus

    def get_damage_roll_bonus(self) -> int:
        return self.damage_roll_bonus
