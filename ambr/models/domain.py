from __future__ import annotations

from typing import Any

from pydantic import Field, field_validator

from ambr.enums import City

from ._base import BaseModel

__all__ = ("Domain", "DomainReward", "Domains")


class DomainReward(BaseModel):
    """Represents a potential reward from a domain.

    Attributes:
        id: The ID of the reward item.
    """

    id: int

    @property
    def icon(self) -> str:
        """Returns the icon URL for the reward item."""
        return f"https://gi.yatta.moe/assets/UI/UI_ItemIcon_{self.id}.png"


class Domain(BaseModel):
    """Represents a domain and its potential rewards for a specific day.

    Attributes:
        id: The unique ID of the domain.
        name: The name of the domain.
        rewards: A list of potential rewards available from the domain.
        city: The city/region the domain is located in.
    """

    id: int
    name: str
    rewards: list[DomainReward] = Field(alias="reward")
    city: City

    @field_validator("rewards", mode="before")
    @classmethod
    def __convert_rewards(cls, v: list[int]) -> list[DomainReward]:
        return [DomainReward(id=id_) for id_ in v]


class Domains(BaseModel):
    """Container for domains available on each day of the week.

    Attributes:
        monday: List of domains available on Monday.
        tuesday: List of domains available on Tuesday.
        wednesday: List of domains available on Wednesday.
        thursday: List of domains available on Thursday.
        friday: List of domains available on Friday.
        saturday: List of domains available on Saturday.
        sunday: List of domains available on Sunday.
    """

    monday: list[Domain]
    tuesday: list[Domain]
    wednesday: list[Domain]
    thursday: list[Domain]
    friday: list[Domain]
    saturday: list[Domain]
    sunday: list[Domain]

    @staticmethod
    def _convert_domains(domains: dict[str, dict[str, Any]]) -> list[Domain]:
        return [Domain(**domain) for domain in domains.values()]

    @field_validator("*", mode="before")
    @classmethod
    def __convert_domains(cls, v: dict[str, dict[str, Any]]) -> list[Domain]:
        return cls._convert_domains(v)
