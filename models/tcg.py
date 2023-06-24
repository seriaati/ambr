from typing import Dict, List, Optional

from pydantic import BaseModel, Field, validator


class DiceCost(BaseModel):
    type: str
    count: int


class TCGCard(BaseModel):
    """
    Represents a TCG card.

    Attributes
    ----------
    id: :class:`int`
        The card's ID.
    name: :class:`str`
        The card's name.
    type: :class:`str`
        The card's type.
    tags: Dict[:class:`str`, :class:`str`]
        The card's tags.
    dice_cost: Dict[:class:`str`, :class:`int`]
        The card's properties.
    icon: :class:`str`
        The card's icon.
    route: :class:`str`
        The card's route.
    sort_order: :class:`int`
        The card's sort order.
    """

    id: int
    name: str
    type: str
    tags: Dict[str, str]
    dice_cost: List[DiceCost] = Field(None, alias="props")
    icon: str
    route: str
    sort_order: int = Field(alias="sortOrder")

    @validator("dice_cost", pre=True)
    def _convert_dice_cost(cls, v: Optional[Dict[str, int]]) -> List[DiceCost]:
        return (
            [DiceCost(type=type_, count=count) for type_, count in v.items()]
            if v
            else []
        )

    @validator("icon", pre=True)
    def _add_icon_url(cls, v: str) -> str:
        return f"https://api.ambr.top/assets/UI/{v}.png"
