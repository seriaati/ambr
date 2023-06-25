import re
from typing import Any, Dict


def remove_html_tags(text: str) -> str:
    clean = re.compile(r"<.*?>|\{SPRITE_PRESET#[^\}]+\}")
    return re.sub(clean, "", text)


def replace_placeholders(string: str, params: Dict[str, Any]) -> str:
    for key, value in params.items():
        string = string.replace(f"$[{key}]", str(value))
    string = re.sub(r"\{SPRITE_PRESET#[^\}]+\}", "", string)
    return string
