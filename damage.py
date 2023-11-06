from enum import Enum

class DamageType(Enum):
    BLUDGEONING = 1
    PIERCING = 2
    SLASHING = 3
    ACID = 4
    COLD = 5
    FIRE = 6
    POINSON = 7
    PSYCHIC = 8
    RADIANT = 9
    FORCE = 10
    LIGHTNING = 11
    NECROTIC = 12
    THUNDER = 13

class Damage:
    def __init__(self, dmg, dmg_type, is_magical=False):
        self.dmg = dmg
        self.dmg_type = dmg_type
        self.is_magical = is_magical

    def get_dmg(self) -> int:
        return self.dmg

    def get_type(self) -> DamageType:
        return self.dmg_type

    def is_magical(self) -> bool:
        return self.is_magical
    
