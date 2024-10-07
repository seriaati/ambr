from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field, field_validator

__all__ = ("Artifact", "ArtifactAffix", "ArtifactSet", "ArtifactSetDetail")


class ArtifactAffix(BaseModel):
    """
    Represents an artifact set's set effect.

    Attributes:
        id (str): The effect's ID.
        effect (str): The effect's description.
    """

    id: str
    effect: str


class Artifact(BaseModel):
    """
    Represents an artifact.

    Attributes:
        pos (str): The position of the artifact.
        name (str): The name of the artifact.
        description (str): The description of the artifact.
        max_rarity (int): The maximum rarity of the artifact.
        icon (str): The name of the icon file for the artifact.
    """

    pos: str
    name: str
    description: str
    max_rarity: int = Field(alias="maxLevel")
    icon: str

    @field_validator("icon", mode="before")
    def _convert_icon_url(cls, v: str) -> str:
        return f"https://gi.yatta.moe/assets/UI/reliquary/{v}.png"


class ArtifactSetDetail(BaseModel):
    """
    Represents an artifact set detail.

    Attributes:
        id (int): The artifact set's ID.
        name (str): The artifact set's name.
        rarity_list (list[int]): The artifact set's rarity list.
        affix_list (list[ArtifactAffix]): The artifact set's affix list.
        icon (str): The artifact set's icon.
        route (str): The artifact set's route.
        artifacts (list[Artifact]): Artifacts that belong to the artifact set.
    """

    id: int
    name: str
    rarity_list: list[int] = Field(alias="levelList")
    affix_list: list[ArtifactAffix] = Field(alias="affixList")
    icon: str
    route: str
    artifacts: list[Artifact] = Field(alias="suit")

    @field_validator("affix_list", mode="before")
    def _convert_affix_list(cls, v: dict[str, str]) -> list[ArtifactAffix]:
        return [ArtifactAffix(id=k, effect=v[k]) for k in v]

    @field_validator("icon", mode="before")
    def _convert_icon_url(cls, v: str) -> str:
        return f"https://gi.yatta.moe/assets/UI/reliquary/{v}.png"

    @field_validator("artifacts", mode="before")
    def _convert_artifacts(cls, v: dict[str, dict[str, Any]]) -> list[Artifact]:
        return [Artifact(pos=artifact_pos, **v[artifact_pos]) for artifact_pos in v]


class ArtifactSet(BaseModel):
    """
    Represents an artifact set.

    Attributes:
        id (int): The artifact set's ID.
        name (str): The artifact set's name.
        rarity_list (list[int]): Obtainable rarities of the artifact set.
        affix_list (list[ArtifactAffix]): The artifact set's set effect list.
        icon (str): The artifact set's icon.
        route (str): The artifact set's route.
        sort_order (int): The artifact set's sort order.
    """

    id: int
    name: str
    rarity_list: list[int] = Field(alias="levelList")
    affix_list: list[ArtifactAffix] = Field(alias="affixList")
    icon: str
    route: str
    sort_order: int = Field(alias="sortOrder")

    @field_validator("icon", mode="before")
    def _convert_icon_url(cls, v: str) -> str:
        return f"https://gi.yatta.moe/assets/UI/reliquary/{v}.png"

    @field_validator("affix_list", mode="before")
    def _convert_affix_list(cls, v: dict[str, str]) -> list[ArtifactAffix]:
        return [ArtifactAffix(id=k, effect=v[k]) for k in v]
