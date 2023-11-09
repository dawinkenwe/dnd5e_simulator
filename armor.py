from enum import Enum
class ArmorType(Enum):
    CLOTHING="clothing"
    LIGHT="light"
    MEDIUM="medium"
    HEAVY="heavy"


class Shield:
    def __init__(self, name: str, ac_bonus: int):
        self.name = name
        self.ac_bonus = ac_bonus

    def get_ac_bonus(self) -> int:
        return self.ac_bonus

    def __str__(self):
        return (f"Shield"
                f"Name: {self.name}"
                f"AC: {self.ac_bonus}")

class Armor:
    def __init__(self, name: str, ac_bonus: int, armor_type: ArmorType):
        self.name = name
        self.ac_bonus = ac_bonus
        self.armor_type = armor_type

    def get_ac_bonus(self) -> int:
        return self.ac_bonus

    def get_max_ac_dex_bonus(self) -> int:
        if self.armor_type == ArmorType.HEAVY:
            return 0
        elif self.armor_type == ArmorType.MEDIUM:
            return 2
        return float('inf')

    def __str__(self):
        return(f"Name: {self.name}"
               f"AC Bonus: {self.ac_bonus}"
               f"Armor Type: {self.armor_type.value}")
