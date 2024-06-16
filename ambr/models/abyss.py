import datetime
from typing import Any

from pydantic import BaseModel, Field, field_validator

from ..utils import remove_html_tags

__all__ = (
    "Abyss",
    "AbyssData",
    "AbyssEnemy",
    "AbyssResponse",
    "Blessing",
    "ChallengeTarget",
    "Chamber",
    "Floor",
    "LeyLineDisorder",
)


class Blessing(BaseModel):
    """
    Blessing model.

    Attributes:
        description (str): Description of the blessing.
        level_config_name (str): Level configuration name.
        visible (bool): Visibility status.
    """

    description: str
    level_config_name: str = Field(..., alias="levelConfigName")
    visible: bool

    @field_validator("description", mode="before")
    def _format_description(cls, v: str) -> str:
        return remove_html_tags(v)


class ChallengeTarget(BaseModel):
    """
    ChallengeTarget model.

    Attributes:
        type (str): Type of the challenge target.
        values (list[int]): list of values.
        formatted (str): Formatted challenge target.
    """

    type: str
    values: list[int]

    @property
    def formatted(self) -> str:
        return self.type.format("/".join(str(v) for v in self.values))


class Chamber(BaseModel):
    """
    Chamber model.

    Attributes:
        id (int): ID of the chamber.
        challenge_target (ChallengeTarget): Challenge target.
        enemy_level (int): Enemy level.
        wave_one_enemies (list[int]): list of enemies in the first wave.
        wave_two_enemies (list[int] | None): list of enemies in the second wave.
    """

    id: int
    challenge_target: ChallengeTarget = Field(..., alias="challengeTarget")
    enemy_level: int = Field(..., alias="monsterLevel")
    wave_one_enemies: list[int] = Field(..., alias="firstMonsterList")
    wave_two_enemies: list[int] | None = Field(None, alias="secondMonsterList")


class LeyLineDisorder(BaseModel):
    """
    LeyLineDisorder model.

    Attributes:
        description (str): Description of the disorder.
        level_config_name (str): Level configuration name.
        visible (bool): Visibility status.
    """

    description: str
    level_config_name: str = Field(..., alias="levelConfigName")
    visible: bool

    @field_validator("description", mode="before")
    def _format_description(cls, v: str) -> str:
        return remove_html_tags(v)


class Floor(BaseModel):
    """
    Floor model.

    Attributes:
        id (int): ID of the floor.
        chambers (list[Chamber]): list of chambers.
        ley_line_disorders (list[LeyLineDisorder]): list of ley line disorders.
        override_enemy_level (int): Override enemy level.
        team_num (int): Number of teams.
    """

    id: int
    chambers: list[Chamber] = Field(..., alias="chamberList")
    ley_line_disorders: list[LeyLineDisorder] = Field(..., alias="leyLineDisorder")
    override_enemy_level: int = Field(..., alias="overrideMonsterLevel")
    team_num: int = Field(..., alias="teamNum")


class AbyssData(BaseModel):
    """
    AbyssData model.

    Attributes:
        open_time (datetime.datetime | None): Opening time.
        floors (list[Floor]): list of floors.
    """

    open_time: datetime.datetime | None = Field(None, alias="openTime")
    floors: list[Floor] = Field(..., alias="floorList")

    @field_validator("open_time", mode="before")
    def _format_open_time(cls, v: int) -> datetime.datetime | None:
        return datetime.datetime.fromtimestamp(v) if v else None


class Abyss(BaseModel):
    """
    Abyss model.

    Attributes:
        id (int): ID of the abyss.
        open_time (datetime.datetime): Opening time.
        close_time (datetime.datetime): Closing time.
        blessing (Blessing): Blessing.
        abyss_corridor (AbyssData): Abyss corridor.
        abyssal_moon_spire (AbyssData): Abyssal moon spire.
    """

    id: int
    open_time: datetime.datetime = Field(..., alias="openTime")
    close_time: datetime.datetime = Field(..., alias="closeTime")
    blessing: Blessing
    abyss_corridor: AbyssData = Field(..., alias="entrance")
    abyssal_moon_spire: AbyssData = Field(..., alias="schedule")

    @field_validator("open_time", mode="before")
    def _format_open_time(cls, v: int) -> datetime.datetime:
        # example 1709258399
        return datetime.datetime.fromtimestamp(v)

    @field_validator("close_time", mode="before")
    def _format_close_time(cls, v: int) -> datetime.datetime:
        # example 1709258399
        return datetime.datetime.fromtimestamp(v)

    @field_validator("blessing", mode="before")
    def _format_blessing(cls, v: list[dict[str, Any]]) -> Blessing:
        return Blessing(**v[0])


class AbyssEnemyProperty(BaseModel):
    """
    AbyssEnemyProperty model.

    Attributes:
        initial_value (float): Initial value.
        type (str): Type of the property, e.g. "FIGHT_PROP_BASE_HP".
        growth_type (str): Growth type, e.g. "GROW_CURVE_HP".
    """

    initial_value: float = Field(..., alias="initValue")
    type: str = Field(..., alias="propType")
    growth_type: str = Field(..., alias="type")


class AbyssEnemy(BaseModel):
    """
    AbyssEnemy model.

    Attributes:
        icon (str): Icon URL.
        id (int): ID of the enemy.
        link (bool): Link status.
        name (str): Name of the enemy.
    """

    icon: str
    id: int
    link: bool
    name: str
    properties: list[AbyssEnemyProperty] = Field(..., alias="prop")

    @field_validator("icon", mode="before")
    def _convert_icon_url(cls, v: str) -> str:
        return f"https://api.ambr.top/assets/UI{'/monster' if 'MonsterIcon' in v else ''}/{v}.png"

    @field_validator("properties", mode="before")
    def _convert_properties(cls, v: list[dict[str, Any]]) -> list[AbyssEnemyProperty]:
        return [AbyssEnemyProperty(**prop) for prop in v]


class AbyssResponse(BaseModel):
    """
    AbyssResponse model.

    Attributes:
        enemies (dict[str, AbyssEnemy]): Dictionary of abyss enemies.
        abyss_items (list[Abyss]): list of abyss items.
    """

    enemies: dict[str, AbyssEnemy] = Field(..., alias="monsterList")
    abyss_items: list[Abyss] = Field(..., alias="items")

    @field_validator("enemies", mode="before")
    def _convert_enemies(cls, v: dict[str, dict[str, Any]]) -> dict[str, AbyssEnemy]:
        return {item_id: AbyssEnemy(**v[item_id]) for item_id in v}

    @field_validator("abyss_items", mode="before")
    def _convert_abyss_items(cls, v: dict[str, dict[str, Any]]) -> list[Abyss]:
        result: list[Abyss] = []
        for item_data in v.values():
            item_data["openTime"] = item_data["schedule"]["openTime"]
            result.append(Abyss(**item_data))
        return result
