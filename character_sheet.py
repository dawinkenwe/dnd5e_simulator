# Home Brew Imports
from damage import Damage
from dice_roller import roll_d20, roll_xdy
from equipment_manager import EquipmentManager
from health_pool import HealthPool
from skills import Skill
from stats import StatBlock
from weapon import Weapon, WeaponProperties, WeaponType

# Python Lib Imports
from typing import List
class CharacterSheet:
    def __init__(self,
                 stat_block: StatBlock,
                 skill_proficiencies: List[Skill],
                 saving_throw_proficiencies: List[str],
                 weapon_proficiencies: List[WeaponType],
                 health_pool: HealthPool,
                 proficiency_bonus: int,
                 equipment_manager: EquipmentManager,
                 feats: List[int]=None) -> CharacterSheet:
        self.stat_block = stat_block
        self.skill_proficiencies = skill_proficiencies
        self.saving_throw_proficiencies = saving_throw_proficiencies
        self.health_pool = health_pool
        self.weapon_proficiencies = weapon_proficiencies
        self.proficiency_bonus = proficiency_bonus
        self.equipment_manager = equipment_manager
        self.feats = feats

    def is_proficient_with_skill(self, skill: Skill) -> bool:
        return skill in self.skill_proficiencies

    def is_proficient_with_weapon(self, weapon: Weapon) -> bool:
        return weapon.weapon_type in self.weapon_proficiencies

    def is_proficient_with_saving_throw(self, saving_throw: str) -> bool:
        return saving_throw in self.saving_throw_proficiencies

    def calculate_armor_class(self, ac_bonus: int, include_dex: bool=True) -> int:
        # TODO: Extend to include wis override for monks.
        total_ac = 10
        max_dex_bonus = float('inf')
        if include_dex:
            if armor is not None:
                max_dex_bonus = self.equipment_manager.get_max_dex_bonus()
            dex_modifier = self.stat_block.get_modifier_for_stat("dex")
            total_ac += min(dex_modifier, max_dex_bonus)
        total_ac += ac_bonus
        total_ac += equipment_manager.get_total_ac_bonus()

        return total_ac

    # TODO: handle thrown weapons here.
    def get_stat_bonus_for_weapon_roll(self, thrown: bool=False, offhand: bool=False, attack: bool=True) -> int:
        if offhand and not attack:
            # TODO: add two weapon fighting when feats are implemented.
            return 0
        if WeaponProperties.RANGED in self.equipment_manager.main_hand_equipment.properties:
            return self.stat_block.get_modifier_for_stat("dex")
        if WeaponProperties.FINESSE in self.equipment_manager.main_hand_equipment.properties:
            dex_val = self.stat_block.get_modifier_for_stat("dex")
            str_val = self.stat_block.get_modifier_for_stat("str")
            return max(dex_val, str_val)
        return self.stat_block.get_modifier_for_stat("str")

    """
    Rolls an attack with the equipped weapon.
    Returns a tuple with the resulting number, and a boolean for if it is a critical hit.
    """
    def roll_attack_with_equipped_weapon(self, advantage: bool=False, offhand: bool=False, range: int=0) -> Tuple[int, bool]:
        is_critical = False

        disadvantage = self.equipment_manager.main_hand_equipment.has_disadvantage_at_range()
        roll = roll_d20(with_advantage=advantage, with_disadvantage=disadvantage)
        if roll == 20:
            is_critical = True
        if self.is_proficient_with_weapon():
            roll += self.proficiency_bonus
        roll += self.get_stat_bonus_for_weapon_attack(offhand=offhand)
        roll += self.equipment_manager.main_hand_equipment.get_attack_roll_bonus() if not offhand else self.equipment_manager.off_hand_equipment.get_attack_roll_bonus()
        return (roll, is_critical)

    def roll_damage_with_equipped_weapon(self, offhand: bool=False, is_critical=False) -> Damage:
        stat_bonus = self.get_stat_bonus_for_weapon_roll(offhand=offhand, attack=False)
        damage_dice = self.equipment_manager.main_hand_equipment.get_damage_dice() if not offhand else self.equipment_manager.off_hand_equipment.get_damage_dice()
        damage_type = self.equipment_manager.main_hand_equipment.get_damage_type() if not offhand else self.equipment_manager.off_hand_equipment.get_damage_type()
        damage_bonus = self.equipment_manager.main_hand_equipment.get_damage_roll_bonus() if not offhand else self.equipment_manager.off_hand_equipment.get_damage_roll_bonus()
        roll = roll_xdy(damage_dice)
        if is_critical:
            roll += roll_xdy(damage_dice)
        roll += stat_bonus
        roll += damage_bonus



