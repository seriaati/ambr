from __future__ import annotations

import datetime
from typing import Any

from pydantic import BaseModel, Field, field_validator

from ..utils import remove_html_tags

__all__ = (
    "Abyss",
    "AbyssData",
    "AbyssEnemy",
    "AbyssEnemyProperty",
    "AbyssResponse",
    "Blessing",
    "ChallengeTarget",
    "Chamber",
    "Floor",
    "LeyLineDisorder",
)


class Blessing(BaseModel):
    """Represents the Benediction of the Abyssal Moon (Blessing) for a Spiral Abyss cycle.

    Attributes:
        description: The description of the blessing's effect.
        level_config_name: Internal configuration name for the blessing.
        visible: Whether the blessing is currently visible or active.
    """

    description: str
    level_config_name: str = Field(..., alias="levelConfigName")
    visible: bool

    @field_validator("description", mode="before")
    @classmethod
    def _format_description(cls, v: str) -> str:
        return remove_html_tags(v)


class ChallengeTarget(BaseModel):
    """Represents the challenge targets for a Spiral Abyss chamber (e.g., time limits).

    Attributes:
        type: A format string describing the challenge type (e.g., "Challenge time limit: {}s").
        values: A list of numerical values corresponding to the targets (e.g., time limits for 1, 2, 3 stars).
    """

    type: str
    values: list[int]

    @property
    def formatted(self) -> str:
        """Returns the challenge target description with values formatted in."""
        return self.type.format("/".join(str(v) for v in self.values))


class Chamber(BaseModel):
    """Represents a single chamber within a Spiral Abyss floor.

    Attributes:
        id: The ID of the chamber (usually 1, 2, or 3).
        challenge_target: The challenge targets (e.g., time limits) for this chamber.
        enemy_level: The base level of the enemies in this chamber.
        wave_one_enemies: A list of enemy IDs appearing in the first half/wave.
        wave_two_enemies: An optional list of enemy IDs appearing in the second half/wave.
    """

    id: int
    challenge_target: ChallengeTarget = Field(..., alias="challengeTarget")
    enemy_level: int = Field(..., alias="monsterLevel")
    wave_one_enemies: list[int] = Field(..., alias="firstMonsterList")
    wave_two_enemies: list[int] | None = Field(None, alias="secondMonsterList")


class LeyLineDisorder(BaseModel):
    """Represents a Ley Line Disorder effect active on a Spiral Abyss floor.

    Attributes:
        description: The description of the disorder's effect.
        level_config_name: Internal configuration name for the disorder.
        visible: Whether the disorder is currently visible or active.
    """

    description: str
    level_config_name: str = Field(..., alias="levelConfigName")
    visible: bool

    @field_validator("description", mode="before")
    @classmethod
    def _format_description(cls, v: str) -> str:
        return remove_html_tags(v)


class Floor(BaseModel):
    """Represents a floor within the Spiral Abyss (either Corridor or Spire).

    Attributes:
        id: The ID of the floor (e.g., 9, 10, 11, 12).
        chambers: A list of chambers within this floor.
        ley_line_disorders: A list of Ley Line Disorders active on this floor.
        override_enemy_level: An optional override for the enemy level on this floor.
        team_num: The number of teams required for this floor (usually 1 or 2).
    """

    id: int
    chambers: list[Chamber] = Field(..., alias="chamberList")
    ley_line_disorders: list[LeyLineDisorder] = Field(..., alias="leyLineDisorder")
    override_enemy_level: int = Field(..., alias="overrideMonsterLevel")
    team_num: int = Field(..., alias="teamNum")


class AbyssData(BaseModel):
    """Represents data for either the Abyss Corridor or the Abyssal Moon Spire.

    Attributes:
        open_time: The time when this specific section (usually Spire) becomes available (optional).
        floors: A list of floors within this section.
    """

    open_time: datetime.datetime | None = Field(None, alias="openTime")
    floors: list[Floor] = Field(..., alias="floorList")

    @field_validator("open_time", mode="before")
    @classmethod
    def _format_open_time(cls, v: int) -> datetime.datetime | None:
        return datetime.datetime.fromtimestamp(v) if v else None


