

class HealthPool:
    def __init__(self, max_hp, current_hp=0, temporary_hp=0):
        self.max_hp = max_hp
        self.current_hp = current_hp
        self.temporary_hp = temporary_hp

    def remove_hp(self, hp_to_remove: int) -> None:
        if self.temporary_hp > 0:
            if self.temporary_hp > hp_to_remove:
                self.temporary_hp -= hp_to_remove
                return
            else:
                hp_to_remove -= self.temporary_hp
                self.temporary_hp = 0
        self.current_hp -= hp_to_remove

    def add_hp(self, hp_to_add: int) -> None:
        pass

    def add_temporary_hp(self, hp_to_add: int) -> None:
        self.temporary_hp += hp_to_add

    def is_concious(self) -> bool:
        return self.current_hp + self.temporary_hp > 0
