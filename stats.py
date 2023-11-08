from enum import Enum

class Stat(Enum):
    STR="str"
    DEX="dex"
    CON="con"
    INT="int"
    WIS="wis"
    CHA="cha"


class StatBlock:
    def __init__(self, str_val=10, dex_val=10, con_val=10, int_val=10, wis_val=10, cha_val=10):
        stats = {"str": str_val, "dex": dev_val, "con": con_val, "int": int_val, "wis": wis_val, "cha": cha_val}
        self.stats = stats

    def get_modifier_for_stat(self, stat_str, modifiers: int = 0):
        stat = self.stats[stat_str]
        return (stat - 10 + modifiers) // 2

    def __str__(self):
        print(self.stats)
