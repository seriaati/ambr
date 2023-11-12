import logging
from enum import Enum
from typing import Any, Dict, Final, List

import aiohttp
from diskcache import Cache

from .exceptions import DataNotFound
from .models import *

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


cache = Cache()


class AmbrAPI:
    BASE_URL: Final[str] = "https://api.ambr.top/v2"

    def __init__(self, lang: Language = Language.EN) -> None:
        self.lang = lang
        self.session = aiohttp.ClientSession(headers={"User-Agent": "ambr.py"})

    async def __aenter__(self) -> "AmbrAPI":
        return self

    async def __aexit__(self, exc_type, exc, tb) -> None:
        await self.close()

    @cache.memoize(expire=86400)
    async def _request(self, endpoint: str, *, static: bool = False) -> Dict[str, Any]:
        """
        A helper function to make requests to the API.

        Parameters
        ----------
        endpoint: :class:`str`
            The endpoint to request from.
        static: :class:`bool`
            Whether to use the static endpoint or not. Defaults to ``False``.

        Returns
        -------
        Dict[str, Any]
            The response from the API.
        """
        if static:
            url = f"{self.BASE_URL}/static/{endpoint}"
        else:
            url = f"{self.BASE_URL}/{self.lang.value}/{endpoint}"
        logging.debug(f"Requesting {url}...")
        async with self.session.get(url) as resp:
            data = await resp.json()
            if "code" in data and data["code"] == 404:
                raise DataNotFound(data["data"])
            return data

    async def close(self) -> None:
        """
        Closes the client session.
        """
        await self.session.close()

    async def fetch_achievement_categories(self) -> List[AchievementCategory]:
        """
        Fetches all achievement categories.

        Returns
        -------
        List[:class:`AchievementCategory`]
            The achievement categories.
        """
        data = await self._request("achievement")
        return [
            AchievementCategory(**achievement_category)
            for achievement_category in data["data"].values()
        ]

    async def fetch_artifact_sets(self) -> List[ArtifactSet]:
        """
        Fetches all artifact sets.

        Returns
        -------
        List[:class:`ArtifactSet`]
            The artifact sets.
        """
        data = await self._request("reliquary")
        return [
            ArtifactSet(**artifact_set)
            for artifact_set in data["data"]["items"].values()
        ]

    async def fetch_artifact_set_detail(self, id: int) -> ArtifactSetDetail:
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
        data = await self._request(f"reliquary/{id}")
        return ArtifactSetDetail(**data["data"])

    async def fetch_books(self) -> List[Book]:
        """
        Fetches all books.

        Returns
        -------
        List[:class:`Book`]
            The books.
        """
        data = await self._request("book")
        return [Book(**book) for book in data["data"]["items"].values()]

    async def fetch_book_detail(self, id: int) -> BookDetail:
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
        data = await self._request(f"book/{id}")
        return BookDetail(**data["data"])

    async def fetch_characters(self) -> List[Character]:
        """
        Fetches all characters.

        Returns
        -------
        List[:class:`Character`]
            The characters.
        """
        data = await self._request("avatar")
        return [Character(**character) for character in data["data"]["items"].values()]

    async def fetch_character_detail(self, id: str) -> CharacterDetail:
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
        data = await self._request(f"avatar/{id}")
        return CharacterDetail(**data["data"])

    async def fetch_foods(self) -> List[Food]:
        """
        Fetches all foods.

        Returns
        -------
        List[:class:`Food`]
            The foods.
        """
        data = await self._request("food")
        return [Food(**food) for food in data["data"]["items"].values()]

    async def fetch_food_detail(self, id: int) -> FoodDetail:
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
        data = await self._request(f"food/{id}")
        return FoodDetail(**data["data"])

    async def fetch_furnitures(self) -> List[Furniture]:
        """
        Fetches all furnitures.

        Returns
        -------
        List[:class:`Furniture`]
            The furnitures.
        """
        data = await self._request("furniture")
        return [Furniture(**furniture) for furniture in data["data"]["items"].values()]

    async def fetch_furniture_detail(self, id: int) -> FurnitureDetail:
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
        data = await self._request(f"furniture/{id}")
        return FurnitureDetail(**data["data"])

    async def fetch_materials(self) -> List[Material]:
        """
        Fetches all materials.

        Returns
        -------
        List[:class:`Material`]
            The materials.
        """
        data = await self._request("material")
        return [Material(**material) for material in data["data"]["items"].values()]

    async def fetch_material_detail(self, id: int) -> MaterialDetail:
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
        data = await self._request(f"material/{id}")
        return MaterialDetail(**data["data"])

    async def fetch_monsters(self) -> List[Monster]:
        """
        Fetches all monsters.

        Returns
        -------
        List[:class:`Monster`]
            The monsters.
        """
        data = await self._request("monster")
        return [Monster(**monster) for monster in data["data"]["items"].values()]

    async def fetch_monster_detail(self, id: int) -> MonsterDetail:
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
        data = await self._request(f"monster/{id}")
        return MonsterDetail(**data["data"])

    async def fetch_namecards(self) -> List[Namecard]:
        """
        Fetches all name cards.

        Returns
        -------
        List[:class:`NameCard`]
            The name cards.
        """
        data = await self._request("namecard")
        return [Namecard(**name_card) for name_card in data["data"]["items"].values()]

    async def fetch_namecard_detail(self, id: int) -> NamecardDetail:
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
        data = await self._request(f"namecard/{id}")
        return NamecardDetail(**data["data"])

    async def fetch_quests(self) -> List[Quest]:
        """
        Fetches all quests.

        Returns
        -------
        List[:class:`Quest`]
            The quests.
        """
        data = await self._request("quest")
        return [Quest(**quest) for quest in data["data"]["items"].values()]

    async def fetch_tcg_cards(self) -> List[TCGCard]:
        """
        Fetches all TCG cards.

        Returns
        -------
        List[:class:`TCGCard`]
            The TCG cards.
        """
        data = await self._request("gcg")
        return [TCGCard(**tcg_card) for tcg_card in data["data"]["items"].values()]

    async def fetch_tcg_card_detail(self, id: int) -> TCGCardDetail:
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
        data = await self._request(f"gcg/{id}")
        return TCGCardDetail(**data["data"])

    async def fetch_weapons(self) -> List[Weapon]:
        """
        Fetches all weapons.

        Returns
        -------
        List[:class:`Weapon`]
            The weapons.
        """
        data = await self._request("weapon")
        return [Weapon(**weapon) for weapon in data["data"]["items"].values()]

    async def fetch_weapon_types(self) -> Dict[str, str]:
        """
        Fetches all weapon types.

        Returns
        -------
        Dict[:class:`str`, :class:`str`]
            All of the weapon types.
        """
        data = await self._request("weapon")
        return data["data"]["types"]

    async def fetch_weapon_detail(self, id: int) -> WeaponDetail:
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
        data = await self._request(f"weapon/{id}")
        return WeaponDetail(**data["data"])

    async def fetch_domains(self) -> Domains:
        """
        Fetches all domains.

        Returns
        -------
        :class:`Domains`
            The domains.
        """
        data = await self._request("dailyDungeon")
        return Domains(**data["data"])

    @cache.memoize(expire=3600)
    async def fetch_change_logs(self) -> List[ChangeLog]:
        """
        Fetch change logs from the API.

        Returns
        -------
        List[ChangeLog]
            A list of ChangeLog objects.
        """
        data = await self._request("changelog", static=True)
        change_logs: List[ChangeLog] = []
        for id, log in data["data"].items():
            change_logs.append(ChangeLog(id=int(id), **log))
        return change_logs

    async def fetch_upgrade_data(self) -> UpgradeData:
        """
        Fetch upgrade data from the API.

        Returns
        -------
        UpgradeData
            The upgrade data.
        """
        data = await self._request("upgrade")
        return UpgradeData(**data["data"])

    async def fetch_manual_weapon(self) -> Dict[str, str]:
        """
        Fetch manual weapon data from the API.

        Returns
        -------
        Dict[str, str]
            The manual weapon data.
        """
        data = await self._request("manualWeapon")
        return data["data"]

    async def fetch_readable(self, id: str) -> str:
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
        data = await self._request(f"readable/{id}")
        return data["data"]

    async def fetch_avatar_curve(self) -> Dict[str, Dict[str, Dict[str, float]]]:
        """
        Fetch avatar curve from the API.

        Returns
        -------
        Dict[str, Dict[str, Dict[str, float]]]
            The avatar curve.
        """
        data = await self._request("avatarCurve", static=True)
        return data["data"]

    async def fetch_weapon_curve(self) -> Dict[str, Dict[str, Dict[str, float]]]:
        """
        Fetch weapon curve from the API.

        Returns
        -------
        Dict[str, Dict[str, Dict[str, float]]]
            The weapon curve.
        """
        data = await self._request("weaponCurve", static=True)
        return data["data"]
