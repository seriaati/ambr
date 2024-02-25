import asyncio
import logging
from enum import Enum
from typing import Any, Final

import aiohttp
from diskcache import Cache

from .exceptions import DataNotFoundError
from .models import (
    AchievementCategory,
    ArtifactSet,
    ArtifactSetDetail,
    Book,
    BookDetail,
    Changelog,
    Character,
    CharacterDetail,
    CharacterFetter,
    Domains,
    Food,
    FoodDetail,
    Furniture,
    FurnitureDetail,
    Material,
    MaterialDetail,
    Monster,
    MonsterDetail,
    Namecard,
    NamecardDetail,
    Quest,
    TCGCard,
    TCGCardDetail,
    UpgradeData,
    Weapon,
    WeaponDetail,
)
from .models.furniture import FurnitureSet, FurnitureSetDetail
from .utils import remove_html_tags

__all__ = ("AmbrAPI", "Language")


class Language(Enum):
    CHT = "cht"
    CHS = "chs"
    DE = "de"
    EN = "en"
    ES = "es"
    FR = "fr"
    ID = "id"
    JP = "jp"
    KR = "kr"
    PT = "pt"
    RU = "ru"
    TH = "th"
    VI = "vi"
    IT = "it"
    TR = "tr"


LOGGER_ = logging.getLogger("ambr.py")


