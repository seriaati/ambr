from __future__ import annotations

import ambr


async def test_fetch_books() -> None:
    async with ambr.AmbrAPI() as api:
        await api.fetch_books()


async def test_fetch_characters() -> None:
    async with ambr.AmbrAPI() as api:
        await api.fetch_characters()


async def test_fetch_foods() -> None:
    async with ambr.AmbrAPI() as api:
        await api.fetch_foods()


async def test_fetch_furniture_sets() -> None:
    async with ambr.AmbrAPI() as api:
        await api.fetch_furniture_sets()


async def test_fetch_materials() -> None:
    async with ambr.AmbrAPI() as api:
        await api.fetch_materials()


async def test_fetch_monsters() -> None:
    async with ambr.AmbrAPI() as api:
        await api.fetch_monsters()


async def test_fetch_namecards() -> None:
    async with ambr.AmbrAPI() as api:
        await api.fetch_namecards()


async def test_fetch_tcg_cards() -> None:
    async with ambr.AmbrAPI() as api:
        await api.fetch_tcg_cards()


async def test_fetch_weapons() -> None:
    async with ambr.AmbrAPI() as api:
        await api.fetch_weapons()


async def test_fetch_artifact_sets() -> None:
    async with ambr.AmbrAPI() as api:
        await api.fetch_artifact_sets()


async def test_fetch_achievement_categories() -> None:
    async with ambr.AmbrAPI() as api:
        await api.fetch_achievement_categories()


async def test_fetch_quests() -> None:
    async with ambr.AmbrAPI() as api:
        await api.fetch_quests()


async def test_fetch_domains() -> None:
    async with ambr.AmbrAPI() as api:
        await api.fetch_domains()


async def test_fetch_changelogs() -> None:
    async with ambr.AmbrAPI() as api:
        await api.fetch_changelogs()


async def test_fetch_upgrade_data() -> None:
    async with ambr.AmbrAPI() as api:
        await api.fetch_upgrade_data()


async def test_fetch_abyss_data() -> None:
    async with ambr.AmbrAPI() as api:
        await api.fetch_abyss_data()
