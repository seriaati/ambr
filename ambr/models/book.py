from typing import List

from pydantic import BaseModel, Field, field_validator

__all__ = (
    "BookVolume",
    "BookDetail",
    "Book",
)


class BookVolume(BaseModel):
    """
    Represents a book volume.

    Attributes
    ----------
    id: :class:`int`
        The book volume's ID.
    name: :class:`str`
        The book volume's name.
    description: :class:`str`
        The book volume's description.
    story_id: :class:`int`
        The book volume's story ID.
    """

    id: int
    name: str
    description: str
    story_id: int = Field(alias="storyId")


class BookDetail(BaseModel):
    """
    Represents a book detail.

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
    volumes: List[:class:`BookVolume`]
        The book's volumes.
    """

    id: int
    name: str
    rarity: int = Field(alias="rank")
    icon: str
    volumes: List[BookVolume] = Field(alias="volume")

    @field_validator("icon", mode="before")
    def _convert_icon_url(cls, v: str) -> str:
        return f"https://api.ambr.top/assets/UI/{v}.png"


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

    @field_validator("icon", mode="before")
    def _convert_icon_url(cls, v: str) -> str:
        return f"https://api.ambr.top/assets/UI/{v}.png"
