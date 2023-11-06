from character import Character
from dice_roller import roll_d20, roll_xdy
from damage import Damage
from typing import Tuple

class Combattant:
    def __init__(self, character: Character, ac_override: int=0):
        self.character = character

    def calculate_ac(self) -> int:
        return self.ac_override if ac_override else character.calculate_ac()
        if self.ac_override:
            return self.ac_override

    def does_combattant_have_advantage(self) -> bool:
        return False

    def does_attack_hit(self, atk_roll: int) -> bool:
        return atk_roll >= self.calculate_ac()

    def take_damage(self, damage: Damage) -> None:
        self.character.take_damage(damage)

    # TODO: When adding states, add target and check for
    # Paralyzed or other conditions that would cause auto crits
    def is_critical_hit(self, roll: int):
        return roll == 20

    def make_attack_roll(self) -> Tuple[int, bool]:
        roll = roll_d20(with_advantage=self.does_combattant_have_advantage())
        weapon = self.character.weapon
        weapon_bonus = weapon.get_attack_roll_bonus()
        proficiency_bonus = character.proficiency if character.is_proficient_with_weapon() else 0
        stat_bonus = character.get_stat_bonus()
        total_roll = roll + weapon_bonus + proficiency_bonus
        return (total_roll, is_critical_hit(roll))

    def make_damage_roll(self, is_critical: bool=False) -> None:
        dmg_dice = self.character.weapon.get_damage_dice()
        damage = roll_xdy(dmg_dice)
        if is_critical:
            damage += roll_xdy(dmg_dice)
        skill_modifier = self.character.fetch_weapon_attack_modifier()
        damage += skill_modifier
        return Damage(dmg=damage, dmg_type=self.character.weapon.get_damage_type())
    
        
        
    
