from __future__ import annotations

import re
from collections import defaultdict
from typing import TYPE_CHECKING, Any

from .constants import PERCENTAGE_FIGHT_PROPS

if TYPE_CHECKING:
    import ambr

__all__ = (
    "calculate_upgrade_stat_values",
    "format_layout",
    "format_num",
    "format_stat_values",
    "get_params",
    "get_skill_attributes",
    "remove_html_tags",
    "replace_fight_prop_with_name",
    "replace_placeholders",
    "replace_pronouns",
)


def remove_html_tags(text: str) -> str:
    clean = re.compile(r"<.*?>|\{SPRITE_PRESET#[^\}]+\}")
    return re.sub(clean, "", text).replace("\\n", "\n")


def replace_placeholders(string: str, params: dict[str, Any]) -> str:
    for key, value in params.items():
        string = string.replace(f"$[{key}]", str(value))
    string = re.sub(r"\{SPRITE_PRESET#[^\}]+\}", "", string)
    return string


def replace_pronouns(text: str) -> str:
    female_pronoun_pattern = r"\{F#(.*?)\}"
    male_pronoun_pattern = r"\{M#(.*?)\}"

    female_pronoun_match = re.search(female_pronoun_pattern, text)
    male_pronoun_match = re.search(male_pronoun_pattern, text)

    if female_pronoun_match and male_pronoun_match:
        female_pronoun = female_pronoun_match.group(1)
        male_pronoun = male_pronoun_match.group(1)
        replacement = f"{female_pronoun}/{male_pronoun}"

        text = re.sub(female_pronoun_pattern, replacement, text)
        text = re.sub(male_pronoun_pattern, "", text)
        text = text.replace("#", "")

    return text


def calculate_upgrade_stat_values(
    upgrade_data: ambr.CharacterUpgrade | ambr.WeaponUpgrade,
    curve_data: dict[str, dict[str, dict[str, float]]],
    level: int,
    ascended: bool,
) -> dict[str, float]:
    result: defaultdict[str, float] = defaultdict(float)

    for stat in upgrade_data.base_stats:
        if stat.prop_type is None:
            continue
        result[stat.prop_type] = (
            stat.init_value * curve_data[str(level)]["curveInfos"][stat.growth_type]
        )

    for promote in reversed(upgrade_data.promotes):
        if promote.add_stats is None:
            continue
        if (level == promote.unlock_max_level and ascended) or level > promote.unlock_max_level:
            for stat in promote.add_stats:
                if stat.value != 0:
                    result[stat.id] += stat.value
                    if stat.id in {"FIGHT_PROP_CRITICAL_HURT", "FIGHT_PROP_CRITICAL"}:
                        result[stat.id] += 0.5
            break

    return result


def format_stat_values(stat_values: dict[str, float]) -> dict[str, str]:
    result: dict[str, str] = {}
    for fight_prop, value in stat_values.items():
        if fight_prop in PERCENTAGE_FIGHT_PROPS:
            result[fight_prop] = f"{round(value * 100, 1)}%"
        else:
            result[fight_prop] = str(round(value))
    return result


def format_num(digits: int, calculation: int | float) -> str:
    return f"{calculation:.{digits}f}"


def format_layout(text: str) -> str:
    if "LAYOUT" in text:
        brackets = re.findall(r"{LAYOUT.*?}", text)
        word_to_replace = re.findall(r"{LAYOUT.*?#(.*?)}", brackets[0])[0]
        text = text.replace("".join(brackets), word_to_replace)
    return text


def get_params(text: str, param_list: list[int | float]) -> list[str]:
    params: list[str] = re.findall(r"{[^}]*}", text)

    for item in params:
        if "param" not in item:
            continue

        param_text = re.findall(r"{param(\d+):([^}]*)}", item)[0]
        param, value = param_text

        if value in {"F1P", "F2P"}:
            result = format_num(int(value[1]), param_list[int(param) - 1] * 100)
            text = re.sub(re.escape(item), f"{result}%", text)
        elif value in {"F1", "F2"}:
            result = format_num(int(value[1]), param_list[int(param) - 1])
            text = re.sub(re.escape(item), result, text)
        elif value == "P":
            result = format_num(0, param_list[int(param) - 1] * 100)
            text = re.sub(re.escape(item), f"{result}%", text)
        elif value == "I":
            result = int(param_list[int(param) - 1])
            text = re.sub(re.escape(item), str(round(result)), text)

    text = format_layout(text)
    text = text.replace("{NON_BREAK_SPACE}", "")
    text = text.replace("#", "")
    return text.split("|")


def get_skill_attributes(descriptions: list[str], params: list[int | float]) -> str:
    result = ""
    for desc in descriptions:
        try:
            k, v = get_params(desc, params)
        except ValueError:
            continue
        result += f"{k}: {v}\n"
    return result


def replace_fight_prop_with_name(
    stat_values: dict[str, Any], manual_weapon: dict[str, str]
) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for fight_prop, value in stat_values.items():
        fight_prop_name = manual_weapon.get(fight_prop, fight_prop)
        result[fight_prop_name] = value
    return result
