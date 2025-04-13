from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field, field_validator

from ..constants import WEEKDAYS
from ..utils import remove_html_tags

__all__ = ("Material", "MaterialDetail", "MaterialRecipe", "MaterialSource")


class MaterialRecipe(BaseModel):
    """Represents an item used as input in a material crafting recipe.

    Attributes:
        icon: The icon URL of the input item.
        amount: The quantity of the input item required.
    """

    icon: str
    amount: int = Field(alias="count")

    @field_validator("icon", mode="before")
    @classmethod
    def _convert_icon_url(cls, v: str) -> str:
        return f"https://gi.yatta.moe/assets/UI/{v}.png"


class MaterialSource(BaseModel):
    """Represents a source where a material can be obtained.

    Attributes:
        name: The name of the source (e.g., "Cecilia Garden", "Dropped by Cryo Slimes").
        type: The type of source (e.g., "Domain", "Monster").
        days: A list of integers representing the days of the week the source is available (optional, 1=Monday, 7=Sunday).
    """

    name: str
    type: str
    days: list[int] | None = Field(None)

    @field_validator("days", mode="before")
    @classmethod
    def _convert_days(cls, v: list[str]) -> list[int]:
        return [WEEKDAYS[day] for day in v]


class MaterialDetail(BaseModel):
    """Represents detailed information about a material.

    Attributes:
        name: The name of the material.
        description: The description of the material.
        type: The type or category of the material.
        recipe: A list of input items required if this material can be crafted.
        sources: A list of sources where this material can be obtained.
        icon: The icon URL for the material.
        rarity: The rarity rank of the material.
        route: The route identifier for the material.
    """

    name: str
    description: str
    type: str
    recipe: list[MaterialRecipe]
    sources: list[MaterialSource] = Field(alias="source")
    icon: str
    rarity: int = Field(alias="rank")
    route: str

    @field_validator("description", mode="before")
    @classmethod
    def _format_description(cls, v: str) -> str:
        return remove_html_tags(v)

    @field_validator("recipe", mode="before")
    @classmethod
    def _convert_recipe(
        cls, v: bool | dict[str, dict[str, dict[str, Any]]]
    ) -> list[MaterialRecipe]:
        if isinstance(v, dict):
            recipe = next(iter(v.values()))
            return [MaterialRecipe(**item) for item in recipe.values()]
        return []

    @field_validator("sources", mode="before")
    @classmethod
    def _convert_sources(cls, v: list[dict] | None) -> list[MaterialSource]:
        return [MaterialSource(**item) for item in v] if v else []

    @field_validator("icon", mode="before")
    @classmethod
    def _convert_icon_url(cls, v: str) -> str:
        return f"https://gi.yatta.moe/assets/UI/{v}.png"


class Material(BaseModel):
    """Represents a material summary.

    Attributes:
        id: The unique ID of the material.
        name: The name of the material.
        type: The type or category of the material.
        recipe: Whether the material can be crafted.
        icon: The icon URL for the material.
        rarity: The rarity rank of the material.
        route: The route identifier for the material.
    """

    id: int
    name: str
    type: str
    recipe: bool
    icon: str
    rarity: int = Field(alias="rank")
    route: str

    @field_validator("recipe", mode="before")
    @classmethod
    def _convert_recipe(cls, v: bool | None) -> bool:
        return bool(v)

    @field_validator("icon", mode="before")
    @classmethod
    def _convert_icon_url(cls, v: str) -> str:
        return f"https://gi.yatta.moe/assets/UI/{v}.png"
