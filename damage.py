from enum import Enum

class DamageType(Enum):
    BLUDGEONING = "bludgeoning"
    PIERCING = "piercing"
    SLASHING = "slashing"
    ACID = "acid"
    COLD = "cold"
    FIRE = "fire"
    POINSON = "poison"
    PSYCHIC = "psychic"
    RADIANT = "radiant"
    FORCE = "force"
    LIGHTNING = "lightning"
    NECROTIC = "necrotic"
    THUNDER = "thunder"

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
    
