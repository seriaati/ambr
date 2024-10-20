from __future__ import annotations

import pytest

import ambr


async def test_book() -> None:
    async with ambr.AmbrAPI() as api:
        books = await api.fetch_books()
        for book in books:
            await api.fetch_book_detail(book.id)


async def test_character() -> None:
    async with ambr.AmbrAPI() as api:
        characters = await api.fetch_characters()
        for character in characters:
            await api.fetch_character_detail(character.id)


async def test_character_fetter() -> None:
    async with ambr.AmbrAPI() as api:
        characters = await api.fetch_characters()
        for character in characters:
            if "-" in character.id:
                continue
            await api.fetch_character_fetter(character.id)


async def test_food() -> None:
    async with ambr.AmbrAPI() as api:
        foods = await api.fetch_foods()
        for food in foods:
            await api.fetch_food_detail(food.id)


async def test_furniture() -> None:
    async with ambr.AmbrAPI() as api:
        furniture_sets = await api.fetch_furniture_sets()
        for furniture_set in furniture_sets:
            await api.fetch_furniture_set_detail(furniture_set.id)


async def test_material() -> None:
    async with ambr.AmbrAPI() as api:
        materials = await api.fetch_materials()
        for material in materials:
            await api.fetch_material_detail(material.id)


async def test_monster() -> None:
    async with ambr.AmbrAPI() as api:
        monsters = await api.fetch_monsters()
        for monster in monsters:
            await api.fetch_monster_detail(monster.id)


async def test_namecard() -> None:
    async with ambr.AmbrAPI() as api:
        namecards = await api.fetch_namecards()
        for namecard in namecards:
            await api.fetch_namecard_detail(namecard.id)


async def test_tcg_card() -> None:
    async with ambr.AmbrAPI() as api:
        tcg_cards = await api.fetch_tcg_cards()
        for tcg_card in tcg_cards:
            await api.fetch_tcg_card_detail(tcg_card.id)


async def test_weapon() -> None:
    async with ambr.AmbrAPI() as api:
        weapons = await api.fetch_weapons()
        for weapon in weapons:
            await api.fetch_weapon_detail(weapon.id)


async def test_artifact_sets() -> None:
    async with ambr.AmbrAPI() as api:
        artifact_sets = await api.fetch_artifact_sets()
        for artifact_set in artifact_sets:
            await api.fetch_artifact_set_detail(artifact_set.id)


async def test_furniture_sets() -> None:
    async with ambr.AmbrAPI() as api:
        furniture_sets = await api.fetch_furniture_sets()
        for furniture_set in furniture_sets:
            await api.fetch_furniture_set_detail(furniture_set.id)


async def test_achievement_categories() -> None:
    async with ambr.AmbrAPI() as api:
        await api.fetch_achievement_categories()


async def test_quests() -> None:
    async with ambr.AmbrAPI() as api:
        await api.fetch_quests()


async def test_domains() -> None:
    async with ambr.AmbrAPI() as api:
        await api.fetch_domains()


async def test_changelogs() -> None:
    async with ambr.AmbrAPI() as api:
        await api.fetch_changelogs()


async def test_upgrade_data() -> None:
    async with ambr.AmbrAPI() as api:
        await api.fetch_upgrade_data()


async def test_invalid_id() -> None:
    with pytest.raises(ambr.DataNotFoundError):
        async with ambr.AmbrAPI() as api:
            await api.fetch_character_detail("invalid")


async def test_abyss_data() -> None:
    async with ambr.AmbrAPI() as api:
        await api.fetch_abyss_data()
