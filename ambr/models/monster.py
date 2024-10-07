from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field, field_validator

from ..utils import remove_html_tags

__all__ = ("Monster", "MonsterDetail", "MonsterEntry", "MonsterReward")


class MonsterReward(BaseModel):
    id: int
    rarity: int = Field(alias="rank")
    icon: str
    count: float | None = Field(None)

    @field_validator("icon", mode="before")
    def _convert_icon_url(cls, v: str) -> str:
        return f"https://gi.yatta.moe/assets/UI/{v}.png"


class MonsterEntry(BaseModel):
    id: int
    type: str
    rewards: list[MonsterReward] = Field(alias="reward")

    @field_validator("rewards", mode="before")
    def _convert_rewards(cls, v: dict[str, dict[str, Any]] | None) -> list[MonsterReward]:
        return [MonsterReward(id=int(item_id), **v[item_id]) for item_id in v] if v else []


class MonsterDetail(BaseModel):
    id: int
    name: str
    type: str
    icon: str
    route: str
    title: str | None
    special_name: str | None = Field(alias="specialName")
    description: str
    entries: list[MonsterEntry]

    @field_validator("icon", mode="before")
    def _convert_icon_url(cls, v: str) -> str:
        return f"https://gi.yatta.moe/assets/UI{'/monster' if 'MonsterIcon' in v else ''}/{v}.png"

    @field_validator("entries", mode="before")
    def _convert_entries(cls, v: dict[str, dict[str, Any]]) -> list[MonsterEntry]:
        return [MonsterEntry(**v[item_id]) for item_id in v]

    @field_validator("description", mode="before")
    def _format_description(cls, v: str) -> str:
        return remove_html_tags(v)


class Monster(BaseModel):
    """
    Represents a living being.

    Attributes
    ----------
    id: :class:`int`
        The living being's ID.
    name: :class:`str`
        The living being's name.
    type: :class:`str`
        The living being's type.
    icon: :class:`str`
        The living being's icon.
    route: :class:`str`
        The living being's route.
    """

    id: int
    name: str
    type: str
    icon: str
    route: str

    @field_validator("icon", mode="before")
    def _convert_icon_url(cls, v: str) -> str:
        if "MonsterIcon" in v:
            return f"https://gi.yatta.moe/assets/UI/monster/{v}.png"
        else:
            return f"https://gi.yatta.moe/assets/UI/{v}.png"
