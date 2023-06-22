from enum import Enum
from typing import Any, Dict, Final, List

import aiohttp

from .models import (
    Achievement,
    Artifact,
    Book,
    Character,
    Food,
    Furniture,
    Material,
    Monster,
    NameCard,
    Quest,
    TCGCard,
    Weapon,
)


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


class AmbrAPI:
    BASE_URL: Final[str] = "https://api.ambr.top/v2"

    def __init__(self, lang: Language = Language.EN) -> None:
        self.lang = lang

    async def _request(self, endpoint: str) -> Dict[str, Any]:
        """
        A helper function to make requests to the API.

        Parameters
        ----------
        endpoint: :class:`str`
            The endpoint to request from.

        Returns
        -------
        Dict[str, Any]
            The response from the API.
        """
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"{self.BASE_URL}/{self.lang.value}/{endpoint}"
            ) as resp:
                return await resp.json()

    async def fetch_achievements(self) -> List[Achievement]:
        """
        Fetches all achievements.

        Returns
        -------
        List[:class:`Achievement`]
            The achievements.
        """
        data = await self._request("achievement")
        return [Achievement(**achievement) for achievement in data["data"]["items"]]

    async def fetch_artifacts(self) -> List[Artifact]:
        """
        Fetches all artifacts.

        Returns
        -------
        List[:class:`Artifact`]
            The artifacts.
        """
        data = await self._request("reliquary")
        return [Artifact(**artifact) for artifact in data["data"]["items"]]

    async def fetch_books(self) -> List[Book]:
        """
        Fetches all books.

        Returns
        -------
        List[:class:`Book`]
            The books.
        """
        data = await self._request("book")
        return [Book(**book) for book in data["data"]["items"]]

    async def fetch_characters(self) -> List[Character]:
        """
        Fetches all characters.

        Returns
        -------
        List[:class:`Character`]
            The characters.
        """
        data = await self._request("character")
        return [Character(**character) for character in data["data"]["items"]]

    async def fetch_foods(self) -> List[Food]:
        """
        Fetches all foods.

        Returns
        -------
        List[:class:`Food`]
            The foods.
        """
        data = await self._request("food")
        return [Food(**food) for food in data["data"]["items"]]

    async def fetch_furnitures(self) -> List[Furniture]:
        """
        Fetches all furnitures.

        Returns
        -------
        List[:class:`Furniture`]
            The furnitures.
        """
        data = await self._request("furniture")
        return [Furniture(**furniture) for furniture in data["data"]["items"]]

    async def fetch_materials(self) -> List[Material]:
        """
        Fetches all materials.

        Returns
        -------
        List[:class:`Material`]
            The materials.
        """
        data = await self._request("material")
        return [Material(**material) for material in data["data"]["items"]]

    async def fetch_monsters(self) -> List[Monster]:
        """
        Fetches all monsters.

        Returns
        -------
        List[:class:`Monster`]
            The monsters.
        """
        data = await self._request("monster")
        return [Monster(**monster) for monster in data["data"]["items"]]

    async def fetch_namecards(self) -> List[NameCard]:
        """
        Fetches all name cards.

        Returns
        -------
        List[:class:`NameCard`]
            The name cards.
        """
        data = await self._request("namecard")
        return [NameCard(**namecard) for namecard in data["data"]["items"]]

    async def fetch_quests(self) -> List[Quest]:
        """
        Fetches all quests.

        Returns
        -------
        List[:class:`Quest`]
            The quests.
        """
        data = await self._request("quest")
        return [Quest(**quest) for quest in data["data"]["items"]]

    async def fetch_tcgcards(self) -> List[TCGCard]:
        """
        Fetches all TCG cards.

        Returns
        -------
        List[:class:`TCGCard`]
            The TCG cards.
        """
        data = await self._request("gcg")
        return [TCGCard(**tcgcard) for tcgcard in data["data"]["items"]]

    async def fetch_weapons(self) -> List[Weapon]:
        """
        Fetches all weapons.

        Returns
        -------
        List[:class:`Weapon`]
            The weapons.
        """
        data = await self._request("weapon")
        return [Weapon(**weapon) for weapon in data["data"]["items"]]
