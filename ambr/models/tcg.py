from typing import Any

from pydantic import BaseModel, Field, field_validator

from ..utils import remove_html_tags, replace_placeholders

__all__ = (
    "CardTag",
    "DiceCost",
    "CardDictionary",
    "CardTalent",
    "TCGCardDetail",
    "TCGCard",
)


class CardTag(BaseModel):
    id: str
    name: str


class DiceCost(BaseModel):
    type: str
    amount: int = Field(alias="count")


class CardDictionary(BaseModel):
    id: str
    name: str
    params: dict[str, Any] | None = None
    description: str
    cost: list[DiceCost] = Field(None, alias="diceCost")

    @field_validator("name", mode="before")
    def _format_name(cls, v: str) -> str:
        return remove_html_tags(v)

    @field_validator("cost", mode="before")
    def _convert_cost(cls, v: dict[str, int] | None) -> list[DiceCost]:
        return [DiceCost(type=type_, count=count) for type_, count in v.items()] if v else []

    @field_validator("description", mode="before")
    def _format_description(cls, v: str, values: Any) -> str:
        params = values.data.get("params")
        if params:
            v = replace_placeholders(v, params)
        return remove_html_tags(v)


class CardTalent(BaseModel):
    id: str
    name: str
    params: dict[str, Any] | None
    description: str
    cost: list[DiceCost]
    tags: list[CardTag]
    icon: str
    sub_skills: dict[str, Any] | None = Field(None, alias="subSkills")

    @field_validator("description", mode="before")
    def _format_description(cls, v: str, values: Any) -> str:
        params = values.data.get("params")
        if params:
            v = replace_placeholders(v, params)
        return remove_html_tags(v)

    @field_validator("cost", mode="before")
    def _convert_cost(cls, v: dict[str, int] | None) -> list[DiceCost]:
        return [DiceCost(type=type_, count=count) for type_, count in v.items()] if v else []

    @field_validator("tags", mode="before")
    def _convert_tags(cls, v: dict[str, str] | None) -> list[CardTag]:
        return [CardTag(id=id_, name=name) for id_, name in v.items()] if v else []

    @field_validator("icon", mode="before")
    def _convert_icon_url(cls, v: str) -> str:
        return f"https://api.ambr.top/assets/UI/{v}.png"

    @property
    def small_icon(self) -> str:
        return self.icon.replace(".png", ".sm.png")


class TCGCardDetail(BaseModel):
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
    def _convert_tags(cls, v: dict[str, str] | None) -> list[CardTag]:
        return [CardTag(id=id_, name=name) for id_, name in v.items()] if v else []

    @field_validator("icon", mode="before")
    def _convert_icon_url(cls, v: str) -> str:
        return f"https://api.ambr.top/assets/UI/gcg/{v}.png"

    @property
    def small_icon(self) -> str:
        return self.icon.replace(".png", ".sm.png")

    @field_validator("dictionaries", mode="before")
    def _convert_dictionaries(cls, v: dict[str, dict[str, Any]] | None) -> list[CardDictionary]:
        return [CardDictionary(id=item_id, **v[item_id]) for item_id in v] if v else []

    @field_validator("talents", mode="before")
    def _convert_talents(cls, v: dict[str, dict[str, Any]]) -> list[CardTalent]:
        return [CardTalent(id=item_id, **v[item_id]) for item_id in v]


class TCGCard(BaseModel):
    """
    Represents a TCG card.

    Attributes
    ----------
    id: :class:`int`
        The card's ID.
    name: :class:`str`
        The card's name.
    type: :class:`str`
        The card's type.
    tags: Dict[:class:`str`, :class:`str`]
        The card's tags.
    dice_cost: Dict[:class:`str`, :class:`int`]
        The card's properties.
    icon: :class:`str`
        The card's icon.
    route: :class:`str`
        The card's route.
    sort_order: :class:`int`
        The card's sort order.
    """

    id: int
    name: str
    type: str
    tags: list[CardTag]
    dice_cost: list[DiceCost] = Field(None, alias="props")
    icon: str
    route: str
    sort_order: int = Field(alias="sortOrder")

    @field_validator("tags", mode="before")
    def _convert_tags(cls, v: dict[str, str] | None) -> list[CardTag]:
        return [CardTag(id=id_, name=name) for id_, name in v.items()] if v else []

    @field_validator("dice_cost", mode="before")
    def _convert_dice_cost(cls, v: dict[str, int] | None) -> list[DiceCost]:
        return [DiceCost(type=type_, count=count) for type_, count in v.items()] if v else []

    @field_validator("icon", mode="before")
    def _convert_icon_url(cls, v: str) -> str:
        return f"https://api.ambr.top/assets/UI/gcg/{v}.png"

    @property
    def small_icon(self) -> str:
        return self.icon.replace(".png", ".sm.png")
