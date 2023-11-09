from collections import defaultdict

from armor import Armor
from character import Character
from character_sheet import CharacterSheet
from combattant import Combattant
from combat_instance import CombatInstance
from damage import DamageType
from health_pool import HealthPool
from stats import StatBlock
from weapon import Weapon, WeaponProperties, WeaponType

class Simulator:
    def __init__(self, num_simulations: int=0):
        self.num_simulations = num_simulations
        self.results = []
        self.combat_instance = None

    def create_combat_instance(self, debug_print=False):
        heroes = []
        enemies = []
        shortsword = Weapon(name="shortsword",
                            properties=[WeaponProperties.FINESSE],
                            weapon_type=WeaponType.MARTIAL,
                            damage_dice="1d6",
                            damage_type=DamageType.SLASHING)
        longsword = Weapon(name="longsword",
                           properties=[],
                           weapon_type=WeaponType.MARTIAL,
                           damage_dice="1d8",
                           damage_type=DamageType.SLASHING)
        lance = Weapon(name="vicious lance",
                       properties=[WeaponProperties.REACH],
                       weapon_type=WeaponType.MARTIAL,
                       damage_dice="1d10",
                       damage_type=DamageType.PIERCING)
        for i in range(1, 9):
            health = HealthPool(current_hp=19, max_hp=19)
            stats = StatBlock(str_val=10, dex_val=14, con_val=15, int_val=6, wis_val=8, cha_val=5)
            sheet = CharacterSheet(name="Skeeton #" + str(i),
                                   stat_block=stats,
                                   health_pool=health,
                                   proficiency_bonus=2,
                                   damage_immunities=[DamageType.POINSON],
                                   damage_vulnerabilities=[DamageType.BLUDGEONING],
                                   damage_resistances=None,
                                   weapon_proficiencies=[WeaponType.MARTIAL],
                                   weapon=shortsword,
                                   armor=None,
                                   ac_override=13,
                                   damage_roll_bonuses=[3])
            hero = Combattant(character_sheet=sheet, ac_override=13)
            heroes.append(hero)

        for i in range(1, 5):
            health = HealthPool(current_hp=22, max_hp=22)
            stats = StatBlock(str_val=15, dex_val=12, con_val=12, int_val=10, wis_val=10, cha_val=10)
            sheet = CharacterSheet(name="Dragon Army Soldier #" + str(i),
                                       stat_block=stats,
                                       health_pool=health,
                                       proficiency_bonus=2,
                                       damage_immunities=[],
                                       damage_vulnerabilities=[],
                                       damage_resistances=[],
                                       weapon_proficiencies=[WeaponType.MARTIAL],
                                       weapon=longsword,
                                       number_of_attacks=2
                                       )
            enemy = Combattant(character_sheet=sheet, ac_override=17)
            enemies.append(enemy)
        stats = StatBlock(str_val=16, dex_val=14, con_val=15, int_val=12, wis_val=14, cha_val=12)
        sheet = CharacterSheet(name="Dragon Army Officer",
                               stat_block = stats,
                               health_pool=HealthPool(max_hp=65, current_hp=65),
                               proficiency_bonus=3,
                               damage_immunities=[],
                               damage_vulnerabilities=[],
                               damage_resistances=[],
                               weapon_proficiencies=[WeaponType.MARTIAL],
                               weapon=lance,
                               number_of_attacks=2,
                               ac_override=19
                               )
        officer = Combattant(character_sheet=sheet, ac_override=19)
        enemies.append(officer)

        instance = CombatInstance(heroes=heroes, enemies=enemies, debug_print=debug_print)
        self.combat_instance = instance

    def run_simulations(self):
        for _ in range(self.num_simulations):
            self.create_combat_instance(debug_print=self.num_simulations < 2)
            result = self.combat_instance.run()
            self.results.append(result)

    def print_results(self):
        if self.num_simulations < 10:
            for result in self.results:
                print("#"*32)
                for survivor in result[1]:
                    print(survivor)
        else:
            skeetons = defaultdict(int)
            soldiers = defaultdict(int)
            for result in self.results:
                if result[0] == "Heroes":
                    skeetons[sum([1 if not hero.is_down() else 0 for hero in result[1]])] += 1
                else:
                    soldiers[sum([1 if not hero.is_down() else 0 for hero in result[1]])] += 1
            print(f"Skeetons won {sum([skeetons[key] for key in skeetons])} times")
            print(f"Soldiers won {sum([soldiers[key] for key in soldiers])} times")
            print(f"Skeeton survival counts: {dict(skeetons)}")
            print(f"Soldiers survival counts: {dict(soldiers)}")

if __name__ == "__main__":
    sim = Simulator(num_simulations=1000)
    sim.run_simulations()
    sim.print_results()
            

        
