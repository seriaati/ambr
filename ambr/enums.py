from __future__ import annotations

from enum import IntEnum, StrEnum

__all__ = ("Element", "ExtraLevelType", "SpecialStat", "TalentType", "WeaponType")


class WeaponType(StrEnum):
    """Character weapon types."""

    BOW = "WEAPON_BOW"
    CATALYST = "WEAPON_CATALYST"
    CLAYMORE = "WEAPON_CLAYMORE"
    SWORD = "WEAPON_SWORD_ONE_HAND"
    POLE = "WEAPON_POLE"


class SpecialStat(StrEnum):
    """Character specialized stat."""

    CRIT_RATE = "FIGHT_PROP_CRITICAL"
    CRITI_DMG = "FIGHT_PROP_CRITICAL_HURT"

    BASE_ATTACK = "FIGHT_PROP_BASE_ATTACK"
    ATTACK = "FIGHT_PROP_ATTACK_PERCENT"
    HP = "FIGHT_PROP_HP_PERCENT"
    DEFENSE = "FIGHT_PROP_DEFENSE_PERCENT"

    HEAL_BONUS = "FIGHT_PROP_HEAL_ADD"
    ELEMENTAL_MASTERY = "FIGHT_PROP_ELEMENT_MASTERY"
    ENERGY_RECHARGE = "FIGHT_PROP_CHARGE_EFFICIENCY"

    HYDRO_DMG_BONUS = "FIGHT_PROP_WATER_ADD_HURT"
    PYRO_DMG_BONUS = "FIGHT_PROP_FIRE_ADD_HURT"
    ELECTRO_DMG_BONUS = "FIGHT_PROP_ELEC_ADD_HURT"
    ANEMO_DMG_BONUS = "FIGHT_PROP_WIND_ADD_HURT"
    CRYO_DMG_BONUS = "FIGHT_PROP_ICE_ADD_HURT"
    GEO_DMG_BONUS = "FIGHT_PROP_ROCK_ADD_HURT"
    DENDRO_DMG_BONUS = "FIGHT_PROP_GRASS_ADD_HURT"
    PHYSICAL_DMG_BONUS = "FIGHT_PROP_PHYSICAL_ADD_HURT"


class Element(StrEnum):
    ANEMO = "Wind"
    GEO = "Rock"
    ELECTRO = "Electric"
    PYRO = "Fire"
    HYDRO = "Water"
    CRYO = "Ice"
    DENDRO = "Grass"


class TalentType(IntEnum):
    NORMAL = 0
    ULTIMATE = 1
    PASSIVE = 2


class ExtraLevelType(IntEnum):
    NORMAL = 1
    ULTIMATE = 9
    SKILL = 2
