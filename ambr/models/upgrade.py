from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field, field_validator

__all__ = (
    "UpgradeItem",
    "Upgrade",
    "UpgradeData",
)


class UpgradeItem(BaseModel):
    id: int
    rarity: int


class Upgrade(BaseModel):
    id: str
    name: Optional[str] = Field(None)
    icon: str
    items: List[UpgradeItem]

    @field_validator("icon", mode="before")
    def _convert_icon_url(cls, v: str) -> str:
        return f"https://api.ambr.top/assets/UI/{v}.png"

    @field_validator("items", mode="before")
    def _convert_items(cls, v: Dict[str, int]) -> List[UpgradeItem]:
        return [UpgradeItem(id=int(k), rarity=v[k]) for k in v]


class UpgradeData(BaseModel):
    character: List[Upgrade] = Field(alias="avatar")
    weapon: List[Upgrade] = Field(alias="weapon")

    @field_validator("*", mode="before")
    def _convert_upgrade(cls, v: Dict[str, Dict[str, Any]]) -> List[Upgrade]:
        return [Upgrade(id=k, **v[k]) for k in v]
