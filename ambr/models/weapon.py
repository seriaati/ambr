from typing import Any

from pydantic import BaseModel, Field, field_validator

from ..utils import remove_html_tags

__all__ = (
    "WeaponAscensionMaterial",
    "WeaponPromoteCostItem",
    "WeaponPromote",
    "WeaponBaseStat",
    "WeaponUpgrade",
    "WeaponAffixUpgrade",
    "WeaponAffix",
    "WeaponDetail",
    "Weapon",
)


class WeaponAscensionMaterial(BaseModel):
    id: int
    rarity: int


class WeaponPromoteCostItem(BaseModel):
    id: int
    amount: int


class WeaponPromoteStat(BaseModel):
    id: str
    value: float


class WeaponPromote(BaseModel):
    unlock_max_level: int = Field(alias="unlockMaxLevel")
    promote_level: int = Field(alias="promoteLevel")
    cost_items: list[WeaponPromoteCostItem] | None = Field(None, alias="costItems")
    coin_cost: int | None = Field(None, alias="coinCost")
    required_player_level: int | None = Field(None, alias="requiredPlayerLevel")
    add_stats: list[WeaponPromoteStat] | None = Field(None, alias="addProps")

    @field_validator("cost_items", mode="before")
    def _convert_cost_items(cls, v: dict[str, int]) -> list[WeaponPromoteCostItem]:
        return [WeaponPromoteCostItem(id=int(k), amount=v[k]) for k in v]

    @field_validator("add_stats", mode="before")
    def _convert_add_stats(cls, v: dict[str, float]) -> list[WeaponPromoteStat]:
        return [WeaponPromoteStat(id=stat_id, value=v[stat_id]) for stat_id in v]


class WeaponBaseStat(BaseModel):
    prop_type: str | None = Field(None, alias="propType")
    init_value: float = Field(alias="initValue")
    growth_type: str = Field(alias="type")


class WeaponUpgrade(BaseModel):
    awaken_cost: list[int] = Field(alias="awakenCost")
    base_stats: list[WeaponBaseStat] = Field(alias="prop")
    promotes: list[WeaponPromote] = Field(alias="promote")


class WeaponAffixUpgrade(BaseModel):
    level: int
    description: str

    @field_validator("description", mode="before")
    def _format_description(cls, v: str) -> str:
        return remove_html_tags(v)


class WeaponAffix(BaseModel):
    name: str
    upgrades: list[WeaponAffixUpgrade] = Field(alias="upgrade")

    @field_validator("upgrades", mode="before")
    def _convert_upgrades(cls, v: dict[str, str]) -> list[WeaponAffixUpgrade]:
        return [WeaponAffixUpgrade(level=int(k), description=v[k]) for k in v]


class WeaponDetail(BaseModel):
    id: int
    rarity: int = Field(alias="rank")
    type: str
    name: str
    description: str
    icon: str
    story_id: int | None = Field(alias="storyId")
    affix: WeaponAffix | None
    route: str
    upgrade: WeaponUpgrade
    ascension_materials: list[WeaponAscensionMaterial] = Field(alias="ascension")

    @field_validator("story_id", mode="before")
    def _flatten_story_id(cls, v: list[int] | None) -> int | None:
        return v[0] if v else None

    @field_validator("icon", mode="before")
    def _convert_icon_url(cls, v: str) -> str:
        return f"https://api.ambr.top/assets/UI/{v}.png"

    @field_validator("affix", mode="before")
    def _convert_affix(cls, v: dict[str, dict[str, Any]] | None) -> WeaponAffix | None:
        if v is None:
            return None
        affix = list(v.values())[0]
        return WeaponAffix(**affix)

    @field_validator("ascension_materials", mode="before")
    def _convert_ascension_materials(cls, v: dict[str, int]) -> list[WeaponAscensionMaterial]:
        return [WeaponAscensionMaterial(id=int(k), rarity=v[k]) for k in v]


class Weapon(BaseModel):
    """
    Represents a weapon.

    Attributes
    ----------
    id: :class:`int`
        The weapon's ID.
    rarity: :class:`int`
        The weapon's rarity.
    type: :class:`str`
        The weapon's type.
    name: :class:`str`
        The weapon's name.
    icon: :class:`str`
        The weapon's icon.
    route: :class:`str`
        The weapon's route.
    """

    id: int
    rarity: int = Field(alias="rank")
    type: str
    name: str
    icon: str
    route: str

    @field_validator("icon", mode="before")
    def _convert_icon_url(cls, v: str) -> str:
        return f"https://api.ambr.top/assets/UI/{v}.png"
