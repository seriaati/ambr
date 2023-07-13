from typing import Optional

from pydantic import BaseModel, Field, validator


class NameCardDetail(BaseModel):
    id: int
    name: str
    rarity: int = Field(alias="rank")
    icon: str
    route: str
    description: str
    description_special: str = Field(alias="descriptionSpecial")
    source: Optional[str]

    @validator("icon", pre=True)
    def _convert_icon_url(cls, v: str) -> str:
        return f"https://api.ambr.top/assets/UI/{v}.png"


class NameCard(BaseModel):
    """
    Represents a name card.

    Attributes
    ----------
    id: :class:`int`
        The name card's ID.
    name: :class:`str`
        The name card's name.
    type: :class:`str`
        The name card's type.
    rarity: :class:`int`
        The name card's rarity.
    icon: :class:`str`
        The name card's icon.
    route: :class:`str`
        The name card's route.
    """

    id: int
    name: str
    type: str
    rarity: int = Field(alias="rank")
    icon: str
    route: str

    @validator("icon", pre=True)
    def _convert_icon_url(cls, v: str) -> str:
        return f"https://api.ambr.top/assets/UI/{v}.png"