from __future__ import annotations

import datetime
from typing import Any

from loguru import logger
from pydantic import Field, field_validator

from ..enums import Element, ExtraLevelType, SpecialStat, TalentType, WeaponType
from ._base import BaseModel

__all__ = (
    "AscensionMaterial",
    "Birthday",
    "Character",
    "CharacterBaseStat",
    "CharacterCV",
    "CharacterDetail",
    "CharacterInfo",
    "CharacterPromote",
    "CharacterPromoteMaterial",
    "CharacterPromoteStat",
    "CharacterUpgrade",
    "Constellation",
    "Talent",
    "TalentExtraLevel",
    "TalentUpgrade",
    "TalentUpgradeItem",
)


class Birthday(BaseModel):
    """Represents a character's birthday.

    Attributes:
        month: The month of the birthday.
        day: The day of the birthday.
    """

    month: int
    day: int


class TalentExtraLevel(BaseModel):
    """Represents an extra talent level granted by a constellation.

    Attributes:
        talent_type: The type of talent that gets the extra level (Normal, Skill, Ultimate).
        extra_level: The number of extra levels granted.
    """

    talent_type: ExtraLevelType = Field(alias="talentIndex")
    extra_level: int = Field(alias="extraLevel")


class Constellation(BaseModel):
    """Represents a character constellation.

    Attributes:
        name: The name of the constellation.
        description: The description of the constellation's effect.
        extra_level: Information about extra talent levels granted by this constellation (optional).
        icon: The icon URL for the constellation.
    """

    name: str
    description: str
    extra_level: TalentExtraLevel | None = Field(alias="extraData")
    icon: str

    @field_validator("extra_level", mode="before")
    @classmethod
    def _convert_extra_level(cls, v: dict[str, dict[str, Any]] | None) -> TalentExtraLevel | None:
        return TalentExtraLevel(**v["addTalentExtraLevel"]) if v else None

    @field_validator("icon", mode="before")
    @classmethod
    def _convert_icon_url(cls, v: str) -> str:
        return f"https://gi.yatta.moe/assets/UI/{v}.png"


class TalentUpgradeItem(BaseModel):
    """Represents an item required for talent upgrades.

    Attributes:
        id: The ID of the required item.
        amount: The quantity of the item required.
    """

    id: int
    amount: int


class TalentUpgrade(BaseModel):
    """Represents a specific level upgrade for a talent.

    Attributes:
        level: The target level of the upgrade.
        cost_items: A list of items required for this upgrade level (optional).
        mora_cost: The Mora cost for this upgrade level (optional).
        description: A list of strings describing the talent's effect at this level.
        params: A list of numerical parameters associated with the talent's effect at this level.
    """

    level: int
    cost_items: list[TalentUpgradeItem] | None = Field(None, alias="costItems")
    mora_cost: int | None = Field(None, alias="coinCost")
    description: list[str]
    params: list[int | float]

    @field_validator("description", mode="before")
    @classmethod
    def __stringify_descriptions(cls, v: list[Any]) -> list[str]:
        return [str(i) for i in v]

    @field_validator("cost_items", mode="before")
    @classmethod
    def _convert_cost_items(cls, v: dict[str, int] | None) -> list[TalentUpgradeItem] | None:
        return [TalentUpgradeItem(id=int(k), amount=v[k]) for k in v] if v else None


class Talent(BaseModel):
    """Represents a character talent.

    Attributes:
        type: The type of talent (Normal, Skill, Ultimate, Passive).
        name: The name of the talent.
        description: The base description of the talent.
        icon: The icon URL for the talent.
        upgrades: A list of upgrade details for each level (optional, usually for active talents).
        cooldown: The cooldown time in seconds (optional).
        cost: The energy cost (optional, usually for Ultimate).
    """

    type: TalentType
    name: str
    description: str
    icon: str
    upgrades: list[TalentUpgrade] | None = Field(None, alias="promote")
    cooldown: float | None = Field(None)
    cost: int | None = Field(None)

    @field_validator("icon", mode="before")
    @classmethod
    def _convert_icon_url(cls, v: str) -> str:
        return f"https://gi.yatta.moe/assets/UI/{v}.png"

    @field_validator("upgrades", mode="before")
    @classmethod
    def _convert_upgrades(cls, v: dict[str, dict[str, Any]]) -> list[TalentUpgrade]:
        return [TalentUpgrade(**upgrade) for upgrade in v.values()]


class AscensionMaterial(BaseModel):
    """Represents a material required for character ascension.

    Attributes:
        id: The ID of the ascension material.
        rarity: The rarity rank of the material.
    """

    id: int
    rarity: int


