from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field, validator


class CharacterAscensionStat(BaseModel):
    id: str
    value: float


class CharacterAscensionMaterial(BaseModel):
    id: str
    count: int


class CharacterAscension(BaseModel):
    ascension_level: int = Field(alias="promoteLevel")
    unlock_max_level: int = Field(alias="unlockMaxLevel")
    cost_items: Optional[List[CharacterAscensionMaterial]] = Field(
        None, alias="costItems"
    )
    add_stats: Optional[List[CharacterAscensionStat]] = Field(None, alias="addProps")
    required_player_level: Optional[int] = Field(None, alias="requiredPlayerLevel")
    mora_cost: Optional[int] = Field(None, alias="coinCost")

    @validator("cost_items", pre=True)
    def _add_cost_items(cls, v: Dict[str, int]) -> List[CharacterAscensionMaterial]:
        return [
            CharacterAscensionMaterial(id=item_id, count=v[item_id]) for item_id in v
        ]

    @validator("add_stats", pre=True)
    def _add_add_stats(cls, v: Dict[str, float]) -> List[CharacterAscensionStat]:
        return [CharacterAscensionStat(id=stat_id, value=v[stat_id]) for stat_id in v]


class CharacterStat(BaseModel):
    prop_type: str = Field(alias="propType")
    init_value: float = Field(alias="initValue")
    growth_type: str = Field(alias="type")


class CharacterUpgrade(BaseModel):
    stats: List[CharacterStat] = Field(alias="prop")
    ascensions: List[CharacterAscension] = Field(alias="promote")

    @validator("stats", pre=True)
    def _add_stats(cls, v: List[Dict[str, Any]]) -> List[CharacterStat]:
        return [CharacterStat(**stat) for stat in v]

    @validator("ascensions", pre=True)
    def _add_ascensions(cls, v: List[Dict[str, Any]]) -> List[CharacterAscension]:
        return [CharacterAscension(**ascension) for ascension in v]


class CharacterCV(BaseModel):
    lang: str
    va: str


class CharacterInfo(BaseModel):
    title: str
    detail: str
    constellation: str
    native: str
    cv: List[CharacterCV]

    @validator("cv", pre=True)
    def _add_cv(cls, v: Dict[str, str]) -> List[CharacterCV]:
        return [CharacterCV(lang=lang, va=v[lang]) for lang in v]


class CharacterDetail(BaseModel):
    id: int
    rarity: int = Field(alias="rank")
    name: str
    element: str
    weapon_type: str = Field(alias="weaponType")
    icon: str
    bithday: List[str]
    release: int
    route: str
    info: CharacterInfo = Field(alias="fetter")
    upgrade: CharacterUpgrade = Field(alias="upgrade")
    ascension_materials: List[str] = Field(alias="ascension")

    @validator("icon", pre=True)
    def _add_icon_url(cls, v: str) -> str:
        return f"https://api.ambr.top/assets/UI/{v}.png"

    @validator("info", pre=True)
    def _add_info(cls, v: Dict[str, Any]) -> CharacterInfo:
        return CharacterInfo(**v)

    @validator("upgrade", pre=True)
    def _add_upgrade(cls, v: Dict[str, Any]) -> CharacterUpgrade:
        return CharacterUpgrade(**v)

    @validator("ascension_materials", pre=True)
    def _add_ascension_materials(cls, v: Dict[str, str]) -> List[str]:
        return [item_id for item_id in v]


class Character(BaseModel):
    """
    Represents a character.

    Attributes
    ----------
    id: :class:`int`
        The character's ID.
    rarity: :class:`int`
        The character's rarity.
    name: :class:`str`
        The character's name.
    element: :class:`str`
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

    id: int
    rarity: int = Field(alias="rank")
    name: str
    element: str
    weapon_type: str = Field(alias="weaponType")
    icon: str
    birthday: List[str]
    release: int
    route: str

    @validator("icon", pre=True)
    def _add_icon_url(cls, v: str) -> str:
        return f"https://api.ambr.top/assets/UI/{v}.png"
