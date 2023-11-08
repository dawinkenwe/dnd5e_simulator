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

    def is_dead(self) -> bool:
        return self.death_save_failures < 3

    def remove_hp(self, hp_to_remove: int) -> None:
        if self.temporary_hp > 0:
            if self.temporary_hp > hp_to_remove:
                self.temporary_hp -= hp_to_remove
                return
            else:
                hp_to_remove -= self.temporary_hp
                self.temporary_hp = 0
        self.current_hp -= hp_to_remove

    """
    Adds hp to current HP up to max_hp. 
    Returns the overflow amount if any.
    """
    def add_hp(self, hp_to_add: int) -> None:
        if self.is_dead():
            return
        if hp_to_add + self.current_hp > self.max_hp:
            overflow = (self.max_hp - self.current_hp)
            self.current_hp = self.max_hp
            return overflow
        else:
            self.current_hp += hp_to_add
        return 0

    def add_temporary_hp(self, hp_to_add: int) -> None:
        self.temporary_hp += hp_to_add

    def is_concious(self) -> bool:
        return self.current_hp + self.temporary_hp > 0

    def num_hit_dice_remaining(self) -> int:
        return self.available_hit_dice

    def reset_hit_dice(self):
        self.available_hit_dice = self.num_hit_dice

    def roll_hit_die(self) -> int:
        self.available_hit_dice -= 1
        return roll_xdy(self.hit_die)

    def reset_death_saves(self) -> None:
        self.death_save_failures = 0
        self.death_save_successes = 0

    def is_stabilized(self) -> bool:
        return self.death_save_successes >= 3

    def roll_death_save(self) -> None:
        roll = roll_d20()
        if roll == 20:
            self.reset_death_saves()
            self.current_hp = 1
        elif roll >= 10:
            self.death_save_successes += 1
        else:
            self.death_save_failures += 1