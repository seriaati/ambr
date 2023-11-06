from enum import IntEnum
from typing import Any, Dict, List

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
    rewards: List[int] = Field(alias="reward")
    city: City


class Domains(BaseModel):
    monday: List[Domain]
    tuesday: List[Domain]
    wednesday: List[Domain]
    thursday: List[Domain]
    friday: List[Domain]
    saturday: List[Domain]
    sunday: List[Domain]

    @staticmethod
    def _convert_domains(domains: Dict[str, Dict[str, Any]]) -> List[Domain]:
        return [Domain(**domain) for domain in domains.values()]

    @field_validator("*", mode="before")
    def convert_domains(cls, v: Dict[str, Dict[str, Any]]) -> List[Domain]:
        return cls._convert_domains(v)
