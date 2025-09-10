from __future__ import annotations

from typing import Self

import pydantic

from ambr.utils import remove_html_tags

REMOVE_HTML_TAG_FIELD_NAMES = {"description", "desc", "name", "title"}


class BaseModel(pydantic.BaseModel):
    model_config = {"coerce_numbers_to_str": True}

    @pydantic.model_validator(mode="after")
    def __remove_html_tags(self) -> Self:
        for field in self.__class__.model_fields:
            if field in REMOVE_HTML_TAG_FIELD_NAMES and isinstance(getattr(self, field), str):
                setattr(self, field, remove_html_tags(getattr(self, field)))
        return self
