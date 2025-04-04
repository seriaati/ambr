from __future__ import annotations

from pydantic import BaseModel, Field, field_validator

from ambr.utils import remove_html_tags

__all__ = ("Book", "BookDetail", "BookVolume")


class BookVolume(BaseModel):
    """
    Represents a book volume.

    Attributes:
        id (int): The book volume's ID.
        name (str): The book volume's name.
        description (str): The book volume's description.
        story_id (int): The book volume's story ID.
    """

    id: int
    name: str
    description: str
    story_id: int = Field(alias="storyId")

    @field_validator("description", mode="before")
    @classmethod
    def __format_description(cls, v: str) -> str:
        return remove_html_tags(v)

    @field_validator("name", "description", mode="before")
    def __convert_name(cls, v: str | int) -> str:
        return str(v)


class BookDetail(BaseModel):
    """
    Represents a book detail.

    Attributes:
        id (int): The book's ID.
        name (str): The book's name.
        rarity (int): The book's rarity.
        icon (str): The book's icon.
        volumes (list[BookVolume]): The book's volumes.
    """

    id: int
    name: str
    rarity: int = Field(alias="rank")
    icon: str
    volumes: list[BookVolume] = Field(alias="volume")

    @field_validator("icon", mode="before")
    def _convert_icon_url(cls, v: str) -> str:
        return f"https://gi.yatta.moe/assets/UI/{v}.png"

    @field_validator("name", mode="before")
    def __convert_name(cls, v: str | int) -> str:
        return str(v)


class Book(BaseModel):
    """
    Represents a book.

    Attributes:
        id (int): The book's ID.
        name (str): The book's name.
        rarity (int): The book's rarity.
        icon (str): The book's icon.
        route (str): The book's route.
    """

    id: int
    name: str
    rarity: int = Field(alias="rank")
    icon: str
    route: str

    @field_validator("icon", mode="before")
    def _convert_icon_url(cls, v: str) -> str:
        return f"https://gi.yatta.moe/assets/UI/{v}.png"

    @field_validator("name", mode="before")
    def __convert_name(cls, v: str | int) -> str:
        return str(v)
