from pydantic import BaseModel, Field, validator


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

    @validator("icon", pre=True)
    def _add_icon_url(cls, v: str) -> str:
        return f"https://api.ambr.top/assets/UI/{v}.png"
