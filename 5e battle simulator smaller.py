from collections import defaultdict, deque
from random import randint
from typing import List

"""
Acceptance Criteria:
1) Can add combatants to battle
2) In intiative order, they beat on closest enemy
3) They can roll multiattack if they have it
4) Bonuses are added as expected
5) When a unit has less than 1 health, it cannot fight
6) once a side has no active units, the combat is over.
7) When complete, return stats about winning side
"""

# TODO - Stat blocks
# TODO - Vulnerabilities
# TODO - spells
# TODO - Conditions
# TODO - Spacing / maps
# TODO - Targeting
# TODO - Advantage / Disadvantage
# TODO - Critical hits
# TODO - Multiple differnt types of attacks
# TODO - Output - strings / pretty print
# TODO - sleep or timing
# TODO - surprise conditions
# TODO - Movements

DEBUG = False

def debug_print(s: str) -> None:
    if DEBUG:
        print(s)

def roll_dice(dice_str):
    dice_str = dice_str.lower()
    nums = [int(val) for val in dice_str.split('d')]
    result = [0] * nums[0]
    for i in range(nums[0]):
        result[i] = randint(1, nums[1])

    return result


class Combattant:
    def __init__(self, name, hp, ac, to_hit, dmg_dice, dmg_bonus, init, num_atks=1):
        self.name = name
        self. hp = hp
        self.ac = ac
        self.to_hit = to_hit
        self.dmg_dice = dmg_dice
        self.dmg_bonus = dmg_bonus
        self.init = init
        self.num_atks = num_atks

    def does_atk_hit(self, atk_roll) -> bool:
        return atk_roll >= self.ac

    def take_damage(self, amt) -> None:
        self.hp -= amt

    def is_down(self) -> bool:
        return self.hp <= 0

    def roll_to_hit(self) -> int:
        roll = randint(1,20)
        roll += self.to_hit
        return roll

    def roll_damage(self) -> int:
        rolls = roll_dice(self.dmg_dice)
        total_with_mod = sum(rolls) + self.dmg_bonus
        return total_with_mod

    def roll_for_initiative(self) -> int:
        roll = randint(1,20)
        total = roll + self.init
        return total

    def pick_target(self, targets):
        for target in targets:
            if target.hp > 0:
                return target
        return None

    def __str__(self):
        return f"{self.name}- HP: {self.hp}"


class Encounter:
    def __init__(self, heroes: List[Combattant], enemies: List[Combattant]):
        self.heroes = heroes
        self.enemies = enemies
        self.num_enemies = len(enemies)
        self.num_heroes = len(heroes)
        self.turn_queue = None
        self.initiatives = []

    def roll_for_initiatives(self):
        for hero in self.heroes:
            self.initiatives.append((hero, hero.roll_for_initiative()))

        for enemy in self.enemies:
            self.initiatives.append((enemy, enemy.roll_for_initiative()))

        self.initiatives.sort(key=lambda x: (x[1], x[0].init), reverse=True)
        self.turn_queue = deque([init[0] for init in self.initiatives])

    def do_current_turn(self) -> None:
        combattant = self.turn_queue[0]
        if combattant.is_down():
            return
        
        targets = self.heroes if combattant in self.enemies else self.enemies
        target = combattant.pick_target(targets)

        for _ in range(combattant.num_atks):
            target = combattant.pick_target(targets)
            if not target:
                break
            to_hit = combattant.roll_to_hit()
            debug_print(f"{combattant.name} rolled a {to_hit} to hit")
            if target.does_atk_hit(to_hit):
                damage = combattant.roll_damage()
                debug_print(f"{combattant.name} hit {target.name} for {damage} damage")
                target.take_damage(damage)
                if target.is_down():
                    debug_print(f"{target.name} is DEAD")
                    if target in self.enemies:
                        self.num_enemies -= 1
                    else:
                        self.num_heroes -= 1
            else:
                debug_print(f"{combattant.name} missed {target.name}")

    def move_to_next_turn(self) -> None:
        self.turn_queue.rotate(-1)

    def is_combat_over(self) -> bool:
        return self.num_heroes == 0 or self.num_enemies == 0

    def run(self):
        self.roll_for_initiatives()
        while not self.is_combat_over():
            self.do_current_turn()
            self.move_to_next_turn()
        debug_print("Combat is over! Survivors below.")
        for combattant in self.turn_queue:
            if combattant.hp > 0:
                debug_print(combattant)
        if self.num_enemies == 0:
            return ("Skeetons", self.num_heroes)
        else:
            return ("Dragon Army", self.num_enemies, self.enemies[-1].hp > 0)

class Simulator:
    def __init__(self, num_simulations):
        # We can find the number of wins by the sum of the number of times survived
        self.skeeton_survivors = defaultdict(int)
        self.darmy_survivors = defaultdict(int)
        self.officer_survived_count = 0
        self.num_simulations = num_simulations
        self.encounter = None

    def create_encounter(self):
        skeetons = []
        soldiers = []
        for i in range(1, 9):
            skeeton = Combattant(name="Skeeton #" + str(i), hp=19, ac=13,
                                 to_hit=4, dmg_dice="1d6", dmg_bonus=5,
                                 init=2, num_atks=1)
            skeetons.append(skeeton)

        for i in range(1, 5):
            soldier = Combattant(name="Dragon Army Soldier #" + str(i),
                                 hp=22, ac=17, to_hit=4, dmg_dice="1d8",
                                 dmg_bonus=2, init=1, num_atks=2)
            soldiers.append(soldier)

        officer = Combattant(name="Dragon Army Officer", hp=65, ac=19,
                             to_hit=5, dmg_dice="1d10", dmg_bonus=3,
                             init=2, num_atks=2)
        soldiers.append(officer)

        encounter = Encounter(heroes=skeetons, enemies=soldiers)
        self.encounter = encounter

    def run_simulations(self):
        for _ in range(self.num_simulations):
            self.create_encounter()
            result = self.encounter.run()
            if result[0] == "Skeetons":
                self.skeeton_survivors[result[1]] += 1
            else:
                self.darmy_survivors[result[1]] += 1
                if result[2]:
                    self.officer_survived_count += 1

    def print_results(self):
        print(f"Ran {self.num_simulations} simulations")
        print(f"Skeetons won {sum([self.skeeton_survivors[key] for key in self.skeeton_survivors])} times")
        print(f"Skeetons survive count {dict(self.skeeton_survivors)} times")
        print(f"Dragon Army won {sum([self.darmy_survivors[key] for key in self.darmy_survivors])} times")
        print(f"Dragon Army Officer survived {self.officer_survived_count} times")
        print(f"Dragon Army survive count {dict(self.darmy_survivors)}")

def run_full_demo():
    sim = Simulator(num_simulations=1)
    global DEBUG
    DEBUG = True
    sim.run_simulations()
    sim.print_results()

def run_1k_sims():
    sim = Simulator(num_simulations=1000)
    global DEBUG
    DEBUG = False
    sim.run_simulations()
    sim.print_results()

if __name__ == "__main__":
    run_full_demo()
    # run_1k_sims()


    
    
