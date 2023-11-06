from enum import IntEnum, StrEnum
from typing import Any, Dict, List, Optional, Union

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
    extra_level: Optional[TalentExtraLevel] = Field(alias="extraData")
    icon: str

    @field_validator("description", mode="before")
    def _format_description(cls, v: str) -> str:
        return remove_html_tags(v)

    @field_validator("extra_level", mode="before")
    def _convert_extra_level(
        cls, v: Optional[Dict[str, Dict[str, Any]]]
    ) -> Optional[TalentExtraLevel]:
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
    cost_items: Optional[List[TalentUpgradeItem]] = Field(None, alias="costItems")
    mora_cost: Optional[int] = Field(None, alias="coinCost")
    description: List[str]
    params: List[Union[int, float]]

    @field_validator("cost_items", mode="before")
    def _convert_cost_items(
        cls, v: Optional[Dict[str, int]]
    ) -> Optional[List[TalentUpgradeItem]]:
        return [TalentUpgradeItem(id=int(k), amount=v[k]) for k in v] if v else None


class Talent(BaseModel):
    type: TalentType
    name: str
    description: str
    icon: str
    upgrades: Optional[List[TalentUpgrade]] = Field(None, alias="promote")
    cooldown: Optional[int] = Field(None)
    cost: Optional[int] = Field(None)

    @field_validator("description", mode="before")
    def _format_description(cls, v: str) -> str:
        return remove_html_tags(v)

    @field_validator("icon", mode="before")
    def _convert_icon_url(cls, v: str) -> str:
        return f"https://api.ambr.top/assets/UI/{v}.png"

    @field_validator("upgrades", mode="before")
    def _convert_upgrades(cls, v: Dict[str, Dict[str, Any]]) -> List[TalentUpgrade]:
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
    cost_items: Optional[List[CharacterPromoteMaterial]] = Field(
        None, alias="costItems"
    )
    add_stats: Optional[List[CharacterPromoteStat]] = Field(None, alias="addProps")
    required_player_level: Optional[int] = Field(None, alias="requiredPlayerLevel")
    mora_cost: Optional[int] = Field(None, alias="coinCost")

    @field_validator("cost_items", mode="before")
    def _convert_cost_items(cls, v: Dict[str, int]) -> List[CharacterPromoteMaterial]:
        return [
            CharacterPromoteMaterial(id=int(item_id), count=v[item_id]) for item_id in v
        ]

    @field_validator("add_stats", mode="before")
    def _convert_add_stats(cls, v: Dict[str, float]) -> List[CharacterPromoteStat]:
        return [CharacterPromoteStat(id=stat_id, value=v[stat_id]) for stat_id in v]


class CharacterBaseStat(BaseModel):
    prop_type: str = Field(alias="propType")
    init_value: float = Field(alias="initValue")
    growth_type: str = Field(alias="type")


class CharacterUpgrade(BaseModel):
    base_stats: List[CharacterBaseStat] = Field(alias="prop")
    promotes: List[CharacterPromote] = Field(alias="promote")

    @field_validator("base_stats", mode="before")
    def _convert_base_stats(cls, v: List[Dict[str, Any]]) -> List[CharacterBaseStat]:
        return [CharacterBaseStat(**stat) for stat in v]

    @field_validator("promotes", mode="before")
    def _convert_promotes(cls, v: List[Dict[str, Any]]) -> List[CharacterPromote]:
        return [CharacterPromote(**ascension) for ascension in v]


class CharacterCV(BaseModel):
    lang: str
    va: str


class CharacterInfo(BaseModel):
    title: str
    detail: str
    constellation: str
    native: str
    cv: List[CharacterCV]

    @field_validator("cv", mode="before")
    def _convert_cv(cls, v: Dict[str, str]) -> List[CharacterCV]:
        return [CharacterCV(lang=lang, va=v[lang]) for lang in v]


class CharacterDetail(BaseModel):
    id: str
    rarity: int = Field(alias="rank")
    name: str
    element: Element
    weapon_type: str = Field(alias="weaponType")
    icon: str
    birthday: Birthday
    release: Optional[int] = Field(None)
    route: str
    info: CharacterInfo = Field(alias="fetter")
    upgrade: CharacterUpgrade
    ascension_materials: List[AscensionMaterial] = Field(alias="ascension")
    talents: List[Talent] = Field(alias="talent")
    constellations: List[Constellation] = Field(alias="constellation")
    beta: bool = Field(False)

    @field_validator("id", mode="before")
    def _stringify_id(cls, v: int) -> str:
        return str(v)

    @field_validator("icon", mode="before")
    def _convert_icon_url(cls, v: str) -> str:
        return f"https://api.ambr.top/assets/UI/{v}.png"

    @field_validator("birthday", mode="before")
    def _convert_birthday(cls, v: List[int]) -> Birthday:
        return Birthday(month=v[0], day=v[1])

    @field_validator("info", mode="before")
    def _convert_info(cls, v: Dict[str, Any]) -> CharacterInfo:
        return CharacterInfo(**v)

    @field_validator("upgrade", mode="before")
    def _convert_upgrade(cls, v: Dict[str, Any]) -> CharacterUpgrade:
        return CharacterUpgrade(**v)

    @field_validator("ascension_materials", mode="before")
    def _convert_ascension_materials(cls, v: Dict[str, int]) -> List[AscensionMaterial]:
        return [AscensionMaterial(id=int(item_id), rarity=v[item_id]) for item_id in v]

    @field_validator("talents", mode="before")
    def _convert_talents(cls, v: Dict[str, Dict[str, Any]]) -> List[Talent]:
        return [Talent(**talent) for talent in v.values()]

    @field_validator("constellations", mode="before")
    def _convert_constellations(
        cls, v: Dict[str, Dict[str, Any]]
    ) -> List[Constellation]:
        return [Constellation(**constellation) for constellation in v.values()]


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
    release: Optional[int] = Field(None)
    route: str
    beta: bool = Field(False)

    @field_validator("id", mode="before")
    def _stringify_id(cls, v: Union[int, str]) -> str:
        return str(v)

    @field_validator("icon", mode="before")
    def _convert_icon_url(cls, v: str) -> str:
        return f"https://api.ambr.top/assets/UI/{v}.png"

    @field_validator("birthday", mode="before")
    def _convert_birthday(cls, v: List[int]) -> Birthday:
        return Birthday(month=v[0], day=v[1])
