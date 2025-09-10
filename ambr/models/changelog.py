from __future__ import annotations

from pydantic import Field, field_validator

from ._base import BaseModel

__all__ = ("Changelog", "Item")


class Item(BaseModel):
    """Represents an item within a changelog.

    Attributes:
        category: The category of the item (e.g., "characters", "weapons").
        ids: A list of IDs belonging to this category that were changed.
    """

    category: str
    ids: list[str]


class Changelog(BaseModel):
    """Represents a change log entry.

    Attributes:
        id: The unique identifier for the change log.
        version: The version string associated with the change log.
        items: A list of items detailing the changes in this version.
        beta: Indicates if this change log is for a beta version.
    """

    id: int
    version: str
    items: list[Item]
    beta: bool = Field(False)

    @field_validator("items", mode="before")
    @classmethod
    def _convert_items(cls, v: dict[str, list[str]]) -> list[Item]:
        return [Item(category=k, ids=v) for k, v in v.items()]  # type: ignore
