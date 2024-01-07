from typing import Dict, List

from pydantic import BaseModel, Field, field_validator

__all__ = (
    "Item",
    "ChangeLog",
)


class Item(BaseModel):
    category: str
    ids: List[str]


class ChangeLog(BaseModel):
    id: int
    version: str
    items: List[Item]
    beta: bool = Field(False)

    @field_validator("items", mode="before")
    def _convert_items(cls, v: Dict[str, List[str]]) -> List[Item]:
        return [Item(category=k, ids=v) for k, v in v.items()]  # type: ignore
