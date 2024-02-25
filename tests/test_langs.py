import pytest

import ambr


@pytest.mark.asyncio
async def test_languages() -> None:
    client = ambr.AmbrAPI()
    for lang in ambr.Language:
        client.lang = lang
        await client.fetch_characters()
