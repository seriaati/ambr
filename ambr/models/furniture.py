from __future__ import annotations

from typing import Any

from pydantic import Field, field_validator

from ._base import BaseModel

__all__ = (
    "Furniture",
    "FurnitureDetail",
    "FurnitureItem",
    "FurnitureRecipe",
    "FurnitureRecipeInput",
    "FurnitureSet",
    "FurnitureSetDetail",
    "FurnitureSetFavoriteNPC",
)


class FurnitureRecipeInput(BaseModel):
    """Represents an input material required for a furniture recipe.

    Attributes:
        id: The ID of the input material.
        icon: The icon URL of the input material.
        amount: The quantity of the material required.
    """

    id: int
    icon: str
    amount: int = Field(alias="count")

    @field_validator("icon", mode="before")
    @classmethod
    def _convert_icon_url(cls, v: str) -> str:
        return f"https://gi.yatta.moe/assets/UI/{v}.png"


class FurnitureRecipe(BaseModel):
    """Represents the crafting recipe for a piece of furniture.

    Attributes:
        exp: The amount of Adeptal Energy experience gained upon crafting.
        time: The time required to craft the furniture (in some unit, likely hours or seconds).
        inputs: A list of materials required to craft the furniture.
    """

    exp: int
    time: int
    inputs: list[FurnitureRecipeInput] = Field(alias="input")

    @field_validator("inputs", mode="before")
    @classmethod
    def _convert_inputs(cls, v: dict[str, dict[str, Any]]) -> list[FurnitureRecipeInput]:
        return [FurnitureRecipeInput(id=int(item_id), **v[item_id]) for item_id in v]


class FurnitureDetail(BaseModel):
    """Represents detailed information about a piece of furniture.

    Attributes:
        id: The unique ID of the furniture.
        name: The name of the furniture.
        cost: The load cost of the furniture (optional).
        comfort: The comfort value (Adeptal Energy) provided by the furniture (optional).
        rarity: The rarity rank of the furniture.
        icon: The icon URL for the furniture.
        route: The route identifier for the furniture.
        categories: A list of categories the furniture belongs to.
        types: A list of types the furniture belongs to.
        description: The description of the furniture.
        recipe: The crafting recipe for the furniture (optional).
    """

    id: int
    name: str
    cost: int | None
    comfort: int | None
    rarity: int = Field(alias="rank")
    icon: str
    route: str
    categories: list[str]
    types: list[str]
    description: str
    recipe: FurnitureRecipe | None

    @field_validator("icon", mode="before")
    @classmethod
    def _convert_icon_url(cls, v: str) -> str:
        return f"https://gi.yatta.moe/assets/UI/furniture/{v}.png"

    @field_validator("recipe", mode="before")
    @classmethod
    def _convert_recipe(cls, v: dict[str, Any] | None) -> FurnitureRecipe | None:
        if v is None:
            return None
        return FurnitureRecipe(**v)


class Furniture(BaseModel):
    """Represents a furniture summary.

    Attributes:
        id: The unique ID of the furniture.
        name: The name of the furniture.
        cost: The load cost of the furniture (optional).
        comfort: The comfort value (Adeptal Energy) provided by the furniture (optional).
        rarity: The rarity rank of the furniture.
        icon: The icon URL for the furniture.
        route: The route identifier for the furniture.
        categories: A list of categories the furniture belongs to.
        types: A list of types the furniture belongs to.
    """

    id: int
    name: str
    cost: int | None
    comfort: int | None
    rarity: int = Field(alias="rank")
    icon: str
    route: str
    categories: list[str]
    types: list[str]

    @field_validator("icon", mode="before")
    @classmethod
    def _convert_icon_url(cls, v: str) -> str:
        return f"https://gi.yatta.moe/assets/UI/furniture/{v}.png"


class FurnitureSet(BaseModel):
    """Represents a furniture set summary.

    Attributes:
        id: The unique ID of the furniture set.
        name: The name of the furniture set.
        icon: The icon URL for the furniture set.
        route: The route identifier for the furniture set.
        categories: A list of categories the set belongs to.
        types: A list of types the set belongs to.
    """

    id: int
    name: str
    icon: str
    route: str
    categories: list[str]
    types: list[str]

    @field_validator("icon", mode="before")
    @classmethod
    def _convert_icon_url(cls, v: str) -> str:
        return f"https://gi.yatta.moe/assets/UI/furnitureSuite/{v}.png"

    @field_validator("categories", mode="before")
    @classmethod
    def _convert_categories(cls, v: list[str] | None) -> list[str]:
        return v or []

    @field_validator("types", mode="before")
    @classmethod
    def _convert_types(cls, v: list[str] | None) -> list[str]:
        return v or []


class FurnitureItem(BaseModel):
    """Represents a single furniture item within a furniture set.

    Attributes:
        id: The ID of the furniture item.
        rarity: The rarity rank of the furniture item.
        icon: The icon URL of the furniture item.
    """

    id: int
    rarity: int = Field(alias="rank")
    icon: str

    @field_validator("icon", mode="before")
    @classmethod
    def _convert_icon_url(cls, v: str) -> str:
        return f"https://gi.yatta.moe/assets/UI/furniture/{v}.png"


class FurnitureSetFavoriteNPC(BaseModel):
    """Represents an NPC who favors a particular furniture set.

    Attributes:
        id: The ID of the NPC.
        icon: The icon URL of the NPC.
    """

    id: str
    icon: str


class FurnitureSetDetail(BaseModel):
    """Represents detailed information about a furniture set.

    Attributes:
        id: The unique ID of the furniture set.
        name: The name of the furniture set.
        icon: The icon URL for the furniture set.
        route: The route identifier for the furniture set.
        categories: A list of categories the set belongs to.
        types: A list of types the set belongs to.
        description: The description of the furniture set.
        furniture_items: A list of furniture items included in the set.
        favorite_npcs: A list of NPCs who favor this set.
    """

    id: int
    name: str
    icon: str
    route: str
    categories: list[str]
    types: list[str]
    description: str
    furniture_items: list[FurnitureItem] = Field(alias="suiteItemList")
    favorite_npcs: list[FurnitureSetFavoriteNPC] = Field(alias="favoriteNpcList")

    @field_validator("icon", mode="before")
    @classmethod
    def _convert_icon_url(cls, v: str) -> str:
        return f"https://gi.yatta.moe/assets/UI/furnitureSuite/{v}.png"

    @field_validator("categories", mode="before")
    @classmethod
    def _convert_categories(cls, v: list[str] | None) -> list[str]:
        return v or []

    @field_validator("types", mode="before")
    @classmethod
    def _convert_types(cls, v: list[str] | None) -> list[str]:
        return v or []

    @field_validator("furniture_items", mode="before")
    @classmethod
    def _convert_furniture_items(cls, v: dict[str, dict[str, Any]]) -> list[FurnitureItem]:
        return [FurnitureItem(id=int(item_id), **v[item_id]) for item_id in v]

    @field_validator("favorite_npcs", mode="before")
    @classmethod
    def _convert_favored_ids(
        cls, v: dict[str, dict[str, Any]] | None
    ) -> list[FurnitureSetFavoriteNPC]:
        return (
            [FurnitureSetFavoriteNPC(id=id_, icon=data["icon"]) for id_, data in v.items()]
            if v is not None
            else []
        )
