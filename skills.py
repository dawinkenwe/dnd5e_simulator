from enum import Enum

class Skill(Enum):
    ACROBATICS="acrobatics"
    ANIMALHANDLING="animal handling"
    ARCANA="arcana"
    ATHLETICS="athletics"
    DECEPTION="deception"
    HISTORY="history"
    INSIGHT="insight"
    INTIMIDATION="intimidation"
    INVESTIGATION="investigation"
    MEDICINE="medicine"
    NATURE="nature"
    PERCEPTION="perception"
    PERFORMANCE="performance"
    PERSUASION="persuasion"
    RELIGION="religion"
    SLEIGHTOFHAND="sleight of hand"
    STEALTH="stealth"
    SURVIVAL="survival"

def get_stat_for_skill(skill: Skill) -> str:
    str_skills = [Skill.ATHLETICS]
    dex_skills = [Skill.ACROBATICS, Skill.SLEIGHTOFHAND, Skill.STEALTH]
    int_skills = [Skill.ARCANA, Skill.HISTORY, Skill.INVESTIGATION, Skill.NATURE, Skill.RELIGION]
    wis_skills = [Skill.ANIMALHANDLING, Skill.INSIGHT, Skill.MEDICINE, Skill.PERCEPTION, Skill.SURVIVAL]
    charisma_skills = [Skill.DECEPTION, Skill.INTIMIDATION, Skill.PERFORMANCE, Skill.PERSUASION]

    if skill in str_skills:
        return "str"
    if skill in dex_skills:
        return "dex"
    if skill in int_skills:
        return "int"
    if skill in wis_skills:
        return "wis"
    if skill in charisma_skills:
        return "cha"