from typing import Any

from pydantic import BaseModel, Field, field_validator

from ..utils import remove_html_tags, replace_pronouns

__all__ = ("Quest", "Task", "Quote", "Story", "CharacterFetter")


class Quest(BaseModel):
    id: int
    quest_title: str | None = Field(None, alias="questTitle")
    chapter_id: int = Field(alias="chapterId")
    chapter_title: str = Field(alias="chapterTitle")


class Task(BaseModel):
    type: str
    quest_list: list[Quest] = Field(alias="questList")


class Quote(BaseModel):
    """
    Represents a quote.

    Attributes
    ----------
    title: :class:`str`
        The quote's title.
    audio_id: :class:`str`
        The quote's audio ID.
    text: :class:`str`
        The quote's text.
    tips: Optional[:class:`str`]
        The quote's tips.
    tasks: List[:class:`Task`]
        The quote's tasks.
    """

    title: str
    audio_id: str = Field(alias="audio")
    text: str
    tips: str | None
    tasks: list[Task]

    @field_validator("text", mode="before")
    def _format_text(cls, v: str) -> str:
        return remove_html_tags(replace_pronouns(v))

    @field_validator("tips", mode="before")
    def _convert_empty_tips(cls, v: str) -> str | None:
        return v if v else None

    @field_validator("tasks", mode="before")
    def _convert_empty_tasks(cls, v: list[dict[str, Any]] | None) -> list[Task]:
        if v is None:
            return []
        return [Task(**task) for task in v]


class Story(BaseModel):
    title: str
    title2: str | None
    text: str
    text2: str | None
    tips: str | None

    @field_validator("text", mode="before")
    def _format_text(cls, v: str) -> str:
        return remove_html_tags(replace_pronouns(v))

    @field_validator("text2", mode="before")
    def _format_text2(cls, v: str | None) -> str | None:
        return remove_html_tags(replace_pronouns(v)) if v else None

    @field_validator("tips", mode="before")
    def _convert_empty_tips(cls, v: str) -> str | None:
        return v if v else None


class CharacterFetter(BaseModel):
    quotes: list[Quote]
    stories: list[Story] = Field(alias="story")

    @field_validator("quotes", mode="before")
    def _flatten_quotes(cls, v: dict[str, dict[str, Any]]) -> list[Quote]:
        return [Quote(**quote) for quote in v.values()]

    @field_validator("stories", mode="before")
    def _flatten_stories(cls, v: dict[str, dict[str, Any]]) -> list[Story]:
        return [Story(**story) for story in v.values()]
