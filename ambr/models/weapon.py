from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field, field_validator

from ..utils import remove_html_tags

__all__ = (
    "WeaponAscensionMaterial",
    "WeaponPromoteCostItem",
    "WeaponPromote",
    "WeaponProp",
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


class WeaponPromote(BaseModel):
    unlock_max_level: int = Field(alias="unlockMaxLevel")
    promote_level: int = Field(alias="promoteLevel")
    cost_items: List[WeaponPromoteCostItem] = Field(list, alias="costItems")
    coin_cost: Optional[int] = Field(None, alias="coinCost")
    required_player_level: Optional[int] = Field(None, alias="requiredPlayerLevel")

    @field_validator("cost_items", mode="before")
    def _convert_cost_items(cls, v: Dict[str, int]) -> List[WeaponPromoteCostItem]:
        return [WeaponPromoteCostItem(id=int(k), amount=v[k]) for k in v]


class WeaponProp(BaseModel):
    prop_type: Optional[str] = Field(None, alias="propType")
    init_value: float = Field(alias="initValue")
    growth_type: str = Field(alias="type")


class WeaponUpgrade(BaseModel):
    awaken_cost: List[int] = Field(alias="awakenCost")
    props: List[WeaponProp] = Field(alias="prop")
    promotes: List[WeaponPromote] = Field(alias="promote")

    @field_validator("props", mode="before")
    def _convert_props(cls, v: List[Dict[str, Any]]) -> List[WeaponProp]:
        return [WeaponProp(**prop) for prop in v]

    @field_validator("promotes", mode="before")
    def _convert_promotes(cls, v: List[Dict[str, Any]]) -> List[WeaponPromote]:
        return [WeaponPromote(**promote) for promote in v]


class WeaponAffixUpgrade(BaseModel):
    level: int
    description: str

    @field_validator("description", mode="before")
    def _format_description(cls, v: str) -> str:
        return remove_html_tags(v)


class WeaponAffix(BaseModel):
    name: str
    upgrades: List[WeaponAffixUpgrade] = Field(alias="upgrade")

    @field_validator("upgrades", mode="before")
    def _convert_upgrades(cls, v: Dict[str, str]) -> List[WeaponAffixUpgrade]:
        return [WeaponAffixUpgrade(level=int(k), description=v[k]) for k in v]


class WeaponDetail(BaseModel):
    id: int
    rarity: int = Field(alias="rank")
    type: str
    name: str
    description: str
    icon: str
    story_id: Optional[int] = Field(alias="storyId")
    affix: Optional[WeaponAffix]
    route: str
    upgrade: WeaponUpgrade
    ascension_materials: List[WeaponAscensionMaterial] = Field(alias="ascension")

    @field_validator("icon", mode="before")
    def _convert_icon_url(cls, v: str) -> str:
        return f"https://api.ambr.top/assets/UI/{v}.png"

    @field_validator("affix", mode="before")
    def _convert_affix(
        cls, v: Optional[Dict[str, Dict[str, Any]]]
    ) -> Optional[WeaponAffix]:
        if v is None:
            return None
        affix = list(v.values())[0]
        return WeaponAffix(**affix)

    @field_validator("upgrade", mode="before")
    def _convert_upgrade(cls, v: Dict[str, Any]) -> WeaponUpgrade:
        return WeaponUpgrade(**v)

    @field_validator("ascension_materials", mode="before")
    def _convert_ascension_materials(
        cls, v: Dict[str, int]
    ) -> List[WeaponAscensionMaterial]:
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
