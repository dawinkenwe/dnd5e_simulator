from dice_roller import roll_d20, roll_xdy

class HealthPool:
    def __init__(self, max_hp, current_hp=0, temporary_hp=0, hit_die="1d6", num_hit_dice=1):
        self.max_hp = max_hp
        self.current_hp = current_hp
        self.temporary_hp = temporary_hp
        self.hit_die = hit_die
        self.num_hit_dice = num_hit_dice
        self.available_hit_dice = num_hit_dice
        self.death_save_successes = 0
        self.death_save_failures = 0

    """
    Adds hp to current HP up to max_hp. 
    Returns the overflow amount if any.
    """
    def add_hp(self, hp_to_add: int) -> int:
        if self.is_dead():
            return
        if not self.is_conscious:
            self.reset_death_saves()
        if hp_to_add + self.current_hp > self.max_hp:
            overflow = (self.max_hp - self.current_hp)
            self.current_hp = self.max_hp
            return overflow
        else:
            self.current_hp += hp_to_add
        return 0

    def add_temporary_hp(self, hp_to_add: int) -> None:
        if self.is_dead():
            return
        if not self.is_conscious():
            self.reset_death_saves()
        self.temporary_hp += hp_to_add


    def remove_hp(self, hp_to_remove: int) -> None:
        if not self.is_conscious():
            self.death_save_failures = self.death_save_successes + 1 if hp_to_remove < self.max_hp else 3
            return

        if self.temporary_hp > 0:
            if self.temporary_hp > hp_to_remove:
                self.temporary_hp -= hp_to_remove
                return
            else:
                hp_to_remove -= self.temporary_hp
                self.temporary_hp = 0

        self.current_hp -= hp_to_remove
        if self.current_hp < -self.max_hp:
            self.death_save_failures = 3
        if self.current_hp < 0:
            self.current_hp = 0

    # Returns True if successful, False if failure..
    def roll_death_save(self) -> None:
        roll = roll_d20()
        if roll >= 10:
            self.death_save_successes += 1
            if roll == 20:
                self.current_hp = 1
                self.reset_death_saves()
            return True
        else:
            self.death_save_failures += 1
            return False

    def reset_death_saves(self) -> None:
        self.death_save_failures = 0
        self.death_save_successes = 0

    def reset_all(self) -> None:
        self.hp = self.max_hp
        self.available_hit_dice = self.num_hit_dice
        self.reset_death_saves()

    def roll_hit_die(self) -> int:
        if self.available_hit_dice < 1:
            return 0
        self.available_hit_dice -= 1
        return roll_xdy(self.hit_die)

    def num_hit_dice_remaining(self) -> int:
        return self.available_hit_dice

    def reset_hit_dice(self):
        self.available_hit_dice = self.num_hit_dice

    def is_stabilized(self) -> bool:
        return self.death_save_successes >= 3

    def is_dead(self) -> bool:
        return self.death_save_failures >= 3

    def is_conscious(self) -> bool:
        return self.current_hp + self.temporary_hp > 0
