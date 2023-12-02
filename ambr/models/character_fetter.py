from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field, field_validator

from ..utils import remove_html_tags, replace_pronouns

__all__ = ("Quest", "Task", "Quote", "Story", "CharacterFetter")


class Quest(BaseModel):
    id: int
    quest_title: Optional[str] = Field(None, alias="questTitle")
    chapter_id: int = Field(alias="chapterId")
    chapter_title: str = Field(alias="chapterTitle")


class Task(BaseModel):
    type: str
    quest_list: List[Quest] = Field(alias="questList")


class Quote(BaseModel):
    title: str
    audio_id: str = Field(alias="audio")
    text: str
    tips: Optional[str]
    tasks: List[Task]

    @field_validator("text", mode="before")
    def _format_text(cls, v: str) -> str:
        return remove_html_tags(replace_pronouns(v))

    @field_validator("tips", mode="before")
    def _convert_empty_tips(cls, v: str) -> Optional[str]:
        return v if v else None

    @field_validator("tasks", mode="before")
    def _convert_empty_tasks(cls, v: Optional[List[Dict[str, Any]]]) -> List[Task]:
        if v is None:
            return []
        return [Task(**task) for task in v]


class Story(BaseModel):
    title: str
    title2: Optional[str]
    text: str
    text2: Optional[str]
    tips: Optional[str]

    @field_validator("text", mode="before")
    def _format_text(cls, v: str) -> str:
        return remove_html_tags(replace_pronouns(v))

    @field_validator("text2", mode="before")
    def _format_text2(cls, v: Optional[str]) -> Optional[str]:
        return remove_html_tags(replace_pronouns(v)) if v else None

    @field_validator("tips", mode="before")
    def _convert_empty_tips(cls, v: str) -> Optional[str]:
        return v if v else None


class CharacterFetter(BaseModel):
    quotes: List[Quote]
    stories: List[Story] = Field(alias="story")

    @field_validator("quotes", mode="before")
    def _flatten_quotes(cls, v: Dict[str, Dict[str, Any]]) -> List[Quote]:
        return [Quote(**quote) for quote in v.values()]

    @field_validator("stories", mode="before")
    def _flatten_stories(cls, v: Dict[str, Dict[str, Any]]) -> List[Story]:
        return [Story(**story) for story in v.values()]
