from __future__ import annotations

from typing import Any

from pydantic import Field, field_validator, model_validator

from ._base import BaseModel

__all__ = ("Quest", "QuestDetail", "QuestReward", "QuestStep", "QuestStory")


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
    def _convert_icon_url(cls, v: str | None) -> str | None:
        if v is None:
            return None
        return f"https://gi.yatta.moe/assets/UI/{v}.png"


class QuestReward(BaseModel):
    """Represents a reward granted for completing a quest.

    Attributes:
        id: The ID of the reward item.
        icon: The icon URL of the reward item (None if the API has no data for the item).
        type: The type of the reward (empty if the API has no data for the item).
        rarity: The rarity rank of the reward item (None if the API has no data for the item).
        count: The amount rewarded.
    """

    id: int
    icon: str | None
    type: str
    rarity: int | None = Field(alias="rank")
    count: int

    @field_validator("icon", mode="before")
    @classmethod
    def _convert_icon_url(cls, v: str) -> str | None:
        if not v:
            return None
        return f"https://gi.yatta.moe/assets/UI/{v}.png"

    @field_validator("rarity", mode="before")
    @classmethod
    def _convert_empty_rarity(cls, v: int | str) -> int | str | None:
        return None if isinstance(v, str) and not v else v


class QuestStep(BaseModel):
    """Represents a single step (objective) within a quest.

    Attributes:
        id: The step's unique ID.
        is_hidden: Whether the step is hidden from the player.
        title: The objective text shown to the player (optional).
        step_description: Additional description for the step (optional).
        task_data: Raw task data, including dialogue trees, as returned by the API (optional).
    """

    id: int
    is_hidden: bool = Field(alias="isHidden")
    title: str | None
    step_description: str | None = Field(alias="stepDescription")
    task_data: list[dict[str, Any]] | None = Field(alias="taskData")


class QuestStory(BaseModel):
    """Represents a single quest within a quest chapter.

    Attributes:
        id: The quest's unique ID.
        title: The title of the quest.
        description: The description of the quest.
        rewards: A list of rewards for completing the quest.
        suggested_quests: A mapping of quest ID to title for quests suggested to track next.
        steps: The ordered steps (objectives) of the quest.
    """

    id: int
    title: str
    description: str
    rewards: list[QuestReward] = Field(alias="reward")
    suggested_quests: dict[int, str] = Field(alias="suggestTrackMainQuestList")
    steps: list[QuestStep] = Field(alias="story")

    @model_validator(mode="before")
    @classmethod
    def _flatten_info(cls, v: dict[str, Any]) -> dict[str, Any]:
        info = v.pop("info", {})
        return {**info, **v}

    @field_validator("rewards", mode="before")
    @classmethod
    def _convert_rewards(cls, v: dict[str, dict[str, Any]] | None) -> list[QuestReward]:
        if v is None:
            return []
        return [QuestReward(**reward) for reward in v.values()]

    @field_validator("suggested_quests", mode="before")
    @classmethod
    def _convert_suggested_quests(cls, v: dict[str, str] | None) -> dict[str, str]:
        return v or {}

    @field_validator("steps", mode="before")
    @classmethod
    def _convert_steps(cls, v: dict[str, dict[str, Any]]) -> list[QuestStep]:
        return [QuestStep(**step) for step in v.values()]


class QuestDetail(BaseModel):
    """Represents detailed information about a quest chapter and the quests within it.

    Attributes:
        info: Summary information about the quest chapter.
        stories: The quests that make up this chapter.
    """

    info: Quest
    stories: list[QuestStory] = Field(alias="storyList")

    @field_validator("stories", mode="before")
    @classmethod
    def _convert_stories(cls, v: dict[str, dict[str, Any]]) -> list[QuestStory]:
        return [QuestStory(**story) for story in v.values()]
