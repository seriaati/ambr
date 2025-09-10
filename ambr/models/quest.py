from __future__ import annotations

from pydantic import Field, field_validator

from ._base import BaseModel

__all__ = ("Quest",)


class Quest(BaseModel):
    """Represents a quest summary.

    Attributes:
        id: The quest's unique ID.
        type: The type or category of the quest (optional).
        chapter_num: The chapter number associated with the quest (optional).
        chapter_title: The title of the quest chapter.
        chapter_icon: The icon URL for the quest chapter (optional).
        chapter_image_title: The title associated with the chapter image (optional).
        route: The route identifier for the quest.
        chapter_count: The count related to the quest chapter.
    """

    id: int
    type: str | None
    chapter_num: str | None = Field(alias="chapterNum")
    chapter_title: str = Field(alias="chapterTitle")
    chapter_icon: str | None = Field(alias="chapterIcon")
    chapter_image_title: str | None = Field(alias="chapterImageTitle")
    route: str
    chapter_count: int = Field(alias="chapterCount")

    @field_validator("chapter_icon", mode="before")
    @classmethod
    def _convert_icon_url(cls, v: str) -> str:
        return f"https://gi.yatta.moe/assets/UI/{v}.png"
