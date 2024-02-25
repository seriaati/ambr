from pydantic import BaseModel, Field, field_validator

__all__ = (
    "Item",
    "ChangeLog",
)


class Item(BaseModel):
    category: str
    ids: list[str]


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
    items: list[Item]
    beta: bool = Field(False)

    @field_validator("items", mode="before")
    def _convert_items(cls, v: dict[str, list[str]]) -> list[Item]:
        return [Item(category=k, ids=v) for k, v in v.items()]  # type: ignore