class AmbrAPI:
    BASE_URL: Final[str] = "https://api.ambr.top/v2"

    def __init__(self, lang: Language = Language.EN, cache_ttl: int = 3600) -> None:
        self.lang = lang
        self.cache_ttl = cache_ttl

        self.session = aiohttp.ClientSession(headers={"User-Agent": "ambr.py"})
        self.cache = Cache(".cache/ambr")

    async def __aenter__(self) -> "AmbrAPI":
        return self

    async def __aexit__(self, exc_type, exc, tb) -> None:  # noqa: ANN001
        await self.close()

    async def _request(
        self, endpoint: str, *, static: bool = False, use_cache: bool
    ) -> dict[str, Any]:
        """
        A helper function to make requests to the API.

        Parameters
        ----------
        endpoint: :class:`str`
            The endpoint to request from.
        static: :class:`bool`
            Whether to use the static endpoint or not. Defaults to ``False``.
        use_cache: :class:`bool`
            Whether to use the cache or not. Defaults to ``True``.

        Returns
        -------
        Dict[str, Any]
            The response from the API.
        """
        if static:
            url = f"{self.BASE_URL}/static/{endpoint}"
        else:
            url = f"{self.BASE_URL}/{self.lang.value}/{endpoint}"

        cache = await asyncio.to_thread(self.cache.get, url)
        if cache is not None and use_cache:
            return cache  # type: ignore

        LOGGER_.debug("Requesting %s...", url)
        async with self.session.get(url) as resp:
            data = await resp.json()
            if "code" in data and data["code"] == 404:
                raise DataNotFoundError(data["data"])
            await asyncio.to_thread(self.cache.set, url, data, expire=self.cache_ttl)
            return data

    async def close(self) -> None:
        """
        Closes the client session.
        """
        await self.session.close()
        self.cache.close()

    async def fetch_achievement_categories(
        self, use_cache: bool = True
    ) -> list[AchievementCategory]:
        """
        Fetches all achievement categories.

        Returns
        -------
        List[:class:`AchievementCategory`]
            The achievement categories.
        """
        data = await self._request("achievement", use_cache=use_cache)
        return [
            AchievementCategory(**achievement_category)
            for achievement_category in data["data"].values()
        ]

    async def fetch_artifact_sets(self, use_cache: bool = True) -> list[ArtifactSet]:
        """
        Fetches all artifact sets.

        Returns
        -------
        List[:class:`ArtifactSet`]
            The artifact sets.
        """
        data = await self._request("reliquary", use_cache=use_cache)
        return [ArtifactSet(**artifact_set) for artifact_set in data["data"]["items"].values()]

    async def fetch_artifact_set_detail(self, id: int, use_cache: bool = True) -> ArtifactSetDetail:
        """
        Fetches an artifact set detail by ID.

        Parameters
        ----------
        id: :class:`int`
            The ID of the artifact set detail to fetch.

        Returns
        -------
        :class:`ArtifactSetDetail`
            The artifact set detail.
        """
        data = await self._request(f"reliquary/{id}", use_cache=use_cache)
        return ArtifactSetDetail(**data["data"])

    async def fetch_books(self, use_cache: bool = True) -> list[Book]:
        """
        Fetches all books.

        Returns
        -------
        List[:class:`Book`]
            The books.
        """
        data = await self._request("book", use_cache=use_cache)
        return [Book(**book) for book in data["data"]["items"].values()]

    async def fetch_book_detail(self, id: int, use_cache: bool = True) -> BookDetail:
        """
        Fetches a book detail by ID.

        Parameters
        ----------
        id: :class:`int`
            The ID of the book detail to fetch.

        Returns
        -------
        :class:`BookDetail`
            The book detail.
        """
        data = await self._request(f"book/{id}", use_cache=use_cache)
        return BookDetail(**data["data"])

    async def fetch_characters(self, use_cache: bool = True) -> list[Character]:
        """
        Fetches all characters.

        Returns
        -------
        List[:class:`Character`]
            The characters.
        """
        data = await self._request("avatar", use_cache=use_cache)
        return [Character(**character) for character in data["data"]["items"].values()]

    async def fetch_character_detail(self, id: str, use_cache: bool = True) -> CharacterDetail:
        """
        Fetches a character detail by ID.

        Parameters
        ----------
        id: :class:`str`
            The ID of the character detail to fetch.

        Returns
        -------
        :class:`CharacterDetail`
            The character detail.
        """
        data = await self._request(f"avatar/{id}", use_cache=use_cache)
        return CharacterDetail(**data["data"])

    async def fetch_character_fetter(self, id: str, use_cache: bool = True) -> CharacterFetter:
        """
        Fetches a character fetter by ID.

        Parameters
        ----------
        id: :class:`str`
            The ID of the character fetter to fetch.

        Returns
        -------
        :class:`CharacterFetter`
            The character fetter.
        """
        data = await self._request(f"avatarFetter/{id}", use_cache=use_cache)
        return CharacterFetter(**data["data"])

    async def fetch_foods(self, use_cache: bool = True) -> list[Food]:
        """
        Fetches all foods.

        Returns
        -------
        List[:class:`Food`]
            The foods.
        """
        data = await self._request("food", use_cache=use_cache)
        return [Food(**food) for food in data["data"]["items"].values()]

    async def fetch_food_detail(self, id: int, use_cache: bool = True) -> FoodDetail:
        """
        Fetches a food detail by ID.

        Parameters
        ----------
        id: :class:`int`
            The ID of the food detail to fetch.

        Returns
        -------
        :class:`FoodDetail`
            The food detail.
        """
        data = await self._request(f"food/{id}", use_cache=use_cache)
        return FoodDetail(**data["data"])

    async def fetch_furnitures(self, use_cache: bool = True) -> list[Furniture]:
        """
        Fetches all furnitures.

        Returns
        -------
        List[:class:`Furniture`]
            The furnitures.
        """
        data = await self._request("furniture", use_cache=use_cache)
        return [Furniture(**furniture) for furniture in data["data"]["items"].values()]

    async def fetch_furniture_detail(self, id: int, use_cache: bool = True) -> FurnitureDetail:
        """
        Fetches a furniture detail by ID.

        Parameters
        ----------
        id: :class:`int`
            The ID of the furniture detail to fetch.

        Returns
        -------
        :class:`FurnitureDetail`
            The furniture detail.
        """
        data = await self._request(f"furniture/{id}", use_cache=use_cache)
        return FurnitureDetail(**data["data"])

    async def fetch_furniture_sets(self, use_cache: bool = True) -> list[FurnitureSet]:
        """
        Fetches all furniture sets.

        Returns
        -------
        List[:class:`FurnitureSet`]
            The furniture sets.
        """
        data = await self._request("furnitureSuite", use_cache=use_cache)
        return [FurnitureSet(**furniture_set) for furniture_set in data["data"]["items"].values()]

    async def fetch_furniture_set_detail(
        self, id: int, use_cache: bool = True
    ) -> FurnitureSetDetail:
        """
        Fetches a furniture set detail by ID.

        Parameters
        ----------
        id: :class:`int`
            The ID of the furniture set detail to fetch.

        Returns
        -------
        :class:`FurnitureSetDetail`
            The furniture set detail.
        """
        data = await self._request(f"furnitureSuite/{id}", use_cache=use_cache)
        return FurnitureSetDetail(**data["data"])

    async def fetch_materials(self, use_cache: bool = True) -> list[Material]:
        """
        Fetches all materials.

        Returns
        -------
        List[:class:`Material`]
            The materials.
        """
        data = await self._request("material", use_cache=use_cache)
        return [Material(**material) for material in data["data"]["items"].values()]

    async def fetch_material_detail(self, id: int, use_cache: bool = True) -> MaterialDetail:
        """
        Fetches a material detail by ID.

        Parameters
        ----------
        id: :class:`int`
            The ID of the material detail to fetch.

        Returns
        -------
        :class:`MaterialDetail`
            The material detail.
        """
        data = await self._request(f"material/{id}", use_cache=use_cache)
        return MaterialDetail(**data["data"])

    async def fetch_monsters(self, use_cache: bool = True) -> list[Monster]:
        """
        Fetches all monsters.

        Returns
        -------
        List[:class:`Monster`]
            The monsters.
        """
        data = await self._request("monster", use_cache=use_cache)
        return [Monster(**monster) for monster in data["data"]["items"].values()]

    async def fetch_monster_detail(self, id: int, use_cache: bool = True) -> MonsterDetail:
        """
        Fetches a monster detail by ID.

        Parameters
        ----------
        id: :class:`int`
            The ID of the monster detail to fetch.

        Returns
        -------
        :class:`MonsterDetail`
            The monster detail.
        """
        data = await self._request(f"monster/{id}", use_cache=use_cache)
        return MonsterDetail(**data["data"])

    async def fetch_namecards(self, use_cache: bool = True) -> list[Namecard]:
        """
        Fetches all name cards.

        Returns
        -------
        List[:class:`NameCard`]
            The name cards.
        """
        data = await self._request("namecard", use_cache=use_cache)
        return [Namecard(**name_card) for name_card in data["data"]["items"].values()]

    async def fetch_namecard_detail(self, id: int, use_cache: bool = True) -> NamecardDetail:
        """
        Fetches a name card detail by ID.

        Parameters
        ----------
        id: :class:`int`
            The ID of the name card detail to fetch.

        Returns
        -------
        :class:`NameCardDetail`
            The name card detail.
        """
        data = await self._request(f"namecard/{id}", use_cache=use_cache)
        return NamecardDetail(**data["data"])

    async def fetch_quests(self, use_cache: bool = True) -> list[Quest]:
        """
        Fetches all quests.

        Returns
        -------
        List[:class:`Quest`]
            The quests.
        """
        data = await self._request("quest", use_cache=use_cache)
        return [Quest(**quest) for quest in data["data"]["items"].values()]

    async def fetch_tcg_cards(self, use_cache: bool = True) -> list[TCGCard]:
        """
        Fetches all TCG cards.

        Returns
        -------
        List[:class:`TCGCard`]
            The TCG cards.
        """
        data = await self._request("gcg", use_cache=use_cache)
        return [TCGCard(**tcg_card) for tcg_card in data["data"]["items"].values()]

    async def fetch_tcg_card_detail(self, id: int, use_cache: bool = True) -> TCGCardDetail:
        """
        Fetches a TCG card detail by ID.

        Parameters
        ----------
        id: :class:`int`
            The ID of the TCG card detail to fetch.

        Returns
        -------
        :class:`TCGCardDetail`
            The TCG card detail.
        """
        data = await self._request(f"gcg/{id}", use_cache=use_cache)
        return TCGCardDetail(**data["data"])

    async def fetch_weapons(self, use_cache: bool = True) -> list[Weapon]:
        """
        Fetches all weapons.

        Returns
        -------
        List[:class:`Weapon`]
            The weapons.
        """
        data = await self._request("weapon", use_cache=use_cache)
        return [Weapon(**weapon) for weapon in data["data"]["items"].values()]

    async def fetch_weapon_types(self, use_cache: bool = True) -> dict[str, str]:
        """
        Fetches all weapon types.

        Returns
        -------
        Dict[:class:`str`, :class:`str`]
            All of the weapon types.
        """
        data = await self._request("weapon", use_cache=use_cache)
        return data["data"]["types"]

    async def fetch_weapon_detail(self, id: int, use_cache: bool = True) -> WeaponDetail:
        """
        Fetches a weapon detail by ID.

        Parameters
        ----------
        id: :class:`int`
            The ID of the weapon detail to fetch.

        Returns
        -------
        :class:`WeaponDetail`
            The weapon detail.
        """
        data = await self._request(f"weapon/{id}", use_cache=use_cache)
        return WeaponDetail(**data["data"])

    async def fetch_domains(self, use_cache: bool = True) -> Domains:
        """
        Fetches all domains.

        Returns
        -------
        :class:`Domains`
            The domains.
        """
        data = await self._request("dailyDungeon", use_cache=use_cache)
        return Domains(**data["data"])

    async def fetch_changelogs(self, use_cache: bool = True) -> list[Changelog]:
        """
        Fetch changelogs from the API.

        Returns
        -------
        List[Changelog]
            A list of Changelog objects.
        """
        data = await self._request("changelog", static=True, use_cache=use_cache)
        changelogs: list[Changelog] = []
        for changelog_id, log in data["data"].items():
            changelogs.append(Changelog(id=int(changelog_id), **log))
        return changelogs

    async def fetch_upgrade_data(self, use_cache: bool = True) -> UpgradeData:
        """
        Fetch upgrade data from the API.

        Returns
        -------
        UpgradeData
            The upgrade data.
        """
        data = await self._request("upgrade", use_cache=use_cache)
        return UpgradeData(**data["data"])

    async def fetch_manual_weapon(self, use_cache: bool = True) -> dict[str, str]:
        """
        Fetch manual weapon data from the API.

        Returns
        -------
        Dict[str, str]
            The manual weapon data.
        """
        data = await self._request("manualWeapon", use_cache=use_cache)
        return data["data"]

    async def fetch_readable(self, id: str, use_cache: bool = True) -> str:
        """
        Fetch a readable from the API.

        Parameters
        ----------
        id: :class:`str`
            The ID of the readable to fetch.

        Returns
        -------
        :class:`str`
            The readable.
        """
        data = await self._request(f"readable/{id}", use_cache=use_cache)
        return remove_html_tags(data["data"])

    async def fetch_avatar_curve(
        self, use_cache: bool = True
    ) -> dict[str, dict[str, dict[str, float]]]:
        """
        Fetch avatar curve from the API.

        Returns
        -------
        Dict[str, Dict[str, Dict[str, float]]]
            The avatar curve.
        """
        data = await self._request("avatarCurve", static=True, use_cache=use_cache)
        return data["data"]

    async def fetch_weapon_curve(
        self, use_cache: bool = True
    ) -> dict[str, dict[str, dict[str, float]]]:
        """
        Fetch weapon curve from the API.

        Returns
        -------
        Dict[str, Dict[str, Dict[str, float]]]
            The weapon curve.
        """
        data = await self._request("weaponCurve", static=True, use_cache=use_cache)
        return data["data"]
