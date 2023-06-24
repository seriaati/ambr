from typing import Any, Dict, List

from pydantic import BaseModel, Field, validator


class ArtifactAffix(BaseModel):
    """
    Represents an artifact affix.

    Attributes
    ----------
    id: :class:`str`
        The artifact affix's ID.
    effect: :class:`str`
        The artifact affix's effect.
    """

    id: str
    effect: str


class Artifact(BaseModel):
    """
    Represents an artifact.

    Attributes
    ----------
    pos: :class:`str`
        The position of the artifact.
    name: :class:`str`
        The name of the artifact.
    description: :class:`str`
        The description of the artifact.
    max_rarity: :class:`int`
        The maximum rarity of the artifact.
    icon: :class:`str`
        The name of the icon file for the artifact.
    """

    pos: str
    name: str
    description: str
    max_rarity: int = Field(alias="maxLevel")
    icon: str

    @validator("icon", pre=True)
    def _add_icon_url(cls, v: str) -> str:
        return f"https://api.ambr.top/assets/UI/{v}.png"


class ArtifactSetDetail(BaseModel):
    """
    Represents an artifact set detail.

    Attributes
    ----------
    id: :class:`int`
        The artifact set detail's ID.
    name: :class:`str`
        The artifact set detail's name.
    rarity_list: List[:class:`int`]
        The artifact set detail's rarity list.
    affix_list: List[:class:`ArtifactAffix`]
        The artifact set detail's affix list.
    icon: :class:`str`
        The artifact set detail's icon.
    route: :class:`str`
        The artifact set detail's route.
    artifacts: List[:class:`Artifact`]
        The artifact set detail's artifacts.
    """

    id: int
    name: str
    rarity_list: List[int] = Field(alias="levelList")
    affix_list: List[ArtifactAffix] = Field(alias="affixList")
    icon: str
    route: str
    artifacts: List[Artifact] = Field(alias="suit")

    @validator("affix_list", pre=True)
    def _add_affix_list(cls, v: Dict[str, str]) -> List[ArtifactAffix]:
        return [ArtifactAffix(id=k, effect=v[k]) for k in v]

    @validator("icon", pre=True)
    def _add_icon_url(cls, v: str) -> str:
        return f"https://api.ambr.top/assets/UI/{v}.png"

    @validator("artifacts", pre=True)
    def _add_artifacts(cls, v: Dict[str, Dict[str, Any]]) -> List[Artifact]:
        return [Artifact(pos=artifact_pos, **v[artifact_pos]) for artifact_pos in v]


class ArtifactSet(BaseModel):
    """
    Represents an artifact set.

    Attributes
    ----------
    id: :class:`int`
        The artifact set's ID.
    name: :class:`str`
        The artifact set's name.
    rarity_list: List[:class:`int`]
        The artifact set's rarity list.
    affix_list: List[:class:`str`]
        The artifact set's affix list.
    icon: :class:`str`
        The artifact set's icon.
    route: :class:`str`
        The artifact set's route.
    sort_order: :class:`int`
        The artifact set's sort order.
    """

    id: int
    name: str
    rarity_list: List[int] = Field(alias="levelList")
    affix_list: List[ArtifactAffix] = Field(alias="affixList")
    icon: str
    route: str
    sort_order: int = Field(alias="sortOrder")

    @validator("icon", pre=True)
    def _add_icon_url(cls, v: str) -> str:
        return f"https://api.ambr.top/assets/UI/{v}.png"

    @validator("affix_list", pre=True)
    def _add_affix_list(cls, v: Dict[str, str]) -> List[ArtifactAffix]:
        return [ArtifactAffix(id=k, effect=v[k]) for k in v]
