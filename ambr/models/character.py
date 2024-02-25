from enum import IntEnum, StrEnum
from typing import Any

from pydantic import BaseModel, Field, field_validator

from ..utils import remove_html_tags

__all__ = (
    "Element",
    "Birthday",
    "ExtraLevelType",
    "TalentExtraLevel",
    "Constellation",
    "TalentType",
    "TalentUpgradeItem",
    "TalentUpgrade",
    "Talent",
    "AscensionMaterial",
    "CharacterPromoteStat",
    "CharacterPromoteMaterial",
    "CharacterPromote",
    "CharacterBaseStat",
    "CharacterUpgrade",
    "CharacterCV",
    "CharacterInfo",
    "CharacterDetail",
    "Character",
)


class Element(StrEnum):
    ANEMO = "Wind"
    GEO = "Rock"
    ELECTRO = "Electric"
    PYRO = "Fire"
    HYDRO = "Water"
    CRYO = "Ice"
    DENDRO = "Grass"


class Birthday(BaseModel):
    month: int
    day: int


class ExtraLevelType(IntEnum):
    NORMAL = 1
    ULTIMATE = 9
    SKILL = 2


class TalentExtraLevel(BaseModel):
    talent_type: ExtraLevelType = Field(alias="talentIndex")
    extra_level: int = Field(alias="extraLevel")


class Constellation(BaseModel):
    name: str
    description: str
    extra_level: TalentExtraLevel | None = Field(alias="extraData")
    icon: str

    @field_validator("description", mode="before")
    def _format_description(cls, v: str) -> str:
        return remove_html_tags(v)

    @field_validator("extra_level", mode="before")
    def _convert_extra_level(cls, v: dict[str, dict[str, Any]] | None) -> TalentExtraLevel | None:
        return TalentExtraLevel(**v["addTalentExtraLevel"]) if v else None

    @field_validator("icon", mode="before")
    def _convert_icon_url(cls, v: str) -> str:
        return f"https://api.ambr.top/assets/UI/{v}.png"


class TalentType(IntEnum):
    NORMAL = 0
    ULTIMATE = 1
    PASSIVE = 2


class TalentUpgradeItem(BaseModel):
    id: int
    amount: int


class TalentUpgrade(BaseModel):
    level: int
    cost_items: list[TalentUpgradeItem] | None = Field(None, alias="costItems")
    mora_cost: int | None = Field(None, alias="coinCost")
    description: list[str]
    params: list[int | float]

    @field_validator("cost_items", mode="before")
    def _convert_cost_items(cls, v: dict[str, int] | None) -> list[TalentUpgradeItem] | None:
        return [TalentUpgradeItem(id=int(k), amount=v[k]) for k in v] if v else None

    @field_validator("description", mode="before")
    def _fix_descriptions(cls, v: list[str | int]) -> list[str]:
        # NOTE: This is a temporary fix for the issue with the API.
        return [remove_html_tags(str(desc)) for desc in v]


class Talent(BaseModel):
    type: TalentType
    name: str
    description: str
    icon: str
    upgrades: list[TalentUpgrade] | None = Field(None, alias="promote")
    cooldown: float | None = Field(None)
    cost: int | None = Field(None)

    @field_validator("description", mode="before")
    def _format_description(cls, v: str) -> str:
        return remove_html_tags(v)

    @field_validator("icon", mode="before")
    def _convert_icon_url(cls, v: str) -> str:
        return f"https://api.ambr.top/assets/UI/{v}.png"

    @field_validator("upgrades", mode="before")
    def _convert_upgrades(cls, v: dict[str, dict[str, Any]]) -> list[TalentUpgrade]:
        return [TalentUpgrade(**upgrade) for upgrade in v.values()]


class AscensionMaterial(BaseModel):
    id: int
    rarity: int


class CharacterPromoteStat(BaseModel):
    id: str
    value: float


class CharacterPromoteMaterial(BaseModel):
    id: int
    count: int


class CharacterPromote(BaseModel):
    promote_level: int = Field(alias="promoteLevel")
    unlock_max_level: int = Field(alias="unlockMaxLevel")
    cost_items: list[CharacterPromoteMaterial] | None = Field(None, alias="costItems")
    add_stats: list[CharacterPromoteStat] | None = Field(None, alias="addProps")
    required_player_level: int | None = Field(None, alias="requiredPlayerLevel")
    coin_cost: int | None = Field(None, alias="coinCost")

    @field_validator("cost_items", mode="before")
    def _convert_cost_items(cls, v: dict[str, int]) -> list[CharacterPromoteMaterial]:
        return [CharacterPromoteMaterial(id=int(item_id), count=v[item_id]) for item_id in v]

    @field_validator("add_stats", mode="before")
    def _convert_add_stats(cls, v: dict[str, float]) -> list[CharacterPromoteStat]:
        return [CharacterPromoteStat(id=stat_id, value=v[stat_id]) for stat_id in v]


