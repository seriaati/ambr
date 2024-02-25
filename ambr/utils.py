import re
from typing import Any


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
