from __future__ import annotations

import pytest

import ambr


@pytest.mark.parametrize("lang", list(ambr.Language))
async def test_languages(lang: ambr.Language) -> None:
    async with ambr.AmbrAPI(lang=lang) as client:
        await client.fetch_characters()
