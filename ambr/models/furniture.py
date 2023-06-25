from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field, validator


class FurnitureRecipeInput(BaseModel):
    id: int
    icon: str
    amount: int = Field(alias="count")


class FurnitureRecipe(BaseModel):
    exp: int
    time: int
    inputs: List[FurnitureRecipeInput] = Field(alias="input")

    @validator("inputs", pre=True)
    def _convert_inputs(
        cls, v: Dict[str, Dict[str, Any]]
    ) -> List[FurnitureRecipeInput]:
        return [FurnitureRecipeInput(id=int(item_id), **v[item_id]) for item_id in v]


class FurnitureDetail(BaseModel):
    id: int
    name: str
    cost: Optional[int]
    comfort: Optional[int]
    rarity: int = Field(alias="rank")
    icon: str
    route: str
    categories: List[str]
    types: List[str]
    description: str
    recipe: Optional[FurnitureRecipe]

    @validator("icon", pre=True)
    def _convert_icon_url(cls, v: str) -> str:
        return f"https://api.ambr.top/assets/UI/{v}.png"

    @validator("recipe", pre=True)
    def _convert_recipe(cls, v: Optional[Dict[str, Any]]) -> Optional[FurnitureRecipe]:
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
    cost: Optional[int]
    comfort: Optional[int]
    rarity: int = Field(alias="rank")
    icon: str
    route: str
    categories: List[str]
    types: List[str]

    @validator("icon", pre=True)
    def _convert_icon_url(cls, v: str) -> str:
        return f"https://api.ambr.top/assets/UI/{v}.png"


class FurnitureSet(BaseModel):
    id: int
    name: str
    icon: str
    route: str
    categories: List[str]
    types: List[str]

    @validator("icon", pre=True)
    def _convert_icon_url(cls, v: str) -> str:
        return f"https://api.ambr.top/assets/UI/{v}.png"
