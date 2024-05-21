from typing import Any

from pydantic import BaseModel, Field, field_validator

__all__ = (
    "Achievement",
    "AchievementCategory",
    "AchievementDetail",
    "AchievementReward",
)


class AchievementReward(BaseModel):
    """
    Represents an achievement reward.

    Attributes:
        rarity (int): The achievement reward's rarity.
        amount (int): The achievement reward's amount.
        icon (str): The achievement reward's icon.
    """

    rarity: int = Field(alias="rank")
    amount: int = Field(alias="count")
    icon: str

    @field_validator("icon", mode="before")
    def _convert_icon_url(cls, v: str) -> str:
        return f"https://api.ambr.top/assets/UI/{v}.png"


class AchievementDetail(BaseModel):
    """
    Represents an achievement detail.

    Attributes:
        id (int): The achievement's ID.
        title (str): The achievement's title.
        description (str): The achievement's description.
        rewards (list[AchievementReward]): The achievement's rewards.
    """

    id: int
    title: str
    description: str
    rewards: list[AchievementReward]

    @field_validator("rewards", mode="before")
    def _convert_rewards(cls, v: dict[str, dict[str, Any]]) -> list[AchievementReward]:
        return [AchievementReward(**v[item_id]) for item_id in v]


class Achievement(BaseModel):
    """
    Represents an achievement.

    Attributes:
        id (int): The achievement's ID.
        order (int): The achievement's order.
        details (list[AchievementDetail]): The achievement's details.
    """

    id: int
    order: int
    details: list[AchievementDetail]


class AchievementCategory(BaseModel):
    """
    Represents an achievement category.

    Attributes:
        id (int): The achievement category's ID.
        name (str): The achievement category's name.
        order (int): The achievement category's order.
        icon (str): The achievement category's icon.
        achievements (list[Achievement]): The achievement category's achievements.
    """

    id: int
    name: str
    order: int
    icon: str
    achievements: list[Achievement] = Field(alias="achievementList")

    @field_validator("icon", mode="before")
    def _convert_icon_url(cls, v: str) -> str:
        return f"https://api.ambr.top/assets/UI/{v}.png"

    @field_validator("achievements", mode="before")
    def _convert_achievements(cls, v: dict[str, dict[str, Any]]) -> list[Achievement]:
        return [Achievement(**v[achievement_id]) for achievement_id in v]
