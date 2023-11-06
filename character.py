from damage import Damage, DamageType
from dice_roller import roll_d20, roll_xdy
from health_pool import HealthPool
from weapon import Weapon

class Character:
    def __init__(self, name: str,
                 health_pool: HealthPool,
                 proficiency_bonus: int,
                 damage_vulnerabilities: List[DamageType],
                 damage_immunities: List[DamageType],
                 damage_resistances: List[DamageType],
                 weapon_proficiencies: List[str],
                 weapon = Weapon,
                 number_of_attacks: int=1
                 ):
        self.name = name
        self.health_pool = health_pool
        self.proficiency_bonus = proficiency_bonus
        self.damage_vulnerabilities = damage_vulnerabilities
        self.damage_immunities = damage_immunities
        self.damage_resistances = damage_resistances
        self.weapon_proficiencies = weapon_proficiencies
        self.number_of_attacks = number_of_attacks

    def adjust_incoming_damage(self, damage: Damage) -> int:
        dmg_type = dmg.get_type()
        dmg = dmg.get_dmg()
        if dmg_type in self.damage_resistances:
            return dmg // 2
        if dmg_type in self.damage_immunities:
            return 0
        if dmg_type in self.damage_vulnerabilities:
            return dmg * 2
        return dmg

    def take_damage(self, damage: Damage) -> None:
        adjusted_damage = self.adjust_incoming_damage(damage)
        self.health_pool.remove_hp(adjusted_damage)

    def fetch_weapon_attack_modifier(self) -> None:
        return 2

    def calculate_ac(self):
        return 10

    def is_proficient_with_weapon(self) -> bool:
        return self.weapon.weapon_type in self.weapon_proficiencies
        
