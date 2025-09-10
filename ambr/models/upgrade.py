from __future__ import annotations

from typing import Any

from pydantic import Field, field_validator

from ._base import BaseModel

__all__ = ("Upgrade", "UpgradeData", "UpgradeItem")


class UpgradeItem(BaseModel):
    """Represents an item required for an upgrade.

    Attributes:
        id: The item's ID.
        rarity: The item's rarity.
    """

    id: int
    rarity: int


class Upgrade(BaseModel):
    """Represents upgrade information for a character or weapon type.

    Attributes:
        id: The ID of the character or weapon.
        name: The name of the character or weapon (optional).
        icon: The icon URL of the character or weapon.
        items: A list of items required for the upgrade.
    """

    id: str
    name: str | None = Field(None)
    icon: str
    items: list[UpgradeItem]

    @field_validator("icon", mode="before")
    @classmethod
    def _convert_icon_url(cls, v: str) -> str:
        return f"https://gi.yatta.moe/assets/UI/{v}.png"

    @field_validator("items", mode="before")
    @classmethod
    def _convert_items(cls, v: dict[str, int]) -> list[UpgradeItem]:
        return [UpgradeItem(id=int(k), rarity=v[k]) for k in v]


class UpgradeData(BaseModel):
    """Container for character and weapon upgrade data.

    Attributes:
        character: A list of character upgrade information.
        weapon: A list of weapon upgrade information.
    """

    character: list[Upgrade] = Field(alias="avatar")
    weapon: list[Upgrade] = Field(alias="weapon")

    @field_validator("*", mode="before")
    @classmethod
    def _convert_upgrade(cls, v: dict[str, dict[str, Any]]) -> list[Upgrade]:
        return [Upgrade(id=k, **v[k]) for k in v]
