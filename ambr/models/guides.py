from __future__ import annotations

from typing import TYPE_CHECKING, Literal

from pydantic import Field, field_validator

from ._base import BaseModel

if TYPE_CHECKING:
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
    """Represents a character within a guide context.

    Attributes:
        id: The character's ID (can be string or int).
        rarity: The character's rarity (4 or 5 star).
        weapon_type: The type of weapon the character uses.
        icon: The character's icon URL.
        route: The route identifier for the character.
    """

    id: str | int
    rarity: Literal[4, 5] = Field(alias="rank")
    weapon_type: WeaponType = Field(alias="weaponType")
    icon: str
    route: str


class GuideWeapon(BaseModel):
    """Represents a weapon within a guide context.

    Attributes:
        id: The weapon's ID.
        rarity: The weapon's rarity (1 to 5 star).
        type: The type of the weapon.
        icon: The weapon's icon URL.
        route: The route identifier for the weapon.
    """

    id: int
    rarity: Literal[1, 2, 3, 4, 5] = Field(alias="rank")
    type: WeaponType
    icon: str
    route: str


class GuideArtifact(BaseModel):
    """Represents an artifact within a guide context.

    Attributes:
        id: The artifact set's ID.
        icon: The icon URL (likely for one piece of the set).
        rarities: A list of possible rarity levels for the artifact set.
        route: The route identifier for the artifact set.
    """

    id: int
    icon: str
    rarities: list[int] = Field(alias="levelList")
    route: str


class AvailableItems(BaseModel):
    """Container for available characters, weapons, and artifacts referenced in guides.

    Attributes:
        characters: A dictionary mapping character IDs to GuideCharacter objects.
        weapons: A dictionary mapping weapon IDs to GuideWeapon objects.
        artifacts: A dictionary mapping artifact set IDs to GuideArtifact objects.
    """

    characters: dict[str, GuideCharacter] = Field(alias="avatar")
    weapons: dict[str, GuideWeapon] = Field(alias="weapon")
    artifacts: dict[str, GuideArtifact] = Field(alias="reliquary")


class GWBuildInfoNormalArtifact(BaseModel):
    """Represents a standard artifact reference in a Genshin Wizard build.

    Attributes:
        id: The artifact set ID.
        type: Always "normal".
    """

    id: int
    type: Literal["normal"]


class GwBuildInfoCustomArtifact(BaseModel):
    """Represents a custom artifact reference in a Genshin Wizard build.

    Attributes:
        id: A custom identifier string for the artifact.
        type: Always "custom".
    """

    id: str
    type: Literal["custom"]


class GWBuildInfo(BaseModel):
    """Represents a specific piece of information within a Genshin Wizard build section.

    Attributes:
        inline: Whether the information should be displayed inline.
        name: The name or label for this piece of information (e.g., "Main Stats").
        value: The textual value associated with the name (optional).
        weapons: A dictionary mapping recommended weapon IDs to their names (optional).
        artifacts: A list of recommended artifact sets (normal or custom) (optional).
    """

    inline: bool
    name: str
    value: str | None = None
    weapons: dict[int, str] | None = Field(None, alias="weaponList")
    """Weapon ID to weapon name."""
    artifacts: list[GWBuildInfoNormalArtifact | GwBuildInfoCustomArtifact] | None = Field(
        None, alias="reliquaryList"
    )


class GWBuild(BaseModel):
    """Represents a complete build recommendation from Genshin Wizard.

    Attributes:
        title: The title of the build (e.g., "Support Build").
        credits: Attribution for the build information.
        info: A list of detailed information sections (GWBuildInfo) for the build.
    """

    title: str
    credits: str
    info: list[GWBuildInfo]


class GWPlaystyle(BaseModel):
    """Represents playstyle information from Genshin Wizard.

    Attributes:
        title: The title of the playstyle section.
        description: The detailed description of the playstyle.
        credits: Attribution for the playstyle information.
    """

    title: str
    description: str
    credits: str


class GWSynergyNormalCharacter(BaseModel):
    """Represents a specific character recommendation in a Genshin Wizard synergy team.

    Attributes:
        id: The character's ID (can be string or int).
        type: Always "normal".
    """

    id: str | int
    type: Literal["normal"]


class GWSynergyElementCharacter(BaseModel):
    """Represents a character slot recommendation based on element in a Genshin Wizard synergy team.

    Attributes:
        element: The recommended element for this slot.
        type: Always "element".
    """

    element: Element
    type: Literal["element"]


