from character_sheet import CharacterSheet
from dice_roller import roll_d20, roll_xdy
from damage import Damage
from typing import List, Tuple

# TODO: Organize methods based off of combat stuff
# Charater sheet retrieval stuff, etc...

class Combattant:
    def __init__(self,
                 character_sheet: CharacterSheet,
                 ac_override: int=0,
                 is_surprised: bool=False,
                 coordinates: Tuple[int, int] = (0,0)):
        self.character_sheet = character_sheet
        self.init = 0
        self.name = character_sheet.name
        self.ac_override = ac_override
        self.is_surprised = is_surprised
        self.movement_remaining = self.character_sheet.movement_speed
        self.coordinates = coordinates

    def calculate_ac(self) -> int:
        return self.ac_override if self.ac_override else self.character_sheet.calculate_ac()
        if self.ac_override:
            return self.ac_override

    def has_advantage(self) -> bool:
        return False

    def has_disadvantage(self, range:int = 5) -> bool:
        return self.character_sheet.weapon.has_disadvantage_at_range(range)

    def does_attack_hit(self, atk_roll: int) -> bool:
        return atk_roll >= self.calculate_ac()

    def take_damage(self, damage: Damage) -> None:
        self.character_sheet.take_damage(damage)

    def is_down(self) -> bool:
        return not self.character_sheet.health_pool.is_conscious()

    def is_dead(self) -> bool:
        return self.character_sheet.health_pool.is_dead()

    def is_conscious(self) -> bool:
        return self.character_sheet.health_pool.is_conscious()

    def roll_death_saving_throw(self):
        return self.character_sheet.health_pool.roll_death_save()

    def get_current_hp(self) -> int:
        return self.character_sheet.health_pool.current_hp

    def roll_for_initiative(self) -> int:
        d20 = roll_d20()
        dex_bonus = self.character_sheet.stat_block.get_modifier_for_stat("dex")
        self.init = d20
        return d20
        # TODO: Retrieve init bonus from character.

    # Paralyzed or other conditions that would cause auto crits
    def is_critical_hit(self, roll: int):
        return roll == 20

    def make_attack_roll(self) -> Tuple[int, bool]:
        return self.character_sheet.make_attack_roll()

    def make_damage_roll(self, is_critical: bool=False) -> Damage:
        return self.character_sheet.make_damage_roll(is_critical=is_critical)

    def pick_target(self, targets):
        for target in targets:
            if not target.is_down():
                return target
        return None

    def __str__(self):
        out = f"""Name: {self.name}
HP: {self.get_current_hp()}"""
        return out
                
    
        
        
    
