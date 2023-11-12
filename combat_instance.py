from battle_grid import BattleGrid, GridSquare
from collections import deque
from combattant import Combattant
from typing import List

class CombatInstance:
    def __init__(self,
                 heroes: List[Combattant],
                 enemies: List[Combattant],
                 grid: BattleGrid,
                 debug_print=True,
                 heroes_surprised=False,
                 enemies_surprised=False):
        self.heroes = heroes
        self.enemies = enemies
        self.num_enemies = len(enemies)
        self.num_heroes = len(heroes)
        self.turn_queue = None
        self.initiatives = []
        self.debug_print = debug_print
        self.grid = grid
        if heroes_surprised:
            for hero in self.heroes:
                hero.is_surprised = True
        if enemies_surprised:
            for enemy in self.enemies:
                enemy.is_surprised = True
        
    def dprint(self, print_str):
        if self.debug_print:
            print(print_str)

    def roll_for_initiatives(self):
        for hero in self.heroes:
            self.initiatives.append((hero, hero.roll_for_initiative()))

        for enemy in self.enemies:
            self.initiatives.append((enemy, enemy.roll_for_initiative()))

        self.initiatives.sort(key=lambda x: (x[1], x[0].init), reverse=True)
        self.turn_queue = deque([init[0] for init in self.initiatives])

    def resolve_death_saves_for_combattant(self, combattant: Combattant) -> None:
        revived = combattant.roll_death_saving_throw()
        if revived and combattant.is_conscious():
            self.dprint(f"{combattant.name} CRIT death save and is conscious again.")
            if combattant in self.heroes:
                self.num_heroes += 1
            else:
                self.num_enemies += 1

    def is_combattant_threatened(self, combattant: Combattant) -> bool:
        pass

    def combattant_attacks_target(self, combattant: Combattant, target: Combattant):
        attack_roll, damage, is_critical = self.combattant.make_attack()
        target.take_attack(attack_roll=attack_roll, damage=damage, is_critical=is_critical)

    def handle_target_goes_down(self, target: Combattant):
        if combattant.is_down():
            if combattant.is_hero:
                self.num_heroes -= 1
            else:
                self.num_enemies -= 1

    def do_movement_and_actions_for_combattant(self, combattant: Combattant):
        # IF our weapon is ranged, look for closest line of site enemy.
        pass

    def do_current_turn(self) -> None:
        combattant = self.turn_queue[0]

        if combattant.is_dead():
            return

        if not combattant.is_conscious():
            self.resolve_death_saves_for_combattant(combattant)
            return

        if combattant.is_surprised:
            combattant.is_surprised = False
            return

        combattant.do_start_of_round_checks()

        self.do_movement_and_actions_for_combattant(combattant)

        combattant.do_end_of_round_checks()

        # If combattant is in range of an enemy that is not downed, attack that enemy.
        # Otherwise, combattants move to get to that enemy.
        
        targets = self.enemies if combattant.is_hero else self.heroes
        target = combattant.pick_target(targets)

        for _ in range(combattant.character_sheet.number_of_attacks):
            target = combattant.pick_target(targets)
            if not target:
                break
            to_hit = combattant.make_attack_roll()
            is_crit = to_hit[1]
            to_hit = to_hit[0]
            self.dprint(f"{combattant.name} rolled a {to_hit} to hit")
            if target.does_attack_hit(to_hit):
                damage = combattant.make_damage_roll(is_critical=is_crit)
                self.dprint(f"{combattant.name} hit {target.name} for {damage.dmg} {damage.dmg_type} damage")
                target.take_damage(damage)
                if target.is_down():
                    self.dprint(f"{target.name} is Unconcious")
                    if target in self.enemies:
                        self.num_enemies -= 1
                    else:
                        self.num_heroes -= 1
            else:
                self.dprint(f"{combattant.name} missed {target.name}")

    def get_closest_enemy_for_combattant(self, combattant: Combattant):
        coord_to_enemy = {}
        if combattant.is_hero:
            coord_to_enemy = {enemy.get_coords: enemy for enemy in self.enemies}
        else:
            coord_to_enemy = {hero.get_coords: hero for hero in self.heroes}
        closest_

    def move_to_next_turn(self) -> None:
        self.turn_queue.rotate(-1)
        
    def is_combat_over(self) -> bool:
        return self.num_heroes == 0 or self.num_enemies == 0

    def do_end_of_round_actions(self):
        pass

    def run(self):
        self.roll_for_initiatives()
        done = False
        while not done:
            for _ in range(len(self.turn_queue)):
                self.do_current_turn()
                self.move_to_next_turn()
                if self.is_combat_over() == True:
                    done = True
                    break
                self.do_end_of_round_actions()
        self.dprint("Combat is over! Survivors below.")
        for combattant in self.turn_queue:
            if combattant.get_current_hp() > 0:
                self.dprint(combattant)
        if self.num_enemies == 0:
            return ("Heroes", self.heroes)
        else:
            return ("Enemies", self.enemies)

    
