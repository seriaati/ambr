from pydantic import BaseModel, Field, validator


class Weapon(BaseModel):
    """
    Represents a weapon.

    Attributes
    ----------
    id: :class:`int`
        The weapon's ID.
    rarity: :class:`int`
        The weapon's rarity.
    type: :class:`str`
        The weapon's type.
    name: :class:`str`
        The weapon's name.
    icon: :class:`str`
        The weapon's icon.
    route: :class:`str`
        The weapon's route.
    """

    id: int
    rarity: int = Field(alias="rank")
    type: str
    name: str
    icon: str
    route: str

    @validator("icon", pre=True)
    def _add_icon_url(cls, v: str) -> str:
        return f"https://api.ambr.top/assets/UI/{v}.png"
