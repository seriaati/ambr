from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field, field_validator

from ..utils import remove_html_tags

__all__ = ("Monster", "MonsterDetail", "MonsterEntry", "MonsterReward")


class MonsterReward(BaseModel):
    """Represents a potential reward dropped by a monster.

    Attributes:
        id: The ID of the reward item.
        rarity: The rarity rank of the reward item.
        icon: The icon URL of the reward item.
        count: The typical amount dropped (optional).
    """

    id: int
    rarity: int = Field(alias="rank")
    icon: str
    count: float | None = Field(None)

    @field_validator("icon", mode="before")
    @classmethod
    def _convert_icon_url(cls, v: str) -> str:
        return f"https://gi.yatta.moe/assets/UI/{v}.png"


class MonsterEntry(BaseModel):
    """Represents an entry or variant of a monster.

    Attributes:
        id: The ID of this specific monster entry/variant.
        type: The type or category of this entry.
        rewards: A list of potential rewards for this entry.
    """

    id: int
    type: str
    rewards: list[MonsterReward] = Field(alias="reward")

    @field_validator("rewards", mode="before")
    @classmethod
    def _convert_rewards(cls, v: dict[str, dict[str, Any]] | None) -> list[MonsterReward]:
        return [MonsterReward(id=int(item_id), **v[item_id]) for item_id in v] if v else []


class MonsterDetail(BaseModel):
    """Represents detailed information about a monster or living being.

    Attributes:
        id: The unique ID of the monster.
        name: The name of the monster.
        type: The type or category of the monster.
        icon: The icon URL for the monster.
        route: The route identifier for the monster.
        title: An optional title associated with the monster.
        special_name: An optional special name for the monster.
        description: The description of the monster.
        entries: A list of different entries or variants of this monster.
    """

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
    @classmethod
    def _convert_icon_url(cls, v: str) -> str:
        return f"https://gi.yatta.moe/assets/UI{'/monster' if 'MonsterIcon' in v else ''}/{v}.png"

    @field_validator("entries", mode="before")
    @classmethod
    def _convert_entries(cls, v: dict[str, dict[str, Any]]) -> list[MonsterEntry]:
        return [MonsterEntry(**v[item_id]) for item_id in v]

    @field_validator("description", mode="before")
    @classmethod
    def _format_description(cls, v: str) -> str:
        return remove_html_tags(v)


class Monster(BaseModel):
    """Represents a monster or living being summary.

    Attributes:
        id: The unique ID of the monster/being.
        name: The name of the monster/being.
        type: The type or category of the monster/being.
        icon: The icon URL for the monster/being.
        route: The route identifier for the monster/being.
    """

    id: int
    name: str
    type: str
    icon: str
    route: str

    @field_validator("icon", mode="before")
    @classmethod
    def _convert_icon_url(cls, v: str) -> str:
        if "MonsterIcon" in v:
            return f"https://gi.yatta.moe/assets/UI/monster/{v}.png"
        return f"https://gi.yatta.moe/assets/UI/{v}.png"
