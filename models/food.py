from pydantic import BaseModel, Field, validator


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
    effect_icon: str = Field(alias="effectIcon")

    @validator("icon", pre=True)
    def _add_icon_url(cls, v: str) -> str:
        return f"https://api.ambr.top/assets/UI/{v}.png"

    @validator("effect_icon", pre=True)
    def _add_effect_icon_url(cls, v: str) -> str:
        return f"https://api.ambr.top/assets/UI/{v}.png"
