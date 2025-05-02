from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field, field_validator

from ..utils import remove_html_tags, replace_pronouns

__all__ = ("CharacterFetter", "Quest", "Quote", "Story", "Task")


class Quest(BaseModel):
    """Represents a quest related to unlocking a character quote or story.

    Attributes:
        id: The ID of the quest.
        quest_title: The title of the specific quest (optional).
        chapter_id: The ID of the chapter the quest belongs to.
        chapter_title: The title of the chapter the quest belongs to.
    """

    id: int
    quest_title: str | None = Field(None, alias="questTitle")
    chapter_id: int = Field(alias="chapterId")
    chapter_title: str = Field(alias="chapterTitle")


class Task(BaseModel):
    """Represents a task or condition required to unlock a character quote.

    Attributes:
        type: The type of task (e.g., "FETTER_TASK_FINISH_QUEST").
        quest_list: A list of quests associated with this task.
    """

    type: str
    quest_list: list[Quest] = Field(alias="questList")


class Quote(BaseModel):
    """Represents a character voice-over quote.

    Attributes:
        title: The title or category of the quote (e.g., "Chat: Knights").
        audio_id: The identifier for the audio file associated with the quote.
        text: The transcribed text of the quote.
        tips: Optional tips or context related to the quote.
        tasks: A list of tasks required to unlock this quote.
    """

    title: str
    audio_id: str = Field(alias="audio")
    text: str
    tips: str | None
    tasks: list[Task]

    @field_validator("text", mode="before")
    @classmethod
    def _format_text(cls, v: str) -> str:
        return remove_html_tags(replace_pronouns(v))

    @field_validator("tips", mode="before")
    @classmethod
    def _convert_empty_tips(cls, v: str | int) -> str | None:
        return str(v) or None

    @field_validator("tasks", mode="before")
    @classmethod
    def _convert_empty_tasks(cls, v: list[dict[str, Any]] | None) -> list[Task]:
        if v is None:
            return []
        return [Task(**task) for task in v]


class Story(BaseModel):
    """Represents a character story entry.

    Attributes:
        title: The title of the story entry (e.g., "Character Story 1").
        title2: An alternative or secondary title (optional).
        text: The main text content of the story entry.
        text2: Alternative or secondary text content (optional).
        tips: Optional tips or context related to the story entry.
    """

    title: str
    title2: str | None
    text: str
    text2: str | None
    tips: str | None

    @field_validator("text", mode="before")
    @classmethod
    def _format_text(cls, v: str) -> str:
        return remove_html_tags(replace_pronouns(v))

    @field_validator("text2", mode="before")
    @classmethod
    def _format_text2(cls, v: str | None) -> str | None:
        return remove_html_tags(replace_pronouns(v)) if v else None

    @field_validator("tips", mode="before")
    @classmethod
    def _convert_empty_tips(cls, v: str | int) -> str | None:
        return str(v) or None


class CharacterFetter(BaseModel):
    """Container for character quotes and stories (fetter information).

    Attributes:
        quotes: A list of character voice-over quotes.
        stories: A list of character story entries.
    """

    quotes: list[Quote]
    stories: list[Story] = Field(alias="story")

    @field_validator("quotes", mode="before")
    @classmethod
    def _flatten_quotes(cls, v: dict[str, dict[str, Any]]) -> list[Quote]:
        return [Quote(**quote) for quote in v.values()]

    @field_validator("stories", mode="before")
    @classmethod
    def _flatten_stories(cls, v: dict[str, dict[str, Any]]) -> list[Story]:
        return [Story(**story) for story in v.values()]
