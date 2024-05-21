from typing import Any

from pydantic import BaseModel, Field, field_validator

from ..utils import remove_html_tags

__all__ = (
    "Food",
    "FoodDetail",
    "FoodEffect",
    "FoodRecipe",
    "FoodSource",
)


class FoodSource(BaseModel):
    name: str
    type: str


class FoodEffect(BaseModel):
    id: str
    description: str

    @field_validator("description", mode="before")
    def _format_description(cls, v: str) -> str:
        return remove_html_tags(v)


class FoodRecipe(BaseModel):
    effect_icon: str = Field(alias="effectIcon")
    effects: list[FoodEffect] = Field(alias="effect")

    @field_validator("effect_icon", mode="before")
    def _convert_effect_icon_url(cls, v: str) -> str:
        return f"https://api.ambr.top/assets/UI/{v}.png"

    @field_validator("effects", mode="before")
    def _convert_effects(cls, v: dict[str, str]) -> list[FoodEffect]:
        return [FoodEffect(id=item_id, description=v[item_id]) for item_id in v]


class FoodDetail(BaseModel):
    name: str
    description: str
    type: str
    recipe: FoodRecipe | bool
    map_mark: bool = Field(alias="mapMark")
    sources: list[FoodSource] = Field(alias="source")
    icon: str
    rarity: int = Field(alias="rank")
    route: str

    @field_validator("recipe", mode="before")
    def _convert_recipe(cls, v: bool | dict[str, Any]) -> FoodRecipe | bool:
        if isinstance(v, dict):
            return FoodRecipe(**v)
        return False

    @field_validator("icon", mode="before")
    def _convert_icon_url(cls, v: str) -> str:
        return f"https://api.ambr.top/assets/UI/{v}.png"


class Food(BaseModel):
    """
    Represents a food.

    Attributes
    ----------
    id: :class:`int`
        The food's ID.
    name: :class:`str`
        The food's name.
    type: :class:`str`
        The food's type.
    recipe: :class:`bool`
        Whether the food is a recipe.
    map_mark: :class:`bool`
        Whether the food has a map mark.
    icon: :class:`str`
        The food's icon.
    rarity: :class:`int`
        The food's rarity.
    route: :class:`str`
        The food's route.
    effect_icon: :class:`str`
        The food's effect icon.
    """

    id: int
    name: str
    type: str
    recipe: bool
    map_mark: bool = Field(alias="mapMark")
    icon: str
    rarity: int = Field(alias="rank")
    route: str
    effect_icon: str | None = Field(None, alias="effectIcon")

    @field_validator("recipe", mode="before")
    def _convert_recipe(cls, v: bool | None) -> bool:
        return bool(v)

    @field_validator("icon", mode="before")
    def _convert_icon_url(cls, v: str) -> str:
        return f"https://api.ambr.top/assets/UI/{v}.png"

    @field_validator("effect_icon", mode="before")
    def _convert_effect_icon_url(cls, v: str | None) -> str | None:
        return f"https://api.ambr.top/assets/UI/{v}.png" if v else None
