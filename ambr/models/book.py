from typing import Any, Dict, List

from pydantic import BaseModel, Field, validator


class BookVolume(BaseModel):
    id: int
    name: str
    description: str
    story_id: int = Field(alias="storyId")


class BookDetail(BaseModel):
    id: int
    name: str
    rarity: int = Field(alias="rank")
    icon: str
    volumes: List[BookVolume] = Field(alias="volume")

    @validator("icon", pre=True)
    def _convert_icon_url(cls, v: str) -> str:
        return f"https://api.ambr.top/assets/UI/{v}.png"

    @validator("volumes", pre=True)
    def _convert_volumes(cls, v: List[Dict[str, Any]]) -> List[BookVolume]:
        return [BookVolume(**volume) for volume in v]


class Book(BaseModel):
    """
    Represents a book.

    Attributes
    ----------
    id: :class:`int`
        The book's ID.
    name: :class:`str`
        The book's name.
    rarity: :class:`int`
        The book's rarity.
    icon: :class:`str`
        The book's icon.
    route: :class:`str`
        The book's route.
    """

    id: int
    name: str
    rarity: int = Field(alias="rank")
    icon: str
    route: str

    @validator("icon", pre=True)
    def _convert_icon_url(cls, v: str) -> str:
        return f"https://api.ambr.top/assets/UI/{v}.png"
