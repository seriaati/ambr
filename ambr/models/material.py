from typing import Any, Dict, List, Literal, Optional, Union

from pydantic import BaseModel, Field, field_validator

WEEKDAYS = {
    "monday": 1,
    "tuesday": 2,
    "wednesday": 3,
    "thursday": 4,
    "friday": 5,
    "saturday": 6,
    "sunday": 0,
}


class MaterialRecipe(BaseModel):
    icon: str
    amount: int = Field(alias="count")

    @field_validator("icon", mode="before")
    def _convert_icon_url(cls, v: str) -> str:
        return f"https://api.ambr.top/assets/UI/{v}.png"


class MaterialSource(BaseModel):
    name: str
    type: str
    days: Optional[List[int]] = Field(None)

    @field_validator("days", mode="before")
    def _convert_days(cls, v: List[str]) -> List[int]:
        return [WEEKDAYS[day] for day in v]


class MaterialDetail(BaseModel):
    name: str
    description: str
    type: str
    recipe: List[MaterialRecipe]
    map_mark: bool = Field(alias="mapMark")
    sources: List[MaterialSource] = Field(alias="source")
    icon: str
    rarity: int = Field(alias="rank")
    route: str

    @field_validator("recipe", mode="before")
    def _convert_recipe(
        cls, v: Union[bool, Dict[str, Dict[str, Dict[str, Any]]]]
    ) -> List[MaterialRecipe]:
        if isinstance(v, dict):
            recipe = list(v.values())[0]
            return [MaterialRecipe(**item) for item in recipe.values()]
        return []

    @field_validator("sources", mode="before")
    def _convert_sources(cls, v: Optional[List[dict]]) -> List[MaterialSource]:
        return [MaterialSource(**item) for item in v] if v else []

    @field_validator("icon", mode="before")
    def _convert_icon_url(cls, v: str) -> str:
        return f"https://api.ambr.top/assets/UI/{v}.png"


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
    map_mark: :class:`bool`
        Whether the material has a map mark.
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
    map_mark: bool = Field(alias="mapMark")
    icon: str
    rarity: int = Field(alias="rank")
    route: str

    @field_validator("icon", mode="before")
    def _convert_icon_url(cls, v: str) -> str:
        return f"https://api.ambr.top/assets/UI/{v}.png"
