from __future__ import annotations

from pydantic import Field, field_validator

from ._base import BaseModel

__all__ = ("Book", "BookDetail", "BookVolume")


class BookVolume(BaseModel):
    """Represents a single volume or chapter within a book.

    Attributes:
        id: The unique ID of this volume.
        name: The name or title of the volume.
        description: The text content of the volume.
        story_id: An associated story ID.
    """

    id: int
    name: str
    description: str
    story_id: int = Field(alias="storyId")


class BookDetail(BaseModel):
    """Represents detailed information about a book, including its volumes.

    Attributes:
        id: The unique ID of the book.
        name: The name or title of the book.
        rarity: The rarity rank of the book item.
        icon: The icon URL for the book item.
        volumes: A list of volumes contained within the book.
    """

    id: int
    name: str
    rarity: int = Field(alias="rank")
    icon: str
    volumes: list[BookVolume] = Field(alias="volume")

    @field_validator("icon", mode="before")
    @classmethod
    def _convert_icon_url(cls, v: str) -> str:
        return f"https://gi.yatta.moe/assets/UI/{v}.png"


class Book(BaseModel):
    """Represents a book summary.

    Attributes:
        id: The unique ID of the book.
        name: The name or title of the book.
        rarity: The rarity rank of the book item.
        icon: The icon URL for the book item.
        route: The route identifier for the book.
    """

    id: int
    name: str
    rarity: int = Field(alias="rank")
    icon: str
    route: str

    @field_validator("icon", mode="before")
    @classmethod
    def _convert_icon_url(cls, v: str) -> str:
        return f"https://gi.yatta.moe/assets/UI/{v}.png"
