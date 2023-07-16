import pytest

import ambr


@pytest.mark.asyncio
async def test_books():
    client = ambr.AmbrAPI()
    books = await client.fetch_books()
    for book in books:
        await client.fetch_book_detail(book.id)


@pytest.mark.asyncio
async def test_characters():
    client = ambr.AmbrAPI()
    characters = await client.fetch_characters()
    for character in characters:
        await client.fetch_character_detail(character.id)


@pytest.mark.asyncio
async def test_foods():
    client = ambr.AmbrAPI()
    foods = await client.fetch_foods()
    for food in foods:
        await client.fetch_food_detail(food.id)


@pytest.mark.asyncio
async def test_furnitures():
    client = ambr.AmbrAPI()
    furnitures = await client.fetch_furnitures()
    for furniture in furnitures:
        await client.fetch_furniture_detail(furniture.id)


@pytest.mark.asyncio
async def test_materials():
    client = ambr.AmbrAPI()
    materials = await client.fetch_materials()
    for material in materials:
        await client.fetch_material_detail(material.id)


@pytest.mark.asyncio
async def test_monsters():
    client = ambr.AmbrAPI()
    monsters = await client.fetch_monsters()
    for monster in monsters:
        await client.fetch_monster_detail(monster.id)


@pytest.mark.asyncio
async def test_name_cards():
    client = ambr.AmbrAPI()
    name_cards = await client.fetch_name_cards()
    for name_card in name_cards:
        await client.fetch_name_card_detail(name_card.id)


@pytest.mark.asyncio
async def test_quests():
    client = ambr.AmbrAPI()
    await client.fetch_quests()


@pytest.mark.asyncio
async def test_tcg_cards():
    client = ambr.AmbrAPI()
    tcg_cards = await client.fetch_tcg_cards()
    for tcg_card in tcg_cards:
        await client.fetch_tcg_card_detail(tcg_card.id)


@pytest.mark.asyncio
async def test_weapons():
    client = ambr.AmbrAPI()
    weapons = await client.fetch_weapons()
    for weapon in weapons:
        await client.fetch_weapon_detail(weapon.id)


@pytest.mark.asyncio
async def test_achievements():
    client = ambr.AmbrAPI()
    await client.fetch_achievement_categories()


@pytest.mark.asyncio
async def test_artifacts():
    client = ambr.AmbrAPI()
    artifacts = await client.fetch_artifact_sets()
    for artifact in artifacts:
        await client.fetch_artifact_set_detail(artifact.id)


@pytest.mark.asyncio
async def test_domains():
    client = ambr.AmbrAPI()
    await client.fetch_domains()


@pytest.mark.asyncio
async def test_change_log():
    client = ambr.AmbrAPI()
    await client.fetch_change_logs()


@pytest.mark.asyncio
async def test_upgrade_data():
    client = ambr.AmbrAPI()
    await client.fetch_upgrade_data()
