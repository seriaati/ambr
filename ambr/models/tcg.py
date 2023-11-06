from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field, field_validator

from ..utils import remove_html_tags, replace_placeholders


class CardTag(BaseModel):
    id: str
    name: str


class DiceCost(BaseModel):
    type: str
    amount: int = Field(alias="count")


class CardProperty(BaseModel):
    id: str
    value: int


class CardDictionary(BaseModel):
    name: str
    description: str


class CardTalent(BaseModel):
    name: str
    params: Optional[Dict[str, Any]]
    description: str
    cost: List[DiceCost]
    tags: List[CardTag]
    icon: str

    @field_validator("description", mode="before")  # type:ignore
    def _format_description(cls, v: str, values: Dict[str, Any]) -> str:
        params = values.get("params")
        if params:
            v = replace_placeholders(v, params)
        return remove_html_tags(v)

    @field_validator("cost", mode="before")
    def _convert_cost(cls, v: Optional[Dict[str, int]]) -> List[DiceCost]:
        return (
            [DiceCost(type=type_, count=count) for type_, count in v.items()]
            if v
            else []
        )

    @field_validator("tags", mode="before")
    def _convert_tags(cls, v: Optional[Dict[str, str]]) -> List[CardTag]:
        return [CardTag(id=id_, name=name) for id_, name in v.items()] if v else []

    @field_validator("icon", mode="before")
    def _convert_icon_url(cls, v: str) -> str:
        return f"https://api.ambr.top/assets/UI/{v}.png"


class TCGCardDetail(BaseModel):
    id: int
    name: str
    type: str
    tags: List[CardTag]
    props: List[CardProperty]
    icon: str
    route: str
    story_title: str = Field(alias="storyTitle")
    story_detail: str = Field(alias="storyDetail")
    source: str
    dictionaries: List[CardDictionary] = Field(alias="dictionary")
    talents: List[CardTalent] = Field(alias="talent")

    @field_validator("tags", mode="before")
    def _convert_tags(cls, v: Optional[Dict[str, str]]) -> List[CardTag]:
        return [CardTag(id=id_, name=name) for id_, name in v.items()] if v else []

    @field_validator("props", mode="before")
    def _convert_props(cls, v: Optional[Dict[str, int]]) -> List[CardProperty]:
        return (
            [CardProperty(id=id_, value=value) for id_, value in v.items()] if v else []
        )

    @field_validator("icon", mode="before")
    def _convert_icon_url(cls, v: str) -> str:
        return f"https://api.ambr.top/assets/UI/{v}.png"

    @field_validator("dictionaries", mode="before")
    def _convert_dictionaries(
        cls, v: Optional[Dict[str, Dict[str, Any]]]
    ) -> List[CardDictionary]:
        return [CardDictionary(**v[item_id]) for item_id in v] if v else []

    @field_validator("talents", mode="before")
    def _convert_talents(cls, v: Dict[str, Dict[str, Any]]) -> List[CardTalent]:
        return [CardTalent(**v[item_id]) for item_id in v]


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
    tags: List[CardTag]
    dice_cost: List[DiceCost] = Field(None, alias="props")
    icon: str
    route: str
    sort_order: int = Field(alias="sortOrder")

    @field_validator("tags", mode="before")
    def _convert_tags(cls, v: Optional[Dict[str, str]]) -> List[CardTag]:
        return [CardTag(id=id_, name=name) for id_, name in v.items()] if v else []

    @field_validator("dice_cost", mode="before")
    def _convert_dice_cost(cls, v: Optional[Dict[str, int]]) -> List[DiceCost]:
        return (
            [DiceCost(type=type_, count=count) for type_, count in v.items()]
            if v
            else []
        )

    @field_validator("icon", mode="before")
    def _convert_icon_url(cls, v: str) -> str:
        return f"https://api.ambr.top/assets/UI/{v}.png"
