from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field, field_validator


class MonsterReward(BaseModel):
    id: int
    rarity: int = Field(alias="rank")
    icon: str
    count: Optional[float] = Field(None)

    @field_validator("icon", mode="before")
    def _convert_icon_url(cls, v: str) -> str:
        return f"https://api.ambr.top/assets/UI/{v}.png"


class MonsterEntry(BaseModel):
    id: int
    type: str
    rewards: List[MonsterReward] = Field(alias="reward")

    @field_validator("rewards", mode="before")
    def _convert_rewards(
        cls, v: Optional[Dict[str, Dict[str, Any]]]
    ) -> List[MonsterReward]:
        return (
            [MonsterReward(id=int(item_id), **v[item_id]) for item_id in v] if v else []
        )


class MonsterDetail(BaseModel):
    id: int
    name: str
    type: str
    icon: str
    route: str
    title: Optional[str]
    special_name: Optional[str] = Field(alias="specialName")
    description: str
    entries: List[MonsterEntry]

    @field_validator("icon", mode="before")
    def _convert_icon_url(cls, v: str) -> str:
        return f"https://api.ambr.top/assets/UI/{v}.png"

    @field_validator("entries", mode="before")
    def _convert_entries(cls, v: Dict[str, Dict[str, Any]]) -> List[MonsterEntry]:
        return [MonsterEntry(**v[item_id]) for item_id in v]


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
        return f"https://api.ambr.top/assets/UI/{v}.png"
