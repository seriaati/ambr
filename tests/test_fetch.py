import asyncio
from typing import TYPE_CHECKING, Any

import pytest

import ambr

if TYPE_CHECKING:
    from collections.abc import Generator


@pytest.fixture(scope="module")
def api_client() -> ambr.AmbrAPI:
    return ambr.AmbrAPI()


@pytest.fixture(scope="module")
def event_loop() -> "Generator[asyncio.AbstractEventLoop, Any, None]":
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()


@pytest.mark.asyncio
async def test_fetch_manual_weapon(api_client: ambr.AmbrAPI) -> None:
    data = await api_client.fetch_manual_weapon()
    assert isinstance(data, dict)


@pytest.mark.asyncio
async def test_fetch_readable(api_client: ambr.AmbrAPI) -> None:
    data = await api_client.fetch_readable("Weapon11509")
    assert isinstance(data, str)


@pytest.mark.asyncio
async def test_fetch_avatar_curve(api_client: ambr.AmbrAPI) -> None:
    data = await api_client.fetch_avatar_curve()
    assert isinstance(data, dict)


@pytest.mark.asyncio
async def test_fetch_weapon_curve(api_client: ambr.AmbrAPI) -> None:
    data = await api_client.fetch_weapon_curve()
    assert isinstance(data, dict)
