from __future__ import annotations

import ambr


async def test_fetch_manual_weapon() -> None:
    async with ambr.AmbrAPI() as api:
        data = await api.fetch_manual_weapon()
        assert isinstance(data, dict)


async def test_fetch_readable() -> None:
    async with ambr.AmbrAPI() as api:
        data = await api.fetch_readable("Weapon11509")
        assert isinstance(data, str)


async def test_fetch_avatar_curve() -> None:
    async with ambr.AmbrAPI() as api:
        data = await api.fetch_avatar_curve()
        assert isinstance(data, dict)


async def test_fetch_weapon_curve() -> None:
    async with ambr.AmbrAPI() as api:
        data = await api.fetch_weapon_curve()
        assert isinstance(data, dict)


async def test_fetch_monster_curve() -> None:
    async with ambr.AmbrAPI() as api:
        data = await api.fetch_monster_curve()
        assert isinstance(data, dict)
