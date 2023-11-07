from collections import deque
from combattant import Combattant
from typing import List

class CombatInstance:
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

        # Saving Throws would go here
        if combattant.is_down():
            return

        is_hero = combattant in self.heroes
        
        targets = self.enemies if is_hero else self.heroes
        target = combattant.pick_target(targets)

        for _ in range(combattant.character.number_of_attacks):
            target = combattant.pick_target(targets)
            if not target:
                break
            to_hit = combattant.make_attack_roll()
            is_crit = to_hit[1]
            to_hit = to_hit[0]
            print(f"{combattant.name} rolled a {to_hit} to hit")
            if target.does_attack_hit(to_hit):
                damage = combattant.make_damage_roll(is_critical=is_crit)
                print(f"{combattant.name} hit {target.name} for {damage.dmg} {damage.dmg_type} damage")
                target.take_damage(damage)
                if target.is_down():
                    print(f"{target.name} is DEAD")
                    if target in self.enemies:
                        self.num_enemies -= 1
                    else:
                        self.num_heroes -= 1
            else:
                print(f"{combattant.name} missed {target.name}")

    def move_to_next_turn(self) -> None:
        self.turn_queue.rotate(-1)
        
    def is_combat_over(self) -> bool:
        return self.num_heroes == 0 or self.num_enemies == 0

    def run(self):
        self.roll_for_initiatives()
        while not self.is_combat_over():
            self.do_current_turn()
            self.move_to_next_turn()
        print("Combat is over! Survivors below.")
        for combattant in self.turn_queue:
            if combattant.get_current_hp() > 0:
                print(combattant)
        if self.num_enemies == 0:
            return ("Heroes", self.heroes)
        else:
            return ("Enemies", self.enemies)

    
