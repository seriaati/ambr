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
    """Removes HTML tags, sprite presets, and link tags from a string.

    Args:
        text: The input string containing HTML tags.

    Returns:
        The string with HTML tags, sprite presets, and link tags removed.
    """
    clean = re.compile(r"<.*?>|\{SPRITE_PRESET#[^\}]+\}|\{/?LINK(?:#[^\}]+)?\}")
    return re.sub(clean, "", text).replace("\\n", "\n")


def replace_placeholders(string: str, params: dict[str, Any]) -> str:
    """Replaces placeholders in a string with values from a dictionary.

    Placeholders are in the format $[key].

    Args:
        string: The input string containing placeholders.
        params: A dictionary mapping placeholder keys to their values.

    Returns:
        The string with placeholders replaced and sprite presets removed.
    """
    for key, value in params.items():
        string = string.replace(f"$[{key}]", str(value))
    return re.sub(r"\{SPRITE_PRESET#[^\}]+\}", "", string)


def replace_pronouns(text: str) -> str:
    """Replaces gendered pronouns in the format {F#She}/{M#He} with She/He.

    Args:
        text: The input string containing gendered pronouns.

    Returns:
        The string with pronouns replaced.
    """
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
    """Calculates the stat values for a character or weapon at a specific level and ascension status.

    Args:
        upgrade_data: The upgrade data for the character or weapon.
        curve_data: The growth curve data.
        level: The target level.
        ascended: Whether the character/weapon is ascended at the target level.

    Returns:
        A dictionary mapping fight property IDs to their calculated values.
    """
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
    """Formats calculated stat values into strings, adding '%' for percentage stats.

    Args:
        stat_values: A dictionary mapping fight property IDs to their numerical values.

    Returns:
        A dictionary mapping fight property IDs to their formatted string values.
    """
    result: dict[str, str] = {}
    for fight_prop, value in stat_values.items():
        if fight_prop in PERCENTAGE_FIGHT_PROPS:
            result[fight_prop] = f"{round(value * 100, 1)}%"
        else:
            result[fight_prop] = str(round(value))
    return result


def format_num(digits: int, calculation: int | float) -> str:
    """Formats a number to a specified number of decimal places.

    Args:
        digits: The number of decimal places.
        calculation: The number to format.

    Returns:
        The formatted number as a string.
    """
    return f"{calculation:.{digits}f}"


def format_layout(text: str) -> str:
    """Extracts and replaces layout placeholders like {LAYOUT_MOBILE#Character Skill}.

    Args:
        text: The input string potentially containing layout placeholders.

    Returns:
        The string with layout placeholders replaced by their content.
    """
    if "LAYOUT" in text:
        brackets = re.findall(r"{LAYOUT.*?}", text)
        word_to_replace = re.findall(r"{LAYOUT.*?#(.*?)}", brackets[0])[0]
        text = text.replace("".join(brackets), word_to_replace)
    return text


def get_params(text: str, param_list: list[int | float]) -> list[str]:
    """Replaces parameter placeholders in text with formatted values from a list.

    Placeholders are in the format {param<index>:<format>}, e.g., {param1:F1P}.
    Formats include:
        F1P, F2P: Float multiplied by 100, formatted to 1 or 2 decimal places with '%'.
        F1, F2: Float formatted to 1 or 2 decimal places.
        P: Float multiplied by 100, formatted to 0 decimal places with '%'.
        I: Integer.

    Args:
        text: The input string containing parameter placeholders.
        param_list: A list of numerical parameter values.

    Returns:
        A list of strings, typically split by '|', after parameter replacement and formatting.
    """
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
    """Generates a formatted string of skill attributes from descriptions and parameters.

    Each description is processed by `get_params` and expected to return a key-value pair
    separated by '|'.

    Args:
        descriptions: A list of strings containing parameter placeholders, often separated by '|'.
        params: A list of numerical parameter values for substitution.

    Returns:
        A newline-separated string of "key: value" pairs for the skill attributes.
    """
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
    """Replaces fight property IDs (e.g., FIGHT_PROP_HP) with their human-readable names.

    Args:
        stat_values: A dictionary mapping fight property IDs to their values.
        manual_weapon: A dictionary mapping fight property IDs to their names.

    Returns:
        A dictionary mapping fight property names to their values.
    """
    result: dict[str, Any] = {}
    for fight_prop, value in stat_values.items():
        fight_prop_name = manual_weapon.get(fight_prop, fight_prop)
        result[fight_prop_name] = value
    return result
