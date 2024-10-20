from __future__ import annotations

import ambr


async def test_languages() -> None:
    async with ambr.AmbrAPI() as client:
        for lang in ambr.Language:
            client.lang = lang
            await client.fetch_characters()
