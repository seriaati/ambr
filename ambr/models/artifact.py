from __future__ import annotations

from typing import Any

from pydantic import Field, computed_field, field_validator

from ._base import BaseModel

__all__ = ("Artifact", "ArtifactAffix", "ArtifactSet", "ArtifactSetDetail")


class ArtifactAffix(BaseModel):
    """Represents an artifact set's bonus effect (2-piece or 4-piece).

    Attributes:
        id: The identifier for the set effect (e.g., "2" or "4").
        effect: The description of the set effect.
    """

    id: str
    effect: str


class Artifact(BaseModel):
    """Represents a single artifact piece within a set.

    Attributes:
        pos: The position or slot of the artifact (e.g., "flower", "plume", "sands", "goblet", "circlet").
        name: The name of the specific artifact piece.
        description: The flavor text or description of the artifact piece.
        max_rarity: The maximum rarity level this artifact piece can have.
        icon: The icon URL for the artifact piece.
        story: The lore of this artifact piece, None if fetch_story=False.
    """

    pos: str
    name: str
    description: str
    max_rarity: int = Field(alias="maxLevel")
    icon_path: str = Field(alias="icon")
    story: str | None = None

    @computed_field
    @property
    def icon(self) -> str:
        """The icon URL for the artifact piece."""
        return f"https://gi.yatta.moe/assets/UI/reliquary/{self.icon_path}.png"


class ArtifactSetDetail(BaseModel):
    """Represents detailed information about an artifact set.

    Attributes:
        id: The unique ID of the artifact set.
        name: The name of the artifact set.
        rarity_list: A list of possible rarity levels for artifacts in this set.
        affix_list: A list of the set bonus effects (2-piece and 4-piece).
        icon: The icon URL representing the artifact set (usually the flower piece).
        route: The route identifier for the artifact set.
        artifacts: A list of the individual artifact pieces belonging to this set.
    """

    id: int
    name: str
    rarity_list: list[int] = Field(alias="levelList")
    affix_list: list[ArtifactAffix] = Field(alias="affixList")
    icon: str
    route: str
    artifacts: list[Artifact] = Field(alias="suit")

    @field_validator("affix_list", mode="before")
    @classmethod
    def _convert_affix_list(cls, v: dict[str, str]) -> list[ArtifactAffix]:
        return [ArtifactAffix(id=k, effect=v[k]) for k in v]

    @field_validator("icon", mode="before")
    @classmethod
    def _convert_icon_url(cls, v: str) -> str:
        return f"https://gi.yatta.moe/assets/UI/reliquary/{v}.png"

    @field_validator("artifacts", mode="before")
    @classmethod
    def _convert_artifacts(cls, v: dict[str, dict[str, Any]]) -> list[Artifact]:
        return [Artifact(pos=artifact_pos, **v[artifact_pos]) for artifact_pos in v]


class ArtifactSet(BaseModel):
    """Represents an artifact set summary.

    Attributes:
        id: The unique ID of the artifact set.
        name: The name of the artifact set.
        rarity_list: A list of possible rarity levels for artifacts in this set.
        affix_list: A list of the set bonus effects (2-piece and 4-piece).
        icon: The icon URL representing the artifact set (usually the flower piece).
        route: The route identifier for the artifact set.
        sort_order: The sorting order value for the artifact set.
    """

    id: int
    name: str
    rarity_list: list[int] = Field(alias="levelList")
    affix_list: list[ArtifactAffix] = Field(alias="affixList")
    icon: str
    route: str
    sort_order: int = Field(alias="sortOrder")

    @field_validator("icon", mode="before")
    @classmethod
    def _convert_icon_url(cls, v: str) -> str:
        return f"https://gi.yatta.moe/assets/UI/reliquary/{v}.png"

    @field_validator("affix_list", mode="before")
    @classmethod
    def _convert_affix_list(cls, v: dict[str, str]) -> list[ArtifactAffix]:
        return [ArtifactAffix(id=k, effect=v[k]) for k in v]
