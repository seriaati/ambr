from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field, field_validator

from ..utils import remove_html_tags

__all__ = ("Food", "FoodDetail", "FoodEffect", "FoodRecipe", "FoodSource")


class FoodSource(BaseModel):
    """Represents a source where food can be obtained.

    Attributes:
        name: The name of the source (e.g., an NPC or location).
        type: The type of source (e.g., "Shop", "Quest").
    """

    name: str
    type: str


class FoodEffect(BaseModel):
    """Represents the effect of a food item.

    Attributes:
        id: The identifier for the effect.
        description: The description of the effect.
    """

    id: str
    description: str

    @field_validator("description", mode="before")
    @classmethod
    def _format_description(cls, v: str) -> str:
        return remove_html_tags(v)


class FoodRecipe(BaseModel):
    """Represents the recipe details for a food item.

    Attributes:
        effect_icon: The URL of the icon representing the food's effect category.
        effects: A list of specific effects provided by the food.
    """

    effect_icon: str = Field(alias="effectIcon")
    effects: list[FoodEffect] = Field(alias="effect")

    @field_validator("effect_icon", mode="before")
    @classmethod
    def _convert_effect_icon_url(cls, v: str) -> str:
        return f"https://gi.yatta.moe/assets/UI/{v}.png"

    @field_validator("effects", mode="before")
    @classmethod
    def _convert_effects(cls, v: dict[str, str]) -> list[FoodEffect]:
        return [FoodEffect(id=item_id, description=v[item_id]) for item_id in v]


class FoodDetail(BaseModel):
    """Represents detailed information about a food item.

    Attributes:
        name: The name of the food.
        description: The description of the food.
        type: The type or category of the food.
        recipe: Details about the recipe if the food can be cooked, otherwise False.
        sources: A list of sources where the food can be obtained.
        icon: The URL of the food's icon.
        rarity: The rarity or rank of the food.
        route: The internal route or identifier for the food.
    """

    name: str
    description: str
    type: str
    recipe: FoodRecipe | bool
    sources: list[FoodSource] = Field(alias="source")
    icon: str
    rarity: int = Field(alias="rank")
    route: str

    @field_validator("recipe", mode="before")
    @classmethod
    def _convert_recipe(cls, v: bool | dict[str, Any]) -> FoodRecipe | bool:
        if isinstance(v, dict):
            return FoodRecipe(**v)
        return False

    @field_validator("icon", mode="before")
    @classmethod
    def _convert_icon_url(cls, v: str) -> str:
        return f"https://gi.yatta.moe/assets/UI/{v}.png"


class Food(BaseModel):
    """Represents a food item (summary view).

    Attributes:
        id: The unique identifier for the food.
        name: The name of the food.
        type: The type or category of the food.
        recipe: Indicates if the food is obtained via a recipe.
        icon: The URL of the food's icon.
        rarity: The rarity or rank of the food.
        route: The internal route or identifier for the food.
        effect_icon: The URL of the icon representing the food's effect category, if applicable.
    """

    id: int
    name: str
    type: str
    recipe: bool
    icon: str
    rarity: int = Field(alias="rank")
    route: str
    effect_icon: str | None = Field(None, alias="effectIcon")

    @field_validator("recipe", mode="before")
    @classmethod
    def _convert_recipe(cls, v: bool | None) -> bool:
        return bool(v)

    @field_validator("icon", mode="before")
    @classmethod
    def _convert_icon_url(cls, v: str) -> str:
        return f"https://gi.yatta.moe/assets/UI/{v}.png"

    @field_validator("effect_icon", mode="before")
    @classmethod
    def _convert_effect_icon_url(cls, v: str | None) -> str | None:
        return f"https://gi.yatta.moe/assets/UI/{v}.png" if v else None
