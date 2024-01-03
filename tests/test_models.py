import asyncio
import contextlib
from typing import Any, Awaitable, Callable, List, Union

import pytest
import pytest_asyncio

import ambr


async def fetch_ids(
    fetch_func: Callable[[], Awaitable[List[Any]]],
) -> List[Union[int, str]]:
    items = await fetch_func()
    return [item.id for item in items]


@pytest.fixture(scope="module")
def api_client() -> ambr.AmbrAPI:
    return ambr.AmbrAPI()


@pytest.fixture(scope="module")
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="module")
async def _fetch_ids(api_client: ambr.AmbrAPI) -> List[List[Union[int, str]]]:
    fetch_funcs = [
        api_client.fetch_books,
        api_client.fetch_characters,
        api_client.fetch_foods,
        api_client.fetch_furnitures,
        api_client.fetch_materials,
        api_client.fetch_monsters,
        api_client.fetch_namecards,
        api_client.fetch_tcg_cards,
        api_client.fetch_weapons,
        api_client.fetch_artifact_sets,
        api_client.fetch_furniture_sets,
    ]
    ids = await asyncio.gather(*(fetch_ids(func) for func in fetch_funcs))
    return ids


@pytest.mark.asyncio
async def test_book(api_client: ambr.AmbrAPI, _fetch_ids):
    book_ids = _fetch_ids[0]
    for book_id in book_ids:
        await api_client.fetch_book_detail(book_id)


@pytest.mark.asyncio
async def test_character(api_client: ambr.AmbrAPI, _fetch_ids):
    character_ids = _fetch_ids[1]
    for character_id in character_ids:
        await api_client.fetch_character_detail(character_id)


@pytest.mark.asyncio
async def test_character_fetter(api_client: ambr.AmbrAPI, _fetch_ids):
    character_ids = _fetch_ids[1]
    for character_id in character_ids:
        with contextlib.suppress(ambr.DataNotFound):
            await api_client.fetch_character_fetter(character_id)


@pytest.mark.asyncio
async def test_food(api_client: ambr.AmbrAPI, _fetch_ids):
    food_ids = _fetch_ids[2]
    for food_id in food_ids:
        await api_client.fetch_food_detail(food_id)


@pytest.mark.asyncio
async def test_furniture(api_client: ambr.AmbrAPI, _fetch_ids):
    furniture_ids = _fetch_ids[3]
    for furniture_id in furniture_ids:
        await api_client.fetch_furniture_detail(furniture_id)


@pytest.mark.asyncio
async def test_material(api_client: ambr.AmbrAPI, _fetch_ids):
    material_ids = _fetch_ids[4]
    for material_id in material_ids:
        await api_client.fetch_material_detail(material_id)


@pytest.mark.asyncio
async def test_monster(api_client: ambr.AmbrAPI, _fetch_ids):
    monster_ids = _fetch_ids[5]
    for monster_id in monster_ids:
        await api_client.fetch_monster_detail(monster_id)


@pytest.mark.asyncio
async def test_name_card(api_client: ambr.AmbrAPI, _fetch_ids):
    name_card_ids = _fetch_ids[6]
    for name_card_id in name_card_ids:
        await api_client.fetch_namecard_detail(name_card_id)


@pytest.mark.asyncio
async def test_tcg_card(api_client: ambr.AmbrAPI, _fetch_ids):
    tcg_card_ids = _fetch_ids[7]
    for tcg_card_id in tcg_card_ids:
        await api_client.fetch_tcg_card_detail(tcg_card_id)


@pytest.mark.asyncio
async def test_weapon(api_client: ambr.AmbrAPI, _fetch_ids):
    weapon_ids = _fetch_ids[8]
    for weapon_id in weapon_ids:
        await api_client.fetch_weapon_detail(weapon_id)


@pytest.mark.asyncio
async def test_artifact_sets(api_client: ambr.AmbrAPI, _fetch_ids):
    artifact_ids = _fetch_ids[9]
    for artifact_id in artifact_ids:
        await api_client.fetch_artifact_set_detail(artifact_id)


@pytest.mark.asyncio
async def test_furniture_sets(api_client: ambr.AmbrAPI, _fetch_ids):
    furniture_ids = _fetch_ids[10]
    for furniture_id in furniture_ids:
        await api_client.fetch_furniture_set_detail(furniture_id)


@pytest.mark.asyncio
async def test_achievement_categories():
    client = ambr.AmbrAPI()
    await client.fetch_achievement_categories()


@pytest.mark.asyncio
async def test_quests(api_client: ambr.AmbrAPI):
    await api_client.fetch_quests()


@pytest.mark.asyncio
async def test_domains(api_client: ambr.AmbrAPI):
    await api_client.fetch_domains()


@pytest.mark.asyncio
async def test_change_logs(api_client: ambr.AmbrAPI):
    await api_client.fetch_change_logs()


@pytest.mark.asyncio
async def test_upgrade_data(api_client: ambr.AmbrAPI):
    await api_client.fetch_upgrade_data()


@pytest.mark.asyncio
async def test_invalid_id(api_client: ambr.AmbrAPI):
    with pytest.raises(ambr.DataNotFound):
        await api_client.fetch_character_detail("invalid")
