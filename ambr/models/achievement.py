from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field, field_validator

__all__ = ("Achievement", "AchievementCategory", "AchievementDetail", "AchievementReward")


class AchievementReward(BaseModel):
    """Represents a reward granted for completing an achievement.

    Attributes:
        rarity: The rarity rank of the reward item (often Primogems).
        amount: The quantity of the reward item granted.
        icon: The icon URL for the reward item.
    """

    rarity: int = Field(alias="rank")
    amount: int = Field(alias="count")
    icon: str

    @field_validator("icon", mode="before")
    @classmethod
    def _convert_icon_url(cls, v: str) -> str:
        return f"https://gi.yatta.moe/assets/UI/{v}.png"


class AchievementDetail(BaseModel):
    """Represents the details of a specific achievement.

    Attributes:
        id: The unique ID of the achievement.
        title: The title or name of the achievement.
        description: The description or requirement for the achievement.
        rewards: A list of rewards granted upon completion.
    """

    id: int
    title: str
    description: str
    rewards: list[AchievementReward]

    @field_validator("rewards", mode="before")
    @classmethod
    def _convert_rewards(cls, v: dict[str, dict[str, Any]]) -> list[AchievementReward]:
        return [AchievementReward(**v[item_id]) for item_id in v]


class Achievement(BaseModel):
    """Represents an achievement, potentially with multiple stages or levels.

    Attributes:
        id: The base ID for the achievement (stages might share this).
        order: The display order of the achievement within its category.
        details: A list containing details for each stage or level of the achievement.
    """

    id: int
    order: int
    details: list[AchievementDetail]


class AchievementCategory(BaseModel):
    """Represents a category of achievements.

    Attributes:
        id: The unique ID of the achievement category.
        name: The name of the category (e.g., "Wonders of the World").
        order: The display order of the category.
        icon: The icon URL for the category.
        achievements: A list of achievements belonging to this category.
    """

    id: int
    name: str
    order: int
    icon: str
    achievements: list[Achievement] = Field(alias="achievementList")

    @field_validator("icon", mode="before")
    @classmethod
    def _convert_icon_url(cls, v: str) -> str:
        return f"https://gi.yatta.moe/assets/UI/{v}.png"

    @field_validator("achievements", mode="before")
    @classmethod
    def _convert_achievements(cls, v: dict[str, dict[str, Any]]) -> list[Achievement]:
        return [Achievement(**v[achievement_id]) for achievement_id in v]
