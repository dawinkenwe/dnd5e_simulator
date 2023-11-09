from damage import DamageType
from enum import Enum
from typing import List, Tuple


class WeaponType(Enum):
    SIMPLE = "simple"
    MARTIAL = "martial"

class WeaponProperties(Enum):
    LIGHT = "light"
    FINESSE = "finesse"
    THROWN = "thrown"
    TWOHANDED = "two handed"
    VERSATILE = "versatile"
    REACH = "reach"
    LOADING = "loading"
    HEAVY = "heavy"
    SPECIAL = "special"
    RANGED = "ranged"
    AMMUNITION = "ammunition"

class Weapon:
    def __init__(self,
                 name: str,
                 properties: List[WeaponProperties],
                 weapon_type: WeaponType,
                 damage_dice: str,
                 damage_type: DamageType,
                 versatile_damage_dice: str = "",
                 damage_roll_bonus: int = 0,
                 attack_roll_bonus: int = 0,
                 attack_range: Tuple[int, int] = (5, 5)):
        self.name = name
        self.properties = properties
        self.weapon_type = weapon_type
        self.damage_dice = damage_dice
        self.damage_type = damage_type
        self.versatile_damage_dice = versatile_damage_dice
        self.damage_roll_bonus = damage_roll_bonus
        self.attack_roll_bonus = attack_roll_bonus
        self.attack_range = attack_range

    def get_damage_dice(self, is_two_handed: bool=False) -> str:
        if is_two_handed and WeaponProperties.VERSATILE in self.properties:
            return self.versatile_damage_dice
        return self.damage_dice

    def get_damage_type(self) -> DamageType:
        return self.damage_type

    def get_attack_roll_bonus(self) -> int:
        return self.attack_roll_bonus

    def get_damage_roll_bonus(self) -> int:
        return self.damage_roll_bonus

    # TODO: add ranged attack ranges.
    def can_hit_enemy_at_range(self, range: int):
        return not (range > self.attack_range[1])

    def has_disadvantage_at_range(self, range: int):
        return range > self.attack_range[0]

    def __str__(self):
        return (f"Name: {self.name}"
                f"Properties: {[weapon_property.value for weapon_property in self.properties]}"
                f"Weapon Type: {self.weapon_type.value}"
                f"Damage: {self.damage_dice}, {self.damage_type.value}")
