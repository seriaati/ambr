from typing import Optional

from pydantic import BaseModel, Field, field_validator


class Quest(BaseModel):
    """
    Represents a quest.

    Attributes
    ----------
    id: :class:`int`
        The quest's ID.
    type: :class:`str`
        The quest's type.
    chapter_num: Optional[:class:`str`]
        The quest's chapter number.
    chapter_title: :class:`str`
        The quest's chapter title.
    chapter_icon: Optional[:class:`str`]
        The quest's chapter icon.
    chapter_image_title: :class:`str`
        The quest's chapter image title.
    route: :class:`str`
        The quest's route.
    chapter_count: :class:`int`
        The quest's chapter count.
    """

    id: int
    type: Optional[str]
    chapter_num: Optional[str] = Field(alias="chapterNum")
    chapter_title: str = Field(alias="chapterTitle")
    chapter_icon: Optional[str] = Field(alias="chapterIcon")
    chapter_image_title: Optional[str] = Field(alias="chapterImageTitle")
    route: str
    chapter_count: int = Field(alias="chapterCount")

    @field_validator("chapter_icon", mode="before")
    def _convert_icon_url(cls, v: str) -> str:
        return f"https://api.ambr.top/assets/UI/{v}.png"