class CharacterPromoteStat(BaseModel):
    """Represents a stat bonus gained from character promotion (ascension).

    Attributes:
        id: The identifier string for the stat (e.g., "FIGHT_PROP_HP").
        value: The value of the stat bonus.
    """

    id: str
    value: float


class CharacterPromoteMaterial(BaseModel):
    """Represents a material required for character promotion (ascension).

    Attributes:
        id: The ID of the required material.
        count: The quantity of the material required.
    """

    id: int
    count: int


class CharacterPromote(BaseModel):
    """Represents a character promotion (ascension) level.

    Attributes:
        promote_level: The ascension phase number (e.g., 1 for first ascension).
        unlock_max_level: The maximum character level unlocked after this promotion.
        cost_items: A list of materials required for this promotion (optional).
        add_stats: A list of stat bonuses granted by this promotion (optional).
        required_player_level: The minimum Adventure Rank required for this promotion (optional).
        coin_cost: The Mora cost for this promotion (optional).
    """

    promote_level: int = Field(alias="promoteLevel")
    unlock_max_level: int = Field(alias="unlockMaxLevel")
    cost_items: list[CharacterPromoteMaterial] | None = Field(None, alias="costItems")
    add_stats: list[CharacterPromoteStat] | None = Field(None, alias="addProps")
    required_player_level: int | None = Field(None, alias="requiredPlayerLevel")
    coin_cost: int | None = Field(None, alias="coinCost")

    @field_validator("cost_items", mode="before")
    @classmethod
    def _convert_cost_items(cls, v: dict[str, int]) -> list[CharacterPromoteMaterial]:
        return [CharacterPromoteMaterial(id=int(item_id), count=v[item_id]) for item_id in v]

    @field_validator("add_stats", mode="before")
    @classmethod
    def _convert_add_stats(cls, v: dict[str, float]) -> list[CharacterPromoteStat]:
        return [CharacterPromoteStat(id=stat_id, value=v[stat_id]) for stat_id in v]


class CharacterBaseStat(BaseModel):
    """Represents a base stat of a character and its growth type.

    Attributes:
        prop_type: The identifier string for the stat (e.g., "FIGHT_PROP_BASE_HP").
        init_value: The initial value of the stat at level 1.
        growth_type: The identifier string for the stat's growth curve (e.g., "GROW_CURVE_HP_S4").
    """

    prop_type: str = Field(alias="propType")
    init_value: float = Field(alias="initValue")
    growth_type: str = Field(alias="type")


class CharacterUpgrade(BaseModel):
    """Represents the upgrade details (stats and promotions) of a character.

    Attributes:
        base_stats: A list of the character's base stats and their growth types.
        promotes: A list of promotion (ascension) levels and their details.
    """

    base_stats: list[CharacterBaseStat] = Field(alias="prop")
    promotes: list[CharacterPromote] = Field(alias="promote")


class CharacterCV(BaseModel):
    """Represents character voice actor information for a specific language.

    Attributes:
        lang: The language code (e.g., "en", "jp").
        va: The name of the voice actor for this language.
    """

    lang: str
    va: str


class CharacterInfo(BaseModel):
    """Represents detailed character information like title, story, affiliation, and CVs.

    Attributes:
        title: The character's title (e.g., "Spark Knight").
        detail: The character's story or profile description.
        constellation: The name of the character's constellation.
        native: The character's affiliation or origin (e.g., "Mondstadt").
        cv: A list of voice actor information for different languages.
    """

    title: str
    detail: str
    constellation: str
    native: str
    cv: list[CharacterCV]

    @field_validator("cv", mode="before")
    @classmethod
    def _convert_cv(cls, v: dict[str, str]) -> list[CharacterCV]:
        return [CharacterCV(lang=lang, va=v[lang]) for lang in v]


