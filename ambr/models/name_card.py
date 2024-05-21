from pydantic import BaseModel, Field, field_validator

from ..utils import remove_html_tags

__all__ = (
    "Namecard",
    "NamecardDetail",
)


class NamecardDetail(BaseModel):
    id: int
    name: str
    rarity: int = Field(alias="rank")
    icon: str
    route: str
    description: str
    description_special: str = Field(alias="descriptionSpecial")
    source: str | None

    @field_validator("description", mode="before")
    def _format_description(cls, v: str) -> str:
        return remove_html_tags(v)

    @field_validator("icon", mode="before")
    def _convert_icon_url(cls, v: str) -> str:
        return f"https://api.ambr.top/assets/UI/namecard/{v}.png"

    @property
    def picture(self) -> str:
        return f"{self.icon.replace('NameCardIcon', 'NameCardPic')[:-4]}_P.png"


class Namecard(BaseModel):
    """
    Represents a namecard.

    Attributes
    ----------
    id: :class:`int`
        The name card's ID.
    name: :class:`str`
        The name card's name.
    type: :class:`str`
        The name card's type.
    rarity: :class:`int`
        The name card's rarity.
    icon: :class:`str`
        The name card's icon.
    route: :class:`str`
        The name card's route.
    """

    id: int
    name: str
    type: str
    rarity: int = Field(alias="rank")
    icon: str
    route: str

    @field_validator("icon", mode="before")
    def _convert_icon_url(cls, v: str) -> str:
        return f"https://api.ambr.top/assets/UI/namecard/{v}.png"

    @property
    def picture(self) -> str:
        return f"{self.icon.replace('NameCardIcon', 'NameCardPic')[:-4]}_P.png"
