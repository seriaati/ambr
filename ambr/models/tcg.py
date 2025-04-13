from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field, field_validator

from ..utils import remove_html_tags, replace_placeholders

__all__ = ("CardDictionary", "CardTag", "CardTalent", "DiceCost", "TCGCard", "TCGCardDetail")


class CardTag(BaseModel):
    """Represents a tag associated with a TCG card.

    Attributes:
        id: The tag's identifier string.
        name: The tag's display name.
    """

    id: str
    name: str


class DiceCost(BaseModel):
    """Represents the dice cost for a TCG card action.

    Attributes:
        type: The type of dice required (e.g., "GCG_COST_DICE_PYRO", "GCG_COST_DICE_VOID").
        amount: The number of dice required.
    """

    type: str
    amount: int = Field(alias="count")


class CardDictionary(BaseModel):
    """Represents a dictionary entry (like a skill description) for a TCG card.

    Attributes:
        id: The dictionary entry's ID.
        name: The name of the entry (e.g., skill name).
        params: Optional parameters used for placeholder replacement in the description.
        description: The detailed description of the entry.
        cost: The dice cost associated with this entry, if any.
    """

    id: str
    name: str
    params: dict[str, Any] | None = None
    description: str
    cost: list[DiceCost] = Field(alias="diceCost", default_factory=list)

    @field_validator("name", mode="before")
    @classmethod
    def _format_name(cls, v: str) -> str:
        return remove_html_tags(v)

    @field_validator("cost", mode="before")
    @classmethod
    def _convert_cost(cls, v: dict[str, int] | None) -> list[DiceCost]:
        return [DiceCost(type=type_, count=count) for type_, count in v.items()] if v else []

    @field_validator("description", mode="before")
    @classmethod
    def _format_description(cls, v: str, values: Any) -> str:
        params = values.data.get("params")
        if params:
            v = replace_placeholders(v, params)
        return remove_html_tags(v)


class CardTalent(BaseModel):
    """Represents a talent or skill associated with a TCG card.

    Attributes:
        id: The talent's ID.
        name: The talent's name.
        params: Optional parameters used for placeholder replacement in the description.
        description: The detailed description of the talent.
        cost: The dice cost to use the talent.
        tags: A list of tags associated with the talent.
        icon: The icon URL for the talent.
        sub_skills: Optional dictionary of sub-skills related to this talent.
    """

    id: str
    name: str
    params: dict[str, Any] | None
    description: str
    cost: list[DiceCost]
    tags: list[CardTag]
    icon: str
    sub_skills: dict[str, Any] | None = Field(None, alias="subSkills")

    @field_validator("description", mode="before")
    @classmethod
    def _format_description(cls, v: str, values: Any) -> str:
        params = values.data.get("params")
        if params:
            v = replace_placeholders(v, params)
        return remove_html_tags(v)

    @field_validator("cost", mode="before")
    @classmethod
    def _convert_cost(cls, v: dict[str, int] | None) -> list[DiceCost]:
        return [DiceCost(type=type_, count=count) for type_, count in v.items()] if v else []

    @field_validator("tags", mode="before")
    @classmethod
    def _convert_tags(cls, v: dict[str, str] | None) -> list[CardTag]:
        return [CardTag(id=id_, name=name) for id_, name in v.items()] if v else []

    @field_validator("icon", mode="before")
    @classmethod
    def _convert_icon_url(cls, v: str) -> str:
        return f"https://gi.yatta.moe/assets/UI/{v}.png"

    @property
    def small_icon(self) -> str:
        """Returns the URL for the small version of the talent icon."""
        return self.icon.replace(".png", ".sm.png")


class TCGCardDetail(BaseModel):
    """Represents detailed information about a TCG card.

    Attributes:
        id: The card's unique ID.
        name: The card's name.
        type: The type of card (e.g., "GCG_CARD_CHARACTER", "GCG_CARD_EVENT").
        tags: A list of tags associated with the card.
        props: Optional properties, often representing dice cost or other stats.
        icon: The main icon URL for the card.
        route: The route identifier for the card.
        story_title: The title of the card's story/flavor text.
        story_detail: The main body of the card's story/flavor text.
        source: How the card is obtained.
        dictionaries: Associated dictionary entries (skills, effects).
        talents: Associated talents or special skills.
    """

    id: int
    name: str
    type: str
    tags: list[CardTag]
    props: dict[str, int] | None
    icon: str
    route: str
    story_title: str = Field(alias="storyTitle")
    story_detail: str = Field(alias="storyDetail")
    source: str
    dictionaries: list[CardDictionary] = Field(alias="dictionary")
    talents: list[CardTalent] = Field(alias="talent")

    @field_validator("tags", mode="before")
    @classmethod
    def _convert_tags(cls, v: dict[str, str] | None) -> list[CardTag]:
        return [CardTag(id=id_, name=name) for id_, name in v.items()] if v else []

    @field_validator("icon", mode="before")
    @classmethod
    def _convert_icon_url(cls, v: str) -> str:
        return f"https://gi.yatta.moe/assets/UI/gcg/{v}.png"

    @property
    def small_icon(self) -> str:
        """Returns the URL for the small version of the card icon."""
        return self.icon.replace(".png", ".sm.png")

    @field_validator("dictionaries", mode="before")
    @classmethod
    def _convert_dictionaries(cls, v: dict[str, dict[str, Any]] | None) -> list[CardDictionary]:
        return [CardDictionary(id=item_id, **v[item_id]) for item_id in v] if v else []

    @field_validator("talents", mode="before")
    @classmethod
    def _convert_talents(cls, v: dict[str, dict[str, Any]]) -> list[CardTalent]:
        return [CardTalent(id=item_id, **v[item_id]) for item_id in v]


class TCGCard(BaseModel):
    """Represents a TCG card summary.

    Attributes:
        id: The card's unique ID.
        name: The card's name.
        type: The type of card (e.g., "GCG_CARD_CHARACTER", "GCG_CARD_EVENT").
        tags: A list of tags associated with the card.
        dice_cost: The dice cost required to play the card.
        icon: The main icon URL for the card.
        route: The route identifier for the card.
        sort_order: The sorting order value for the card.
    """

    id: int
    name: str
    type: str
    tags: list[CardTag]
    dice_cost: list[DiceCost] = Field(alias="props", default_factory=list)
    icon: str
    route: str
    sort_order: int = Field(alias="sortOrder")

    @field_validator("tags", mode="before")
    @classmethod
    def _convert_tags(cls, v: dict[str, str] | None) -> list[CardTag]:
        return [CardTag(id=id_, name=name) for id_, name in v.items()] if v else []

    @field_validator("dice_cost", mode="before")
    @classmethod
    def _convert_dice_cost(cls, v: dict[str, int] | None) -> list[DiceCost]:
        return [DiceCost(type=type_, count=count) for type_, count in v.items()] if v else []

    @field_validator("icon", mode="before")
    @classmethod
    def _convert_icon_url(cls, v: str) -> str:
        return f"https://gi.yatta.moe/assets/UI/gcg/{v}.png"

    @property
    def small_icon(self) -> str:
        """Returns the URL for the small version of the card icon."""
        return self.icon.replace(".png", ".sm.png")
