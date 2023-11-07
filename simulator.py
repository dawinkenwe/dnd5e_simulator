from character import Character
from combattant import Combattant
from combat_instance import CombatInstance
from damage import DamageType
from health_pool import HealthPool
from weapon import Weapon, WeaponProperties, WeaponType

class Simulator:
    def __init__(self, num_simulations: int):
        self.num_simulations = num_simulations
        self.results = []
        self.combat_instance = None

    def create_combat_instance(self):
        heroes = []
        enemies = []
        shortsword = Weapon(name="shortsword",
                            properties=[],
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
            character = Character(name="Skeeton #" + str(i),
                                  health_pool=health,
                                  proficiency_bonus=2,
                                  damage_immunities=[],
                                  damage_vulnerabilities=[DamageType.BLUDGEONING],
                                  damage_resistances=[],
                                  weapon_proficiencies=[WeaponType.MARTIAL],
                                  number_of_attacks=1,
                                  weapon=shortsword)
            hero = Combattant(character=character, ac_override=13)
            heroes.append(hero)

        for i in range(1, 5):
            health = HealthPool(current_hp=22, max_hp=22)
            character = Character(name="Dragon Army Soldier #" + str(i),
                                  health_pool=health,
                                  proficiency_bonus=2,
                                  damage_immunities=[],
                                  damage_vulnerabilities=[],
                                  damage_resistances=[],
                                  weapon_proficiencies=[WeaponType.MARTIAL],
                                  weapon=longsword,
                                  number_of_attacks=2
                                  )
            enemy = Combattant(character=character, ac_override=17)
            enemies.append(enemy)
        character = Character(name="Dragon Army Officer",
                              health_pool=HealthPool(max_hp=65, current_hp=65),
                              proficiency_bonus=3,
                              damage_immunities=[],
                              damage_vulnerabilities=[],
                              damage_resistances=[],
                              weapon_proficiencies=[WeaponType.MARTIAL],
                              weapon=lance,
                              number_of_attacks=2
                              )
        officer = Combattant(character=character, ac_override=19)
        enemies.append(officer)

        instance = CombatInstance(heroes=heroes, enemies=enemies)
        self.combat_instance = instance

    def run_simulations(self):
        for _ in range(self.num_simulations):
            self.create_combat_instance()
            result = self.combat_instance.run()
            self.results.append(result)

    def print_results(self):
        for result in self.results:
            print("#"*32)
            for survivor in result[1]:
                print(survivor)

if __name__ == "__main__":
    sim = Simulator(num_simulations=1)
    sim.run_simulations()
            

        