class CharacterDetail(BaseModel):
    """Represents detailed information about a character.

    Attributes:
        id: The character's unique ID (as a string).
        rarity: The character's rarity rank (4 or 5).
        name: The character's name.
        element: The character's element.
        weapon_type: The type of weapon the character uses.
        icon: The icon URL for the character.
        birthday: The character's birthday.
        release: The date and time the character was released (optional).
        route: The route identifier for the character.
        info: Detailed profile information (title, story, CVs, etc.).
        upgrade: Information about the character's stats and ascension progression.
        ascension_materials: A list of materials required for ascension.
        talents: A list of the character's talents (active and passive).
        constellations: A list of the character's constellations.
        beta: Whether the character data is considered beta/unreleased.
        special_stat: The specialized stat gained through ascension (e.g., Crit Rate, Pyro DMG Bonus).
        region: The region the character is associated with.
    """

    id: str
    rarity: int = Field(alias="rank")
    name: str
    element: Element
    weapon_type: WeaponType = Field(alias="weaponType")
    icon: str
    birthday: Birthday
    release: datetime.datetime | None = Field(None)
    route: str
    info: CharacterInfo = Field(alias="fetter")
    upgrade: CharacterUpgrade
    ascension_materials: list[AscensionMaterial] = Field(alias="ascension")
    talents: list[Talent] = Field(alias="talent")
    constellations: list[Constellation] = Field(alias="constellation")
    beta: bool = Field(False)
    special_stat: SpecialStat | str = Field(alias="specialProp")
    region: str

    @field_validator("icon", mode="before")
    @classmethod
    def _convert_icon_url(cls, v: str) -> str:
        return f"https://gi.yatta.moe/assets/UI/{v}.png"

    @field_validator("birthday", mode="before")
    @classmethod
    def _convert_birthday(cls, v: list[int]) -> Birthday:
        return Birthday(month=v[0], day=v[1])

    @field_validator("ascension_materials", mode="before")
    @classmethod
    def _convert_ascension_materials(cls, v: dict[str, int]) -> list[AscensionMaterial]:
        return [AscensionMaterial(id=int(item_id), rarity=v[item_id]) for item_id in v]

    @field_validator("talents", mode="before")
    @classmethod
    def _convert_talents(cls, v: dict[str, dict[str, Any]]) -> list[Talent]:
        return [Talent(**talent) for talent in v.values()]

    @field_validator("constellations", mode="before")
    @classmethod
    def _convert_constellations(cls, v: dict[str, dict[str, Any]]) -> list[Constellation]:
        return [Constellation(**constellation) for constellation in v.values()]

    @field_validator("release", mode="before")
    @classmethod
    def _convert_release(cls, v: int | None) -> datetime.datetime | None:
        return datetime.datetime.fromtimestamp(v) if v is not None else None

    @field_validator("special_stat", mode="before")
    @classmethod
    def __convert_special_stat(cls, v: str) -> SpecialStat | str:
        try:
            return SpecialStat(v)
        except ValueError:
            logger.error(f"Unknown specialProp: {v!r}")
            return v

    @property
    def gacha(self) -> str:
        """Returns the URL for the character's gacha artwork (full body image)."""
        return self.icon.replace("AvatarIcon", "Gacha_AvatarImg")


class Character(BaseModel):
    """Represents a character summary.

    Attributes:
        id: The character's unique ID (as a string).
        rarity: The character's rarity rank (4 or 5).
        name: The character's name.
        element: The character's element.
        weapon_type: The type of weapon the character uses.
        icon: The icon URL for the character.
        birthday: The character's birthday.
        release: The date and time the character was released (optional).
        route: The route identifier for the character.
        beta: Whether the character data is considered beta/unreleased.
        special_stat: The specialized stat gained through ascension (e.g., Crit Rate, Pyro DMG Bonus).
        region: The region the character is associated with.
    """

    id: str
    rarity: int = Field(alias="rank")
    name: str
    element: Element
    weapon_type: WeaponType = Field(alias="weaponType")
    icon: str
    birthday: Birthday
    release: datetime.datetime | None = Field(None)
    route: str
    beta: bool = Field(False)
    special_stat: SpecialStat | str = Field(alias="specialProp")
    region: str

    @field_validator("icon", mode="before")
    @classmethod
    def _convert_icon_url(cls, v: str) -> str:
        return f"https://gi.yatta.moe/assets/UI/{v}.png"

    @field_validator("birthday", mode="before")
    @classmethod
    def _convert_birthday(cls, v: list[int]) -> Birthday:
        return Birthday(month=v[0], day=v[1])

    @field_validator("release", mode="before")
    @classmethod
    def _convert_release(cls, v: int | None) -> datetime.datetime | None:
        return datetime.datetime.fromtimestamp(v) if v is not None else None

    @field_validator("special_stat", mode="before")
    @classmethod
    def __convert_special_stat(cls, v: str) -> SpecialStat | str:
        try:
            return SpecialStat(v)
        except ValueError:
            logger.error(f"Unknown specialProp: {v!r}")
            return v

    @property
    def gacha(self) -> str:
        """Returns the URL for the character's gacha artwork (full body image)."""
        return self.icon.replace("AvatarIcon", "Gacha_AvatarImg")
