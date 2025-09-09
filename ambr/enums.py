from __future__ import annotations

from enum import IntEnum, StrEnum

__all__ = ("City", "Element", "ExtraLevelType", "Language", "SpecialStat", "TalentType", "WeaponType")


class Language(StrEnum):
    """Supported languages for the API data."""

    CHT = "cht"
    """Traditional Chinese."""
    CHS = "chs"
    """Simplified Chinese."""
    DE = "de"
    """German."""
    EN = "en"
    """English."""
    ES = "es"
    """Spanish."""
    FR = "fr"
    """French."""
    ID = "id"
    """Indonesian."""
    JP = "jp"
    """Japanese."""
    KR = "kr"
    """Korean."""
    PT = "pt"
    """Portuguese."""
    RU = "ru"
    """Russian."""
    TH = "th"
    """Thai."""
    VI = "vi"
    """Vietnamese."""
    IT = "it"
    """Italian."""
    TR = "tr"
    """Turkish."""


class WeaponType(StrEnum):
    """Enumeration of character weapon types."""

    BOW = "WEAPON_BOW"
    CATALYST = "WEAPON_CATALYST"
    CLAYMORE = "WEAPON_CLAYMORE"
    SWORD = "WEAPON_SWORD_ONE_HAND"
    POLE = "WEAPON_POLE"


class SpecialStat(StrEnum):
    """Enumeration of character specialized ascension stats."""

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
    """Enumeration of character elements."""

    ANEMO = "Wind"
    GEO = "Rock"
    ELECTRO = "Electric"
    PYRO = "Fire"
    HYDRO = "Water"
    CRYO = "Ice"
    DENDRO = "Grass"


class TalentType(IntEnum):
    """Enumeration of character talent types."""

    NORMAL = 0
    SKILL = 1  # Often referred to as Elemental Skill
    ULTIMATE = 2  # Often referred to as Elemental Burst
    PASSIVE = 3  # Passive talents


class ExtraLevelType(IntEnum):
    """Enumeration for identifying which talent gets extra levels from constellations."""

    NORMAL = 1
    SKILL = 2
    ULTIMATE = 9


class City(IntEnum):
    """City associated with domains."""

    MONDSTADT = 1
    LIYUE = 2
    INAZUMA = 3
    SUMERU = 4
    FONTAINE = 5
    NATLAN = 6
    NOD_KRAI = 7
