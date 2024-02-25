from enum import IntEnum
from typing import Any

from pydantic import BaseModel, Field, field_validator

__all__ = (
    "City",
    "Domain",
    "Domains",
)


class City(IntEnum):
    MONDSTAT = 1
    LIYUE = 2
    INAZUMA = 3
    SUMERU = 4
    FONTAINE = 5


class Domain(BaseModel):
    id: int
    name: str
    rewards: list[int] = Field(alias="reward")
    city: City


class Domains(BaseModel):
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
    def convert_domains(cls, v: dict[str, dict[str, Any]]) -> list[Domain]:
        return cls._convert_domains(v)