class CharacterBaseStat(BaseModel):
    prop_type: str = Field(alias="propType")
    init_value: float = Field(alias="initValue")
    growth_type: str = Field(alias="type")


class CharacterUpgrade(BaseModel):
    base_stats: list[CharacterBaseStat] = Field(alias="prop")
    promotes: list[CharacterPromote] = Field(alias="promote")


class CharacterCV(BaseModel):
    lang: str
    va: str


class CharacterInfo(BaseModel):
    title: str
    detail: str
    constellation: str
    native: str
    cv: list[CharacterCV]

    @field_validator("cv", mode="before")
    def _convert_cv(cls, v: dict[str, str]) -> list[CharacterCV]:
        return [CharacterCV(lang=lang, va=v[lang]) for lang in v]


class CharacterDetail(BaseModel):
    id: str
    rarity: int = Field(alias="rank")
    name: str
    element: Element
    weapon_type: str = Field(alias="weaponType")
    icon: str
    birthday: Birthday
    release: int | None = Field(None)
    route: str
    info: CharacterInfo = Field(alias="fetter")
    upgrade: CharacterUpgrade
    ascension_materials: list[AscensionMaterial] = Field(alias="ascension")
    talents: list[Talent] = Field(alias="talent")
    constellations: list[Constellation] = Field(alias="constellation")
    beta: bool = Field(False)

    @field_validator("id", mode="before")
    def _stringify_id(cls, v: int) -> str:
        return str(v)

    @field_validator("icon", mode="before")
    def _convert_icon_url(cls, v: str) -> str:
        return f"https://api.ambr.top/assets/UI/{v}.png"

    @field_validator("birthday", mode="before")
    def _convert_birthday(cls, v: list[int]) -> Birthday:
        return Birthday(month=v[0], day=v[1])

    @field_validator("ascension_materials", mode="before")
    def _convert_ascension_materials(cls, v: dict[str, int]) -> list[AscensionMaterial]:
        return [AscensionMaterial(id=int(item_id), rarity=v[item_id]) for item_id in v]

    @field_validator("talents", mode="before")
    def _convert_talents(cls, v: dict[str, dict[str, Any]]) -> list[Talent]:
        return [Talent(**talent) for talent in v.values()]

    @field_validator("constellations", mode="before")
    def _convert_constellations(cls, v: dict[str, dict[str, Any]]) -> list[Constellation]:
        return [Constellation(**constellation) for constellation in v.values()]

    @property
    def gacha(self) -> str:
        """The character's gacha image."""
        return self.icon.replace("AvatarIcon", "Gacha_AvatarImg")


class Character(BaseModel):
    """
    Represents a character.

    Attributes
    ----------
    id: :class:`str`
        The character's ID.
    rarity: :class:`int`
        The character's rarity.
    name: :class:`str`
        The character's name.
    element: :class:`Element`
        The character's element.
    weapon_type: :class:`str`
        The character's weapon type.
    icon: :class:`str`
        The character's icon.
    birthday: List[:class:`str`]
        The character's birthday.
    release: :class:`int`
        The character's release date.
    route: :class:`str`
        The character's route.
    """

    id: str
    rarity: int = Field(alias="rank")
    name: str
    element: Element
    weapon_type: str = Field(alias="weaponType")
    icon: str
    birthday: Birthday
    release: int | None = Field(None)
    route: str
    beta: bool = Field(False)

    @field_validator("id", mode="before")
    def _stringify_id(cls, v: int | str) -> str:
        return str(v)

    @field_validator("icon", mode="before")
    def _convert_icon_url(cls, v: str) -> str:
        return f"https://api.ambr.top/assets/UI/{v}.png"

    @field_validator("birthday", mode="before")
    def _convert_birthday(cls, v: list[int]) -> Birthday:
        return Birthday(month=v[0], day=v[1])

    @property
    def gacha(self) -> str:
        """The character's gacha image."""
        return self.icon.replace("AvatarIcon", "Gacha_AvatarImg")
