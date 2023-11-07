import pytest

import ambr


@pytest.fixture(scope="module")
def api_client() -> ambr.AmbrAPI:
    return ambr.AmbrAPI()


@pytest.mark.asyncio
async def test_fetch_manual_weapon(api_client: ambr.AmbrAPI):
    data = await api_client.fetch_manual_weapon()
    assert isinstance(data, dict)
