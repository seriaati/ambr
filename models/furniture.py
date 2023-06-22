from typing import List, Optional

from pydantic import BaseModel, Field, validator


class Furniture(BaseModel):
    """
    Represents a furniture.

    Attributes
    ----------
    id: :class:`int`
        The furniture's ID.
    name: :class:`str`
        The furniture's name.
    cost: Optional[:class:`int`]
        The furniture's cost.
    comfort: Optional[:class:`int`]
        The furniture's comfort.
    rarity: :class:`int`
        The furniture's rarity.
    icon: :class:`str`
        The furniture's icon.
    route: :class:`str`
        The furniture's route.
    categories: List[:class:`str`]
        The furniture's categories.
    types: List[:class:`str`]
        The furniture's types.
    """

    id: int
    name: str
    cost: Optional[int]
    comfort: Optional[int]
    rarity: int = Field(alias="rank")
    icon: str
    route: str
    categories: List[str]
    types: List[str]

    @validator("icon", pre=True)
    def _add_icon_url(cls, v: str) -> str:
        return f"https://api.ambr.top/assets/UI/{v}.png"


class FurnitureSet(BaseModel):
    id: int
    name: str
    icon: str
    route: str
    categories: List[str]
    types: List[str]

    @validator("icon", pre=True)
    def _add_icon_url(cls, v: str) -> str:
        return f"https://api.ambr.top/assets/UI/{v}.png"