class GWSynergyFlexibleCharacter(BaseModel):
    """Represents a flexible character slot in a Genshin Wizard synergy team.

    Attributes:
        type: Always "flexible".
    """

    type: Literal["flexible"]


class GWSynergyInfo(BaseModel):
    """Represents a piece of textual information related to Genshin Wizard synergies.

    Attributes:
        inline: Whether the information should be displayed inline.
        name: The name or label for this piece of information.
        value: The textual value associated with the name.
    """

    inline: bool
    name: str
    value: str


class GWSynergy(BaseModel):
    """Represents synergy and team composition information from Genshin Wizard.

    Attributes:
        title: The title of the synergy section.
        info: Optional list of textual synergy information (GWSynergyInfo).
        teams: A list of recommended team compositions. Each team is a list of character slots.
        credits: Attribution for the synergy information.
    """

    title: str
    info: list[GWSynergyInfo] | None = None
    teams: list[
        list[GWSynergyNormalCharacter | GWSynergyElementCharacter | GWSynergyFlexibleCharacter]
    ] = Field(alias="synergiestList")
    credits: str


class GWData(BaseModel):
    """Container for all Genshin Wizard guide data for a character.

    Attributes:
        builds: A list of recommended builds (GWBuild).
        playstyle: Optional playstyle information (GWPlaystyle).
        synergies: Synergy and team composition information (GWSynergy).
    """

    builds: list[GWBuild]
    playstyle: GWPlaystyle | None = None
    synergies: GWSynergy


class AzaBestItem(BaseModel):
    """Represents a best-ranked item (character or weapon) from genshin.aza.gg.

    Attributes:
        id: The ID of the item (character or weapon).
        value: A numerical value representing the ranking or usage rate.
    """

    id: int
    value: float

    @property
    def percentage(self) -> str:
        """Formats the value as a percentage string (e.g., "85.3%")."""
        return f"{self.value * 100:.1f}%"


class AzaBestArtifact(BaseModel):
    """Represents an artifact piece within a best artifact set from genshin.aza.gg.

    Attributes:
        id: The artifact set ID.
        num: The number of pieces recommended from this set (e.g., 2 or 4).
    """

    id: int
    num: int


class AzaBestArtifactSets(BaseModel):
    """Represents a ranked artifact set combination from genshin.aza.gg.

    Attributes:
        sets: A list describing the combination of artifact sets (AzaBestArtifact).
        value: A numerical value representing the ranking or usage rate of this combination.
    """

    sets: list[AzaBestArtifact] = Field(alias="setList")
    value: float

    @field_validator("sets", mode="before")
    @classmethod
    def __transform_sets(cls, value: dict[str, int]) -> list[AzaBestArtifact]:
        return [AzaBestArtifact(id=int(k), num=v) for k, v in value.items()]

    @property
    def percentage(self) -> str:
        """Formats the value as a percentage string (e.g., "72.1%")."""
        return f"{self.value * 100:.1f}%"


class AzaData(BaseModel):
    """Container for all genshin.aza.gg guide data for a character.

    Attributes:
        best_characters: Dictionary mapping character IDs to their ranking/usage data.
        best_weapons: Dictionary mapping weapon IDs to their ranking/usage data.
        best_artifact_sets: List of ranked artifact set combinations.
        constellation_usage: Dictionary mapping constellation numbers (as strings) to usage rates.
    """

    best_characters: dict[str, AzaBestItem] = Field(alias="bestAvatarList")
    best_weapons: dict[str, AzaBestItem] = Field(alias="bestWeaponList")
    best_artifact_sets: list[AzaBestArtifactSets] = Field(alias="bestReliquaryList")
    constellation_usage: dict[str, float] = Field(alias="constellationsUsage")


class CharacterGuide(BaseModel):
    """Represents the complete guide data for a character, combining multiple sources.

    Attributes:
        available_items: Information about items (characters, weapons, artifacts) referenced in the guide.
        gw_data: Optional guide data sourced from Genshin Wizard.
        aza_data: Optional guide data sourced from genshin.aza.gg.
    """

    available_items: AvailableItems = Field(alias="dataList")
    gw_data: GWData | None = Field(None, alias="gwData")
    """Genshin Wizard data."""
    aza_data: AzaData | None = Field(None, alias="azaData")
    """genshin.aza.gg data."""
