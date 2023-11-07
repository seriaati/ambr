import pytest

import ambr


@pytest.fixture(scope="module")
def api_client() -> ambr.AmbrAPI:
    return ambr.AmbrAPI()


@pytest.mark.asyncio
async def test_fetch_manual_weapon(api_client: ambr.AmbrAPI):
    data = await api_client.fetch_manual_weapon()
    assert isinstance(data, dict)


@pytest.mark.asyncio
async def test_fetch_readable(api_client: ambr.AmbrAPI):
    data = await api_client.fetch_readable("Weapon11509")
    assert isinstance(data, str)