class Abyss(BaseModel):
    """Represents a full Spiral Abyss cycle configuration.

    Attributes:
        id: The unique ID identifying this Spiral Abyss cycle.
        open_time: The start date and time of this cycle.
        close_time: The end date and time of this cycle.
        blessing: The Benediction of the Abyssal Moon active during this cycle.
        abyss_corridor: Data for the Abyss Corridor floors (usually 1-8).
        abyssal_moon_spire: Data for the Abyssal Moon Spire floors (usually 9-12).
    """

    id: int
    open_time: datetime.datetime = Field(..., alias="openTime")
    close_time: datetime.datetime = Field(..., alias="closeTime")
    blessing: Blessing
    abyss_corridor: AbyssData = Field(..., alias="entrance")
    abyssal_moon_spire: AbyssData = Field(..., alias="schedule")

    @field_validator("open_time", mode="before")
    @classmethod
    def _format_open_time(cls, v: int) -> datetime.datetime:
        # example 1709258399
        return datetime.datetime.fromtimestamp(v)

    @field_validator("close_time", mode="before")
    @classmethod
    def _format_close_time(cls, v: int) -> datetime.datetime:
        # example 1709258399
        return datetime.datetime.fromtimestamp(v)

    @field_validator("blessing", mode="before")
    @classmethod
    def _format_blessing(cls, v: list[dict[str, Any]]) -> Blessing:
        return Blessing(**v[0])


class AbyssEnemyProperty(BaseModel):
    """Represents a base property of an enemy found in the Spiral Abyss.

    Attributes:
        initial_value: The base value of the property at level 1.
        type: The identifier string for the property (e.g., "FIGHT_PROP_BASE_HP").
        growth_type: The identifier string for the property's growth curve.
    """

    initial_value: float = Field(..., alias="initValue")
    type: str = Field(..., alias="propType")
    growth_type: str = Field(..., alias="type")


class AbyssEnemy(BaseModel):
    """Represents an enemy that can appear in the Spiral Abyss.

    Attributes:
        icon: The icon URL for the enemy.
        id: The unique ID of the enemy.
        link: A boolean indicating if there's a link available (purpose unclear).
        name: The name of the enemy.
        properties: A list of base properties (like HP, ATK, DEF) and their growth curves.
    """

    icon: str
    id: int
    link: bool
    name: str
    properties: list[AbyssEnemyProperty] = Field(..., alias="prop")

    @field_validator("icon", mode="before")
    @classmethod
    def _convert_icon_url(cls, v: str) -> str:
        return f"https://gi.yatta.moe/assets/UI{'/monster' if 'MonsterIcon' in v else ''}/{v}.png"

    @field_validator("properties", mode="before")
    @classmethod
    def _convert_properties(cls, v: list[dict[str, Any]]) -> list[AbyssEnemyProperty]:
        return [AbyssEnemyProperty(**prop) for prop in v]


class AbyssResponse(BaseModel):
    """Represents the complete response for Spiral Abyss data.

    Attributes:
        enemies: A dictionary mapping enemy IDs to their details (AbyssEnemy).
        abyss_items: A list containing data for one or more Spiral Abyss cycles (Abyss).
    """

    enemies: dict[str, AbyssEnemy] = Field(..., alias="monsterList")
    abyss_items: list[Abyss] = Field(..., alias="items")

    @field_validator("enemies", mode="before")
    @classmethod
    def _convert_enemies(cls, v: dict[str, dict[str, Any]]) -> dict[str, AbyssEnemy]:
        return {item_id: AbyssEnemy(**v[item_id]) for item_id in v}

    @field_validator("abyss_items", mode="before")
    @classmethod
    def _convert_abyss_items(cls, v: dict[str, dict[str, Any]]) -> list[Abyss]:
        result: list[Abyss] = []
        for item_data in v.values():
            item_data["openTime"] = item_data["schedule"]["openTime"]
            result.append(Abyss(**item_data))
        return result
