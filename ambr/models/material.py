from typing import Any

from pydantic import BaseModel, Field, field_validator

from ..constants import WEEKDAYS
from ..utils import remove_html_tags

__all__ = (
    "Material",
    "MaterialDetail",
    "MaterialRecipe",
    "MaterialSource",
)


class MaterialRecipe(BaseModel):
    icon: str
    amount: int = Field(alias="count")

    @field_validator("icon", mode="before")
    def _convert_icon_url(cls, v: str) -> str:
        return f"https://gi.yatta.moe/assets/UI/{v}.png"


class MaterialSource(BaseModel):
    name: str
    type: str
    days: list[int] | None = Field(None)

    @field_validator("days", mode="before")
    def _convert_days(cls, v: list[str]) -> list[int]:
        return [WEEKDAYS[day] for day in v]


class MaterialDetail(BaseModel):
    name: str
    description: str
    type: str
    recipe: list[MaterialRecipe]
    sources: list[MaterialSource] = Field(alias="source")
    icon: str
    rarity: int = Field(alias="rank")
    route: str

    @field_validator("description", mode="before")
    def _format_description(cls, v: str) -> str:
        return remove_html_tags(v)

    @field_validator("recipe", mode="before")
    def _convert_recipe(
        cls, v: bool | dict[str, dict[str, dict[str, Any]]]
    ) -> list[MaterialRecipe]:
        if isinstance(v, dict):
            recipe = next(iter(v.values()))
            return [MaterialRecipe(**item) for item in recipe.values()]
        return []

    @field_validator("sources", mode="before")
    def _convert_sources(cls, v: list[dict] | None) -> list[MaterialSource]:
        return [MaterialSource(**item) for item in v] if v else []

    @field_validator("icon", mode="before")
    def _convert_icon_url(cls, v: str) -> str:
        return f"https://gi.yatta.moe/assets/UI/{v}.png"


class Material(BaseModel):
    """
    Represents a material.

    Attributes
    ----------
    id: :class:`int`
        The material's ID.
    name: :class:`str`
        The material's name.
    type: :class:`str`
        The material's type.
    recipe: :class:`bool`
        Whether the material is a recipe.
    icon: :class:`str`
        The material's icon.
    rarity: :class:`int`
        The material's rarity.
    route: :class:`str`
        The material's route.
    """

    id: int
    name: str
    type: str
    recipe: bool
    icon: str
    rarity: int = Field(alias="rank")
    route: str

    @field_validator("recipe", mode="before")
    def _convert_recipe(cls, v: bool | None) -> bool:
        return bool(v)

    @field_validator("icon", mode="before")
    def _convert_icon_url(cls, v: str) -> str:
        return f"https://gi.yatta.moe/assets/UI/{v}.png"
