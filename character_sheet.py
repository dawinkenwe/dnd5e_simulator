# Home Brew Imports
from armor import Armor
from damage import Damage, DamageType
from dice_roller import roll_d20, roll_xdy
from equipment_manager import EquipmentManager
from health_pool import HealthPool
from skills import Skill
from stats import StatBlock
from weapon import Weapon, WeaponProperties, WeaponType

# Python Lib Imports
from typing import List, Tuple
class CharacterSheet:
    def __init__(self,
                 name: str,
                 stat_block: StatBlock,
                 health_pool: HealthPool,
                 proficiency_bonus: int,
                 weapon: Weapon = None,
                 armor: Armor = None,
                 feats: List[int]=None,
                 number_of_attacks: int = 1,
                 ac_override: int = 0,
                 base_movement_speed: int = 30,
                 weapon_proficiencies: List[WeaponType] = [WeaponType.SIMPLE],
                 saving_throw_proficiencies: List[str] = None,
                 skill_proficiencies: List[Skill] = None,
                 damage_vulnerabilities: List[DamageType] = None,
                 damage_immunities: List[DamageType] = None,
                 damage_resistances: List[DamageType] = None,
                 damage_roll_bonuses: List[int] = None
                 ):
        self.stat_block = stat_block
        self.skill_proficiencies = skill_proficiencies if skill_proficiencies is not None else []
        self.saving_throw_proficiencies = saving_throw_proficiencies if saving_throw_proficiencies is not None else []
        self.health_pool = health_pool
        self.weapon_proficiencies = weapon_proficiencies
        self.proficiency_bonus = proficiency_bonus
        self.feats = feats
        self.number_of_attacks = number_of_attacks
        self.ac_override = ac_override
        self.weapon = weapon
        self.armor = armor
        self.base_movement_speed = 30
        self.damage_vulnerabilities = [] if damage_vulnerabilities is None else damage_vulnerabilities
        self.damage_resistances = [] if damage_resistances is None else damage_resistances
        self.damage_immunities = [] if damage_immunities is None else damage_immunities
        self.name = name
        self.damage_roll_bonuses = [] if damage_roll_bonuses is None else damage_roll_bonuses

    def is_proficient_with_skill(self, skill: Skill) -> bool:
        return skill in self.skill_proficiencies

    def is_proficient_with_weapon(self, weapon: Weapon) -> bool:
        return weapon.weapon_type in self.weapon_proficiencies

    def is_proficient_with_saving_throw(self, saving_throw: str) -> bool:
        return saving_throw in self.saving_throw_proficiencies

    def get_number_of_attacks(self):
        return self.number_of_attacks

    def calculate_armor_class(self, ac_bonus: int, include_dex: bool=True) -> int:
        if self.ac_override:
            return self.ac_override
        total_ac = 10
        max_dex_bonus = float('inf')
        if include_dex:
            if armor is not None:
                max_dex_bonus = self.armor.get_max_dex_bonus()
            dex_modifier = self.stat_block.get_modifier_for_stat("dex")
            total_ac += min(dex_modifier, max_dex_bonus)
        total_ac += ac_bonus
        total_ac += armor.get_total_ac_bonus()

        return total_ac

    def get_stat_bonus_for_weapon(self, thrown: bool=False, offhand: bool=False) -> int:
        if WeaponProperties.RANGED in self.weapon.properties:
            return self.stat_block.get_modifier_for_stat("dex")
        if WeaponProperties.FINESSE in self.weapon.properties:
            dex_val = self.stat_block.get_modifier_for_stat("dex")
            str_val = self.stat_block.get_modifier_for_stat("str")
            return max(dex_val, str_val)
        return self.stat_block.get_modifier_for_stat("str")

    """
    Rolls an attack with the passed in weapon.
    Returns a tuple with the resulting number, and a boolean for if it is a critical hit.
    """
    def make_attack_roll(self, advantage: bool=False, offhand: bool=False, range: int=5) -> Tuple[int, bool]:
        is_critical = False

        disadvantage = self.weapon.has_disadvantage_at_range(range=range)
        roll = roll_d20(with_advantage=advantage, with_disadvantage=disadvantage)
        if roll == 20:
            is_critical = True
        if self.is_proficient_with_weapon(self.weapon):
            roll += self.proficiency_bonus
        roll += self.get_stat_bonus_for_weapon(offhand=offhand)
        roll += self.weapon.get_attack_roll_bonus()
        return (roll, is_critical)

    def get_damage_roll_bonuses(self) -> int:
        return sum(self.damage_roll_bonuses) + self.weapon.get_damage_roll_bonus()

    def make_damage_roll(self, offhand: bool=False, is_critical=False) -> Damage:
        stat_bonus = self.get_stat_bonus_for_weapon(offhand=offhand)
        damage_dice = self.weapon.get_damage_dice()
        damage_bonus = self.get_damage_roll_bonuses()
        roll = roll_xdy(damage_dice)
        if is_critical:
            roll += roll_xdy(damage_dice)
        roll += stat_bonus
        roll += damage_bonus
        return Damage(dmg=roll, dmg_type = self.weapon.damage_type)

    def take_damage(self, damage: Damage):
        dtype = damage.get_type()
        if dtype in self.damage_immunities:
            damage.dmg = 0
        elif dtype in self.damage_resistances:
            damage.dmg = damage.dmg // 2
        elif dtype in self.damage_vulnerabilities:
            damage.dmg = damage.dmg * 2
        self.health_pool.remove_hp(damage.dmg)

    def roll_skill_check(self, skill: Skill, ) -> int:
        pass
