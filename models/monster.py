from pydantic import BaseModel, validator


class Monster(BaseModel):
    """
    Represents a living being.

    Attributes
    ----------
    id: :class:`int`
        The living being's ID.
    name: :class:`str`
        The living being's name.
    type: :class:`str`
        The living being's type.
    icon: :class:`str`
        The living being's icon.
    route: :class:`str`
        The living being's route.
    """

    id: int
    name: str
    type: str
    icon: str
    route: str

    @validator("icon", pre=True)
    def _add_icon_url(cls, v: str) -> str:
        return f"https://api.ambr.top/assets/UI/{v}.png"
