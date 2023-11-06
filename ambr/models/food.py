from typing import Any, Dict, List, Optional, Union

from pydantic import BaseModel, Field, field_validator

__all__ = (
    "FoodSource",
    "FoodEffect",
    "FoodRecipe",
    "FoodDetail",
    "Food",
)


class FoodSource(BaseModel):
    name: str
    type: str


class FoodEffect(BaseModel):
    id: str
    description: str


class FoodRecipe(BaseModel):
    effect_icon: str = Field(alias="effectIcon")
    effects: List[FoodEffect] = Field(alias="effect")

    @field_validator("effect_icon", mode="before")
    def _convert_effect_icon_url(cls, v: str) -> str:
        return f"https://api.ambr.top/assets/UI/{v}.png"

    @field_validator("effects", mode="before")
    def _convert_effects(cls, v: Dict[str, str]) -> List[FoodEffect]:
        return [FoodEffect(id=item_id, description=v[item_id]) for item_id in v]


class FoodDetail(BaseModel):
    name: str
    description: str
    type: str
    recipe: Union[FoodRecipe, bool]
    map_mark: bool = Field(alias="mapMark")
    sources: List[FoodSource] = Field(alias="source")
    icon: str
    rarity: int = Field(alias="rank")
    route: str

    @field_validator("recipe", mode="before")
    def _convert_recipe(cls, v: Union[bool, Dict[str, Any]]) -> Union[FoodRecipe, bool]:
        if isinstance(v, dict):
            return FoodRecipe(**v)
        return False

    @field_validator("sources", mode="before")
    def _convert_sources(cls, v: List[Dict[str, str]]) -> List[FoodSource]:
        return [FoodSource(**item) for item in v]

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
    effect_icon: Optional[str] = Field(None, alias="effectIcon")

    @field_validator("icon", mode="before")
    def _convert_icon_url(cls, v: str) -> str:
        return f"https://api.ambr.top/assets/UI/{v}.png"

    @field_validator("effect_icon", mode="before")
    def _convert_effect_icon_url(cls, v: Optional[str]) -> Optional[str]:
        return f"https://api.ambr.top/assets/UI/{v}.png" if v else None
