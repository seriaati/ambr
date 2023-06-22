from typing import Any, Dict, List

from pydantic import BaseModel, Field, validator


class AchievementReward(BaseModel):
    """
    Represents an achievement reward.

    Attributes
    ----------
    rarity: :class:`int`
        The achievement reward's rarity.
    count: :class:`int`
        The achievement reward's count.
    icon: :class:`str`
        The achievement reward's icon.
    """

    rarity: int = Field(alias="rank")
    count: int
    icon: str

    @validator("icon", pre=True)
    def _add_icon_url(cls, v: str) -> str:
        return f"https://api.ambr.top/assets/UI/{v}.png"


class AchievementDetail(BaseModel):
    """
    Represents an achievement detail.

    Attributes
    ----------
    id: :class:`int`
        The achievement detail's ID.
    title: :class:`str`
        The achievement detail's title.
    description: :class:`str`
        The achievement detail's description.
    rewards: List[:class:`AchievementReward`]
        The achievement detail's rewards.
    """

    id: int
    title: str
    description: str
    rewards: List[AchievementReward]

    @validator("rewards", pre=True)
    def _add_rewards(cls, v: Dict[str, Dict[str, Any]]) -> List[AchievementReward]:
        return [AchievementReward(**v[item_id]) for item_id in v]


class Achievement(BaseModel):
    """
    Represents an achievement.

    Attributes
    ----------
    id: :class:`int`
        The achievement's ID.
    order: :class:`int`
        The achievement's order.
    details: List[:class:`AchievementDetail`]
        The achievement's details.
    """

    id: int
    order: int
    details: List[AchievementDetail]

    @validator("details", pre=True)
    def _add_details(cls, v: List[Dict[str, Any]]) -> List[AchievementDetail]:
        return [AchievementDetail(**detail) for detail in v]


class AchievementCategory(BaseModel):
    """
    Represents an achievement category.

    Attributes
    ----------
    id: :class:`int`
        The achievement category's ID.
    name: :class:`str`
        The achievement category's name.
    order: :class:`int`
        The achievement category's order.
    icon: :class:`str`
        The achievement category's icon.
    achievements: List[:class:`Achievement`]
        The achievement category's achievements.
    """

    id: int
    name: str
    order: int
    icon: str
    achievements: List[Achievement] = Field(alias="achievementList")

    @validator("icon", pre=True)
    def _add_icon_url(cls, v: str) -> str:
        return f"https://api.ambr.top/assets/UI/{v}.png"

    @validator("achievements", pre=True)
    def _add_achievements(cls, v: Dict[str, Dict[str, Any]]) -> List[Achievement]:
        return [Achievement(**v[achievement_id]) for achievement_id in v]
