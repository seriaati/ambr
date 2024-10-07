from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field, field_validator

from ..utils import remove_html_tags

__all__ = (
    "Furniture",
    "FurnitureDetail",
    "FurnitureItem",
    "FurnitureRecipe",
    "FurnitureRecipeInput",
    "FurnitureSet",
    "FurnitureSetDetail",
)


class FurnitureRecipeInput(BaseModel):
    id: int
    icon: str
    amount: int = Field(alias="count")

    @field_validator("icon", mode="before")
    def _convert_icon_url(cls, v: str) -> str:
        return f"https://gi.yatta.moe/assets/UI/{v}.png"


class FurnitureRecipe(BaseModel):
    exp: int
    time: int
    inputs: list[FurnitureRecipeInput] = Field(alias="input")

    @field_validator("inputs", mode="before")
    def _convert_inputs(cls, v: dict[str, dict[str, Any]]) -> list[FurnitureRecipeInput]:
        return [FurnitureRecipeInput(id=int(item_id), **v[item_id]) for item_id in v]


class FurnitureDetail(BaseModel):
    id: int
    name: str
    cost: int | None
    comfort: int | None
    rarity: int = Field(alias="rank")
    icon: str
    route: str
    categories: list[str]
    types: list[str]
    description: str
    recipe: FurnitureRecipe | None

    @field_validator("icon", mode="before")
    def _convert_icon_url(cls, v: str) -> str:
        return f"https://gi.yatta.moe/assets/UI/furniture/{v}.png"

    @field_validator("recipe", mode="before")
    def _convert_recipe(cls, v: dict[str, Any] | None) -> FurnitureRecipe | None:
        if v is None:
            return None
        return FurnitureRecipe(**v)


class Furniture(BaseModel):
    """
    Represents a furniture.

    Attributes
    ----------
    id: :class:`int`
        The furniture's ID.
    name: :class:`str`
        The furniture's name.
    cost: Optional[:class:`int`]
        The furniture's cost.
    comfort: Optional[:class:`int`]
        The furniture's comfort.
    rarity: :class:`int`
        The furniture's rarity.
    icon: :class:`str`
        The furniture's icon.
    route: :class:`str`
        The furniture's route.
    categories: List[:class:`str`]
        The furniture's categories.
    types: List[:class:`str`]
        The furniture's types.
    """

    id: int
    name: str
    cost: int | None
    comfort: int | None
    rarity: int = Field(alias="rank")
    icon: str
    route: str
    categories: list[str]
    types: list[str]

    @field_validator("icon", mode="before")
    def _convert_icon_url(cls, v: str) -> str:
        return f"https://gi.yatta.moe/assets/UI/furniture/{v}.png"


class FurnitureSet(BaseModel):
    id: int
    name: str
    icon: str
    route: str
    categories: list[str]
    types: list[str]

    @field_validator("icon", mode="before")
    def _convert_icon_url(cls, v: str) -> str:
        return f"https://gi.yatta.moe/assets/UI/furnitureSuite/{v}.png"

    @field_validator("categories", mode="before")
    def _convert_categories(cls, v: list[str] | None) -> list[str]:
        return v or []

    @field_validator("types", mode="before")
    def _convert_types(cls, v: list[str] | None) -> list[str]:
        return v or []


class FurnitureItem(BaseModel):
    id: int
    rarity: int = Field(alias="rank")
    icon: str

    @field_validator("icon", mode="before")
    def _convert_icon_url(cls, v: str) -> str:
        return f"https://gi.yatta.moe/assets/UI/furniture/{v}.png"


class FurnitureSetFavoriteNPC(BaseModel):
    id: str
    icon: str


class FurnitureSetDetail(BaseModel):
    id: int
    name: str
    icon: str
    route: str
    categories: list[str]
    types: list[str]
    description: str
    furniture_items: list[FurnitureItem] = Field(alias="suiteItemList")
    favorite_npcs: list[FurnitureSetFavoriteNPC] = Field(alias="favoriteNpcList")

    @field_validator("icon", mode="before")
    def _convert_icon_url(cls, v: str) -> str:
        return f"https://gi.yatta.moe/assets/UI/furnitureSuite/{v}.png"

    @field_validator("categories", mode="before")
    def _convert_categories(cls, v: list[str] | None) -> list[str]:
        return v or []

    @field_validator("types", mode="before")
    def _convert_types(cls, v: list[str] | None) -> list[str]:
        return v or []

    @field_validator("description", mode="before")
    def _format_description(cls, v: str) -> str:
        return remove_html_tags(v)

    @field_validator("furniture_items", mode="before")
    def _convert_furniture_items(cls, v: dict[str, dict[str, Any]]) -> list[FurnitureItem]:
        return [FurnitureItem(id=int(item_id), **v[item_id]) for item_id in v]

    @field_validator("favorite_npcs", mode="before")
    def _convert_favored_ids(
        cls, v: dict[str, dict[str, Any]] | None
    ) -> list[FurnitureSetFavoriteNPC]:
        return (
            [FurnitureSetFavoriteNPC(id=id_, icon=data["icon"]) for id_, data in v.items()]
            if v is not None
            else []
        )
