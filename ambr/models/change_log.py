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
    """
    Represents a change log.

    Attributes
    ----------
    id: :class:`int`
        The change log's ID.
    version: :class:`str`
        The change log's version.
    items: List[:class:`Item`]
        The change log's items.
    beta: :class:`bool`
        Whether the change log is for beta.
    """

    id: int
    version: str
    items: List[Item]
    beta: bool = Field(False)

    @field_validator("items", mode="before")
    def _convert_items(cls, v: Dict[str, List[str]]) -> List[Item]:
        return [Item(category=k, ids=v) for k, v in v.items()]  # type: ignore
