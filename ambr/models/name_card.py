from __future__ import annotations

from pydantic import Field, field_validator

from ._base import BaseModel

__all__ = ("Namecard", "NamecardDetail")


class NamecardDetail(BaseModel):
    """Represents detailed information about a namecard.

    Attributes:
        id: The namecard's unique ID.
        name: The namecard's name.
        rarity: The rarity rank of the namecard.
        icon: The icon URL for the namecard.
        route: The route identifier for the namecard.
        description: The general description of the namecard.
        description_special: A special or alternative description (optional).
        source: How the namecard is obtained (optional).
    """

    id: int
    name: str
    rarity: int = Field(alias="rank")
    icon: str
    route: str
    description: str
    description_special: str = Field(alias="descriptionSpecial")
    source: str | None

    @field_validator("icon", mode="before")
    @classmethod
    def _convert_icon_url(cls, v: str) -> str:
        return f"https://gi.yatta.moe/assets/UI/namecard/{v}.png"

    @property
    def picture(self) -> str:
        """Returns the URL for the full picture version of the namecard."""
        return f"{self.icon.replace('NameCardIcon', 'NameCardPic')[:-4]}_P.png"


class Namecard(BaseModel):
    """Represents a namecard summary.

    Attributes:
        id: The namecard's unique ID.
        name: The namecard's name.
        type: The type or category of the namecard.
        rarity: The rarity rank of the namecard.
        icon: The icon URL for the namecard.
        route: The route identifier for the namecard.
    """

    id: int
    name: str
    type: str
    rarity: int = Field(alias="rank")
    icon: str
    route: str

    @field_validator("icon", mode="before")
    @classmethod
    def _convert_icon_url(cls, v: str) -> str:
        return f"https://gi.yatta.moe/assets/UI/namecard/{v}.png"

    @property
    def picture(self) -> str:
        """Returns the URL for the full picture version of the namecard."""
        return f"{self.icon.replace('NameCardIcon', 'NameCardPic')[:-4]}_P.png"
