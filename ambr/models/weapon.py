from __future__ import annotations

from typing import Any

from pydantic import Field, field_validator

from ._base import BaseModel

__all__ = (
    "Weapon",
    "WeaponAffix",
    "WeaponAffixUpgrade",
    "WeaponAscensionMaterial",
    "WeaponBaseStat",
    "WeaponDetail",
    "WeaponPromote",
    "WeaponPromoteCostItem",
    "WeaponPromoteStat",
    "WeaponUpgrade",
)


class WeaponAscensionMaterial(BaseModel):
    """Represents a material required for weapon ascension.

    Attributes:
        id: The ID of the ascension material.
        rarity: The rarity rank of the material.
    """

    id: int
    rarity: int


class WeaponPromoteCostItem(BaseModel):
    """Represents an item required for weapon promotion (ascension).

    Attributes:
        id: The ID of the required item.
        amount: The quantity of the item required.
    """

    id: int
    amount: int


class WeaponPromoteStat(BaseModel):
    """Represents a stat bonus gained from weapon promotion (ascension).

    Attributes:
        id: The identifier string for the stat (e.g., "FIGHT_PROP_ATTACK").
        value: The value of the stat bonus.
    """

    id: str
    value: float


class WeaponPromote(BaseModel):
    """Represents a weapon promotion (ascension) level.

    Attributes:
        unlock_max_level: The maximum weapon level unlocked after this promotion.
        promote_level: The ascension phase number (e.g., 1 for first ascension).
        cost_items: A list of materials required for this promotion (optional).
        coin_cost: The Mora cost for this promotion (optional).
        required_player_level: The minimum Adventure Rank required for this promotion (optional).
        add_stats: A list of stat bonuses granted by this promotion (optional).
    """

    unlock_max_level: int = Field(alias="unlockMaxLevel")
    promote_level: int = Field(alias="promoteLevel")
    cost_items: list[WeaponPromoteCostItem] | None = Field(None, alias="costItems")
    coin_cost: int | None = Field(None, alias="coinCost")
    required_player_level: int | None = Field(None, alias="requiredPlayerLevel")
    add_stats: list[WeaponPromoteStat] | None = Field(None, alias="addProps")

    @field_validator("cost_items", mode="before")
    @classmethod
    def _convert_cost_items(cls, v: dict[str, int]) -> list[WeaponPromoteCostItem]:
        return [WeaponPromoteCostItem(id=int(k), amount=v[k]) for k in v]

    @field_validator("add_stats", mode="before")
    @classmethod
    def _convert_add_stats(cls, v: dict[str, float]) -> list[WeaponPromoteStat]:
        return [WeaponPromoteStat(id=stat_id, value=v[stat_id]) for stat_id in v]


class WeaponBaseStat(BaseModel):
    """Represents a base stat of a weapon and its growth type.

    Attributes:
        prop_type: The identifier string for the stat (e.g., "FIGHT_PROP_BASE_ATTACK", "FIGHT_PROP_CRITICAL"). Optional.
        init_value: The initial value of the stat at level 1.
        growth_type: The identifier string for the stat's growth curve (e.g., "GROW_CURVE_ATTACK_101").
    """

    prop_type: str | None = Field(None, alias="propType")
    init_value: float = Field(alias="initValue")
    growth_type: str = Field(alias="type")


class WeaponUpgrade(BaseModel):
    """Represents the upgrade details (stats, promotions, awaken cost) of a weapon.

    Attributes:
        awaken_cost: A list of Mora costs for each refinement level (?).
        base_stats: A list of the weapon's base stats and their growth types.
        promotes: A list of promotion (ascension) levels and their details.
    """

    awaken_cost: list[int] = Field(alias="awakenCost")
    base_stats: list[WeaponBaseStat] = Field(alias="prop")
    promotes: list[WeaponPromote] = Field(alias="promote")


class WeaponAffixUpgrade(BaseModel):
    """Represents an upgrade level (refinement) for a weapon affix (passive ability).

    Attributes:
        level: The refinement level (1 to 5).
        description: The description of the affix effect at this refinement level.
    """

    level: int
    description: str


class WeaponAffix(BaseModel):
    """Represents a weapon's affix (passive ability).

    Attributes:
        name: The name of the affix.
        upgrades: A list detailing the affix effect at each refinement level.
    """

    name: str
    upgrades: list[WeaponAffixUpgrade] = Field(alias="upgrade")

    @field_validator("upgrades", mode="before")
    @classmethod
    def _convert_upgrades(cls, v: dict[str, str]) -> list[WeaponAffixUpgrade]:
        return [WeaponAffixUpgrade(level=int(k), description=v[k]) for k in v]


class WeaponDetail(BaseModel):
    """Represents detailed information about a weapon.

    Attributes:
        id: The unique ID of the weapon.
        rarity: The rarity rank of the weapon (1 to 5).
        type: The type identifier string for the weapon (e.g., "WEAPON_SWORD_ONE_HAND").
        name: The name of the weapon.
        description: The flavor text or description of the weapon.
        icon: The icon URL for the weapon.
        story_id: The ID related to the weapon's story (optional).
        affix: The weapon's passive ability (affix) details (optional).
        route: The route identifier for the weapon.
        upgrade: Information about the weapon's stats, ascension, and refinement costs.
        ascension_materials: A list of materials required for ascension.
    """

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
    @classmethod
    def _flatten_story_id(cls, v: list[int] | None) -> int | None:
        return v[0] if v else None

    @field_validator("icon", mode="before")
    @classmethod
    def _convert_icon_url(cls, v: str) -> str:
        return f"https://gi.yatta.moe/assets/UI/{v}.png"

    @field_validator("affix", mode="before")
    @classmethod
    def _convert_affix(cls, v: dict[str, dict[str, Any]] | None) -> WeaponAffix | None:
        if v is None:
            return None
        affix = next(iter(v.values()))
        return WeaponAffix(**affix)

    @field_validator("ascension_materials", mode="before")
    @classmethod
    def _convert_ascension_materials(cls, v: dict[str, int]) -> list[WeaponAscensionMaterial]:
        return [WeaponAscensionMaterial(id=int(k), rarity=v[k]) for k in v]


class Weapon(BaseModel):
    """Represents a weapon summary.

    Attributes:
        id: The unique ID of the weapon.
        rarity: The rarity rank of the weapon (1 to 5).
        type: The type identifier string for the weapon (e.g., "WEAPON_SWORD_ONE_HAND").
        name: The name of the weapon.
        icon: The icon URL for the weapon.
        route: The route identifier for the weapon.
    """

    id: int
    rarity: int = Field(alias="rank")
    type: str
    name: str
    icon: str
    route: str

    @field_validator("icon", mode="before")
    @classmethod
    def _convert_icon_url(cls, v: str) -> str:
        return f"https://gi.yatta.moe/assets/UI/{v}.png"
