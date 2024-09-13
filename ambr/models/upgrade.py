from typing import Any

from pydantic import BaseModel, Field, field_validator

__all__ = (
    "Upgrade",
    "UpgradeData",
    "UpgradeItem",
)


class UpgradeItem(BaseModel):
    id: int
    rarity: int


class Upgrade(BaseModel):
    id: str
    name: str | None = Field(None)
    icon: str
    items: list[UpgradeItem]

    @field_validator("icon", mode="before")
    def _convert_icon_url(cls, v: str) -> str:
        return f"https://gi.yatta.top/assets/UI/{v}.png"

    @field_validator("items", mode="before")
    def _convert_items(cls, v: dict[str, int]) -> list[UpgradeItem]:
        return [UpgradeItem(id=int(k), rarity=v[k]) for k in v]


class UpgradeData(BaseModel):
    character: list[Upgrade] = Field(alias="avatar")
    weapon: list[Upgrade] = Field(alias="weapon")

    @field_validator("*", mode="before")
    def _convert_upgrade(cls, v: dict[str, dict[str, Any]]) -> list[Upgrade]:
        return [Upgrade(id=k, **v[k]) for k in v]
