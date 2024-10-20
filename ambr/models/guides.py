from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field, field_validator

from ..enums import Element, WeaponType

__all__ = (
    "AvailableItems",
    "AzaBestArtifact",
    "AzaBestArtifactSets",
    "AzaBestItem",
    "AzaData",
    "CharacterGuide",
    "GWBuild",
    "GWBuildInfo",
    "GWBuildInfoNormalArtifact",
    "GWData",
    "GWPlaystyle",
    "GWSynergy",
    "GWSynergyElementCharacter",
    "GWSynergyFlexibleCharacter",
    "GWSynergyInfo",
    "GWSynergyNormalCharacter",
    "GuideArtifact",
    "GuideCharacter",
    "GuideWeapon",
    "GwBuildInfoCustomArtifact",
)


class GuideCharacter(BaseModel):
    id: int
    rarity: Literal[4, 5] = Field(alias="rank")
    weapon_type: WeaponType = Field(alias="weaponType")
    icon: str
    route: str


class GuideWeapon(BaseModel):
    id: int
    rarity: Literal[1, 2, 3, 4, 5] = Field(alias="rank")
    type: WeaponType
    icon: str
    route: str


class GuideArtifact(BaseModel):
    id: int
    icon: str
    rarities: list[int] = Field(alias="levelList")
    route: str


class AvailableItems(BaseModel):
    characters: dict[str, GuideCharacter] = Field(alias="avatar")
    weapons: dict[str, GuideWeapon] = Field(alias="weapon")
    artifacts: dict[str, GuideArtifact] = Field(alias="reliquary")


class GWBuildInfoNormalArtifact(BaseModel):
    id: int
    type: Literal["normal"]


class GwBuildInfoCustomArtifact(BaseModel):
    id: str
    type: Literal["custom"]


class GWBuildInfo(BaseModel):
    inline: bool
    name: str
    value: str | None = None
    weapons: dict[int, str] | None = Field(None, alias="weaponList")
    """Weapon ID to weapon name."""
    artifacts: list[GWBuildInfoNormalArtifact | GwBuildInfoCustomArtifact] | None = Field(
        None, alias="reliquaryList"
    )


class GWBuild(BaseModel):
    """Genshin Wizard build."""

    title: str
    credits: str
    info: list[GWBuildInfo]


class GWPlaystyle(BaseModel):
    title: str
    description: str
    credits: str


class GWSynergyNormalCharacter(BaseModel):
    id: int
    type: Literal["normal"]


class GWSynergyElementCharacter(BaseModel):
    element: Element
    type: Literal["element"]


class GWSynergyFlexibleCharacter(BaseModel):
    type: Literal["flexible"]


class GWSynergyInfo(BaseModel):
    inline: bool
    name: str
    value: str


class GWSynergy(BaseModel):
    title: str
    info: list[GWSynergyInfo] | None = None
    teams: list[
        list[GWSynergyNormalCharacter | GWSynergyElementCharacter | GWSynergyFlexibleCharacter]
    ] = Field(alias="synergiestList")
    credits: str


class GWData(BaseModel):
    builds: list[GWBuild]
    playstyle: GWPlaystyle
    synergies: GWSynergy


class AzaBestItem(BaseModel):
    id: int
    value: float

    @property
    def percentage(self) -> str:
        return f"{self.value * 100:.1f}%"


class AzaBestArtifact(BaseModel):
    id: int
    num: int


class AzaBestArtifactSets(BaseModel):
    sets: list[AzaBestArtifact] = Field(alias="setList")
    value: float

    @field_validator("sets", mode="before")
    @classmethod
    def __transform_sets(cls, value: dict[str, int]) -> list[AzaBestArtifact]:
        return [AzaBestArtifact(id=int(k), num=v) for k, v in value.items()]

    @property
    def percentage(self) -> str:
        return f"{self.value * 100:.1f}%"


class AzaData(BaseModel):
    best_characters: dict[str, AzaBestItem] = Field(alias="bestAvatarList")
    best_weapons: dict[str, AzaBestItem] = Field(alias="bestWeaponList")
    best_artifact_sets: list[AzaBestArtifactSets] = Field(alias="bestReliquaryList")
    constellation_usage: dict[str, float] = Field(alias="constellationsUsage")


class CharacterGuide(BaseModel):
    available_items: AvailableItems = Field(alias="dataList")
    gw_data: GWData = Field(alias="gwData")
    """Genshin Wizard data."""
    aza_data: AzaData | None = Field(None, alias="azaData")
    """genshin.aza.gg data."""
