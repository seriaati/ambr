from enum import StrEnum
from typing import Dict, List

from pydantic import BaseModel, Field, validator


class ItemCategory(StrEnum):
    AVATAR = "avatar"
    WEAPON = "weapon"
    MATERIAL = "material"
    ARTIFACT = "reliquary"
    FOOD = "food"
    BOOK = "book"
    NAME_CARD = "namecard"
    MONSTER = "monster"
    FURNITURE = "furniture"
    TCG = "gcg"
    QUEST = "quest"


class Item(BaseModel):
    category: ItemCategory
    ids: List[str]


class ChangeLog(BaseModel):
    id: int
    version: str
    items: List[Item]
    beta: bool = Field(False)

    @validator("items", pre=True)
    def _convert_items(cls, v: Dict[str, List[str]]) -> List[Item]:
        return [Item(category=k, ids=v) for k, v in v.items()]  # type: ignore
