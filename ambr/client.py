from __future__ import annotations

import time
from enum import Enum
from typing import TYPE_CHECKING, Any, Final, Self

import aiofiles
from aiohttp_client_cache.backends.sqlite import SQLiteBackend
from aiohttp_client_cache.session import CachedSession
from loguru import logger

from .constants import CACHE_PATH
from .exceptions import AmbrAPIError, ConnectionTimeoutError, DataNotFoundError
from .models import (
    AbyssResponse,
    AchievementCategory,
    ArtifactSet,
    ArtifactSetDetail,
    Book,
    BookDetail,
    Changelog,
    Character,
    CharacterDetail,
    CharacterFetter,
    CharacterGuide,
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

if TYPE_CHECKING:
    import aiohttp

__all__ = ("AmbrAPI", "Language")


class Language(Enum):
    """Supported languages for the API data."""

    CHT = "cht"
    """Traditional Chinese."""
    CHS = "chs"
    """Simplified Chinese."""
    DE = "de"
    """German."""
    EN = "en"
    """English."""
    ES = "es"
    """Spanish."""
    FR = "fr"
    """French."""
    ID = "id"
    """Indonesian."""
    JP = "jp"
    """Japanese."""
    KR = "kr"
    """Korean."""
    PT = "pt"
    """Portuguese."""
    RU = "ru"
    """Russian."""
    TH = "th"
    """Thai."""
    VI = "vi"
    """Vietnamese."""
    IT = "it"
    """Italian."""
    TR = "tr"
    """Turkish."""


class AmbrAPI:  # noqa: PLR0904
    """Asynchronous client for interacting with the Ambr project API (gi.yatta.moe).

    Provides methods to fetch various Genshin Impact game data.

    Args:
        lang: The language for the API responses. Defaults to English (EN).
        cache_ttl: Time-to-live for cached responses in seconds. Defaults to 3600 (1 hour).
        headers: Optional custom headers for HTTP requests.
        session: Optional existing aiohttp.ClientSession to use. If None, a new CachedSession is created.

    Attributes:
        lang: The language used for API requests.
        BASE_URL: The base URL for the Ambr API v2.
    """

    BASE_URL: Final[str] = "https://gi.yatta.moe/api/v2"

    def __init__(
        self,
        *,
        lang: Language = Language.EN,
        cache_ttl: int = 3600,
        headers: dict[str, Any] | None = None,
        session: aiohttp.ClientSession | None = None,
    ) -> None:
        self.lang = lang
        self._cache_ttl = cache_ttl

        self._session = session
        self._headers = headers or {"User-Agent": "ambr-py"}

    async def __aenter__(self) -> Self:
        await self.start()
        return self

    async def __aexit__(self, exc_type, exc, tb) -> None:  # noqa: ANN001
        await self.close()

    async def _request(
        self, endpoint: str, *, static: bool = False, use_cache: bool
    ) -> dict[str, Any]:
        if self._session is None:
            msg = f"Call `{self.__class__.__name__}.start()` before making requests."
            raise RuntimeError(msg)

        if static:
            url = f"{self.BASE_URL}/static/{endpoint}"
        else:
            url = f"{self.BASE_URL}/{self.lang.value}/{endpoint}"

        if endpoint != "version":
            version = await self._get_version()
            if version is None:
                logger.debug("Version not found or outdated, fetching latest version.")
                version = await self.fetch_latest_version()
                await self._save_version(version)
            url += f"?vh={version}"

        logger.debug(f"Requesting {url}")

        if not use_cache and isinstance(self._session, CachedSession):
            async with self._session.disabled(), self._session.get(url) as resp:
                if resp.status != 200:
                    self._handle_error(resp.status)
                data = await resp.json()
        else:
            async with self._session.get(url) as resp:
                if resp.status != 200:
                    self._handle_error(resp.status)
                data = await resp.json()

        return data

    def _handle_error(self, code: int) -> None:
        match code:
            case 404:
                raise DataNotFoundError
            case 522 | 524:
                raise ConnectionTimeoutError
            case _:
                raise AmbrAPIError(code)

    async def start(self) -> None:
        """Initializes the internal aiohttp client session.

        Must be called before making any API requests if not using the client
        as an async context manager. Creates a CachedSession if no
        session was provided during initialization.
        """
        self._session = self._session or CachedSession(
            headers=self._headers,
            cache=SQLiteBackend("./.cache/ambr/aiohttp-cache.db", expire_after=self._cache_ttl),
        )

    async def close(self) -> None:
        """Closes the internal aiohttp client session.

        Should be called to gracefully shut down the session if not using
        the client as an async context manager.
        """
        if self._session is not None:
            await self._session.close()

    async def fetch_achievement_categories(
        self, use_cache: bool = True
    ) -> list[AchievementCategory]:
        """Fetches all achievement categories.

        Args:
            use_cache: Whether to use cached data if available. Defaults to True.

        Returns:
            A list of AchievementCategory objects.

        Raises:
            DataNotFoundError: If the requested data is not found (404).
            ConnectionTimeoutError: If the connection times out (522, 524).
            AmbrAPIError: For other API-related errors.
        """
        data = await self._request("achievement", use_cache=use_cache)
        return [
            AchievementCategory(**achievement_category)
            for achievement_category in data["data"].values()
        ]

    async def fetch_artifact_sets(self, use_cache: bool = True) -> list[ArtifactSet]:
        """Fetches summary information for all artifact sets.

        Args:
            use_cache: Whether to use cached data if available. Defaults to True.

        Returns:
            A list of ArtifactSet objects.

        Raises:
            DataNotFoundError: If the requested data is not found (404).
            ConnectionTimeoutError: If the connection times out (522, 524).
            AmbrAPIError: For other API-related errors.
        """
        data = await self._request("reliquary", use_cache=use_cache)
        return [ArtifactSet(**artifact_set) for artifact_set in data["data"]["items"].values()]

    async def fetch_artifact_set_detail(self, id: int, use_cache: bool = True) -> ArtifactSetDetail:
        """Fetches detailed information for a specific artifact set by its ID.

        Args:
            id: The ID of the artifact set to fetch.
            use_cache: Whether to use cached data if available. Defaults to True.

        Returns:
            An ArtifactSetDetail object.

        Raises:
            DataNotFoundError: If the requested data is not found (404).
            ConnectionTimeoutError: If the connection times out (522, 524).
            AmbrAPIError: For other API-related errors.
        """
        data = await self._request(f"reliquary/{id}", use_cache=use_cache)
        return ArtifactSetDetail(**data["data"])

    async def fetch_books(self, use_cache: bool = True) -> list[Book]:
        """Fetches summary information for all readable books.

        Args:
            use_cache: Whether to use cached data if available. Defaults to True.

        Returns:
            A list of Book objects.

        Raises:
            DataNotFoundError: If the requested data is not found (404).
            ConnectionTimeoutError: If the connection times out (522, 524).
            AmbrAPIError: For other API-related errors.
        """
        data = await self._request("book", use_cache=use_cache)
        return [Book(**book) for book in data["data"]["items"].values()]

    async def fetch_book_detail(self, id: int, use_cache: bool = True) -> BookDetail:
        """Fetches detailed information for a specific book by its ID, including volumes.

        Args:
            id: The ID of the book to fetch.
            use_cache: Whether to use cached data if available. Defaults to True.

        Returns:
            A BookDetail object.

        Raises:
            DataNotFoundError: If the requested data is not found (404).
            ConnectionTimeoutError: If the connection times out (522, 524).
            AmbrAPIError: For other API-related errors.
        """
        data = await self._request(f"book/{id}", use_cache=use_cache)
        return BookDetail(**data["data"])

    async def fetch_characters(self, use_cache: bool = True) -> list[Character]:
        """Fetches summary information for all characters.

        Args:
            use_cache: Whether to use cached data if available. Defaults to True.

        Returns:
            A list of Character objects.

        Raises:
            DataNotFoundError: If the requested data is not found (404).
            ConnectionTimeoutError: If the connection times out (522, 524).
            AmbrAPIError: For other API-related errors.
        """
        data = await self._request("avatar", use_cache=use_cache)
        return [Character(**character) for character in data["data"]["items"].values()]

    async def fetch_character_detail(self, id: str, use_cache: bool = True) -> CharacterDetail:
        """Fetches detailed information for a specific character by their ID.

        Args:
            id: The ID of the character to fetch (e.g., "10000002" for Ayaka).
            use_cache: Whether to use cached data if available. Defaults to True.

        Returns:
            A CharacterDetail object.

        Raises:
            DataNotFoundError: If the requested data is not found (404).
            ConnectionTimeoutError: If the connection times out (522, 524).
            AmbrAPIError: For other API-related errors.
        """
        data = await self._request(f"avatar/{id}", use_cache=use_cache)
        return CharacterDetail(**data["data"])

    async def fetch_character_fetter(self, id: str, use_cache: bool = True) -> CharacterFetter:
        """Fetches character stories and voice-over quotes (fetter information) by character ID.

        Args:
            id: The ID of the character to fetch fetter data for.
            use_cache: Whether to use cached data if available. Defaults to True.

        Returns:
            A CharacterFetter object.

        Raises:
            DataNotFoundError: If the requested data is not found (404).
            ConnectionTimeoutError: If the connection times out (522, 524).
            AmbrAPIError: For other API-related errors.
        """
        data = await self._request(f"avatarFetter/{id}", use_cache=use_cache)
        return CharacterFetter(**data["data"])

    async def fetch_foods(self, use_cache: bool = True) -> list[Food]:
        """Fetches summary information for all food items.

        Args:
            use_cache: Whether to use cached data if available. Defaults to True.

        Returns:
            A list of Food objects.

        Raises:
            DataNotFoundError: If the requested data is not found (404).
            ConnectionTimeoutError: If the connection times out (522, 524).
            AmbrAPIError: For other API-related errors.
        """
        data = await self._request("food", use_cache=use_cache)
        return [Food(**food) for food in data["data"]["items"].values()]

    async def fetch_food_detail(self, id: int, use_cache: bool = True) -> FoodDetail:
        """Fetches detailed information for a specific food item by its ID.

        Args:
            id: The ID of the food item to fetch.
            use_cache: Whether to use cached data if available. Defaults to True.

        Returns:
            A FoodDetail object.

        Raises:
            DataNotFoundError: If the requested data is not found (404).
            ConnectionTimeoutError: If the connection times out (522, 524).
            AmbrAPIError: For other API-related errors.
        """
        data = await self._request(f"food/{id}", use_cache=use_cache)
        return FoodDetail(**data["data"])

    async def fetch_furnitures(self, use_cache: bool = True) -> list[Furniture]:
        """Fetches summary information for all furniture items (Serenitea Pot).

        Args:
            use_cache: Whether to use cached data if available. Defaults to True.

        Returns:
            A list of Furniture objects.

        Raises:
            DataNotFoundError: If the requested data is not found (404).
            ConnectionTimeoutError: If the connection times out (522, 524).
            AmbrAPIError: For other API-related errors.
        """
        data = await self._request("furniture", use_cache=use_cache)
        return [Furniture(**furniture) for furniture in data["data"]["items"].values()]

    async def fetch_furniture_detail(self, id: int, use_cache: bool = True) -> FurnitureDetail:
        """Fetches detailed information for a specific furniture item by its ID.

        Args:
            id: The ID of the furniture item to fetch.
            use_cache: Whether to use cached data if available. Defaults to True.

        Returns:
            A FurnitureDetail object.

        Raises:
            DataNotFoundError: If the requested data is not found (404).
            ConnectionTimeoutError: If the connection times out (522, 524).
            AmbrAPIError: For other API-related errors.
        """
        data = await self._request(f"furniture/{id}", use_cache=use_cache)
        return FurnitureDetail(**data["data"])

    async def fetch_furniture_sets(self, use_cache: bool = True) -> list[FurnitureSet]:
        """Fetches summary information for all furniture sets (Serenitea Pot).

        Args:
            use_cache: Whether to use cached data if available. Defaults to True.

        Returns:
            A list of FurnitureSet objects.

        Raises:
            DataNotFoundError: If the requested data is not found (404).
            ConnectionTimeoutError: If the connection times out (522, 524).
            AmbrAPIError: For other API-related errors.
        """
        data = await self._request("furnitureSuite", use_cache=use_cache)
        return [FurnitureSet(**furniture_set) for furniture_set in data["data"]["items"].values()]

    async def fetch_furniture_set_detail(
        self, id: int, use_cache: bool = True
    ) -> FurnitureSetDetail:
        """Fetches detailed information for a specific furniture set by its ID.

        Args:
            id: The ID of the furniture set to fetch.
            use_cache: Whether to use cached data if available. Defaults to True.

        Returns:
            A FurnitureSetDetail object.

        Raises:
            DataNotFoundError: If the requested data is not found (404).
            ConnectionTimeoutError: If the connection times out (522, 524).
            AmbrAPIError: For other API-related errors.
        """
        data = await self._request(f"furnitureSuite/{id}", use_cache=use_cache)
        return FurnitureSetDetail(**data["data"])

    async def fetch_materials(self, use_cache: bool = True) -> list[Material]:
        """Fetches summary information for all materials (includes ingredients, ascension items, etc.).

        Args:
            use_cache: Whether to use cached data if available. Defaults to True.

        Returns:
            A list of Material objects.

        Raises:
            DataNotFoundError: If the requested data is not found (404).
            ConnectionTimeoutError: If the connection times out (522, 524).
            AmbrAPIError: For other API-related errors.
        """
        data = await self._request("material", use_cache=use_cache)
        return [Material(**material) for material in data["data"]["items"].values()]

    async def fetch_material_detail(self, id: int, use_cache: bool = True) -> MaterialDetail:
        """Fetches detailed information for a specific material by its ID.

        Args:
            id: The ID of the material to fetch.
            use_cache: Whether to use cached data if available. Defaults to True.

        Returns:
            A MaterialDetail object.

        Raises:
            DataNotFoundError: If the requested data is not found (404).
            ConnectionTimeoutError: If the connection times out (522, 524).
            AmbrAPIError: For other API-related errors.
        """
        data = await self._request(f"material/{id}", use_cache=use_cache)
        return MaterialDetail(**data["data"])

    async def fetch_monsters(self, use_cache: bool = True) -> list[Monster]:
        """Fetches summary information for all monsters and living beings.

        Args:
            use_cache: Whether to use cached data if available. Defaults to True.

        Returns:
            A list of Monster objects.

        Raises:
            DataNotFoundError: If the requested data is not found (404).
            ConnectionTimeoutError: If the connection times out (522, 524).
            AmbrAPIError: For other API-related errors.
        """
        data = await self._request("monster", use_cache=use_cache)
        return [Monster(**monster) for monster in data["data"]["items"].values()]

    async def fetch_monster_detail(self, id: int, use_cache: bool = True) -> MonsterDetail:
        """Fetches detailed information for a specific monster or living being by its ID.

        Args:
            id: The ID of the monster/being to fetch.
            use_cache: Whether to use cached data if available. Defaults to True.

        Returns:
            A MonsterDetail object.

        Raises:
            DataNotFoundError: If the requested data is not found (404).
            ConnectionTimeoutError: If the connection times out (522, 524).
            AmbrAPIError: For other API-related errors.
        """
        data = await self._request(f"monster/{id}", use_cache=use_cache)
        return MonsterDetail(**data["data"])

    async def fetch_namecards(self, use_cache: bool = True) -> list[Namecard]:
        """Fetches summary information for all namecards.

        Args:
            use_cache: Whether to use cached data if available. Defaults to True.

        Returns:
            A list of Namecard objects.

        Raises:
            DataNotFoundError: If the requested data is not found (404).
            ConnectionTimeoutError: If the connection times out (522, 524).
            AmbrAPIError: For other API-related errors.
        """
        data = await self._request("namecard", use_cache=use_cache)
        return [Namecard(**name_card) for name_card in data["data"]["items"].values()]

    async def fetch_namecard_detail(self, id: int, use_cache: bool = True) -> NamecardDetail:
        """Fetches detailed information for a specific namecard by its ID.

        Args:
            id: The ID of the namecard to fetch.
            use_cache: Whether to use cached data if available. Defaults to True.

        Returns:
            A NamecardDetail object.

        Raises:
            DataNotFoundError: If the requested data is not found (404).
            ConnectionTimeoutError: If the connection times out (522, 524).
            AmbrAPIError: For other API-related errors.
        """
        data = await self._request(f"namecard/{id}", use_cache=use_cache)
        return NamecardDetail(**data["data"])

    async def fetch_quests(self, use_cache: bool = True) -> list[Quest]:
        """Fetches summary information for all quests.

        Args:
            use_cache: Whether to use cached data if available. Defaults to True.

        Returns:
            A list of Quest objects.

        Raises:
            DataNotFoundError: If the requested data is not found (404).
            ConnectionTimeoutError: If the connection times out (522, 524).
            AmbrAPIError: For other API-related errors.
        """
        data = await self._request("quest", use_cache=use_cache)
        return [Quest(**quest) for quest in data["data"]["items"].values()]

    async def fetch_tcg_cards(self, use_cache: bool = True) -> list[TCGCard]:
        """Fetches summary information for all Genius Invokation TCG cards.

        Args:
            use_cache: Whether to use cached data if available. Defaults to True.

        Returns:
            A list of TCGCard objects.

        Raises:
            DataNotFoundError: If the requested data is not found (404).
            ConnectionTimeoutError: If the connection times out (522, 524).
            AmbrAPIError: For other API-related errors.
        """
        data = await self._request("gcg", use_cache=use_cache)
        return [TCGCard(**tcg_card) for tcg_card in data["data"]["items"].values()]

    async def fetch_tcg_card_detail(self, id: int, use_cache: bool = True) -> TCGCardDetail:
        """Fetches detailed information for a specific TCG card by its ID.

        Args:
            id: The ID of the TCG card to fetch.
            use_cache: Whether to use cached data if available. Defaults to True.

        Returns:
            A TCGCardDetail object.

        Raises:
            DataNotFoundError: If the requested data is not found (404).
            ConnectionTimeoutError: If the connection times out (522, 524).
            AmbrAPIError: For other API-related errors.
        """
        data = await self._request(f"gcg/{id}", use_cache=use_cache)
        return TCGCardDetail(**data["data"])

    async def fetch_weapons(self, use_cache: bool = True) -> list[Weapon]:
        """Fetches summary information for all weapons.

        Args:
            use_cache: Whether to use cached data if available. Defaults to True.

        Returns:
            A list of Weapon objects.

        Raises:
            DataNotFoundError: If the requested data is not found (404).
            ConnectionTimeoutError: If the connection times out (522, 524).
            AmbrAPIError: For other API-related errors.
        """
        data = await self._request("weapon", use_cache=use_cache)
        return [Weapon(**weapon) for weapon in data["data"]["items"].values()]

    async def fetch_weapon_types(self, use_cache: bool = True) -> dict[str, str]:
        """Fetches a mapping of weapon type identifiers to their display names.

        Args:
            use_cache: Whether to use cached data if available. Defaults to True.

        Returns:
            A dictionary mapping weapon type IDs (e.g., "WEAPON_SWORD_ONE_HAND") to names (e.g., "Sword").

        Raises:
            DataNotFoundError: If the requested data is not found (404).
            ConnectionTimeoutError: If the connection times out (522, 524).
            AmbrAPIError: For other API-related errors.
        """
        data = await self._request("weapon", use_cache=use_cache)
        return data["data"]["types"]

    async def fetch_weapon_detail(self, id: int, use_cache: bool = True) -> WeaponDetail:
        """Fetches detailed information for a specific weapon by its ID.

        Args:
            id: The ID of the weapon to fetch.
            use_cache: Whether to use cached data if available. Defaults to True.

        Returns:
            A WeaponDetail object.

        Raises:
            DataNotFoundError: If the requested data is not found (404).
            ConnectionTimeoutError: If the connection times out (522, 524).
            AmbrAPIError: For other API-related errors.
        """
        data = await self._request(f"weapon/{id}", use_cache=use_cache)
        return WeaponDetail(**data["data"])

    async def fetch_domains(self, use_cache: bool = True) -> Domains:
        """Fetches information about daily domains and their rewards for each day of the week.

        Args:
            use_cache: Whether to use cached data if available. Defaults to True.

        Returns:
            A Domains object containing lists of domains for each weekday.

        Raises:
            DataNotFoundError: If the requested data is not found (404).
            ConnectionTimeoutError: If the connection times out (522, 524).
            AmbrAPIError: For other API-related errors.
        """
        data = await self._request("dailyDungeon", use_cache=use_cache)
        return Domains(**data["data"])

    async def fetch_changelogs(self, use_cache: bool = True) -> list[Changelog]:
        """Fetches the API changelogs.

        Args:
            use_cache: Whether to use cached data if available. Defaults to True.

        Returns:
            A list of Changelog objects.

        Raises:
            DataNotFoundError: If the requested data is not found (404).
            ConnectionTimeoutError: If the connection times out (522, 524).
            AmbrAPIError: For other API-related errors.
        """
        data = await self._request("changelog", static=True, use_cache=use_cache)
        changelogs: list[Changelog] = []
        for changelog_id, log in data["data"].items():
            changelogs.append(Changelog(id=int(changelog_id), **log))
        return changelogs

    async def fetch_upgrade_data(self, use_cache: bool = True) -> UpgradeData:
        """Fetches general upgrade material requirements for characters and weapons.

        Args:
            use_cache: Whether to use cached data if available. Defaults to True.

        Returns:
            An UpgradeData object containing lists of upgrade requirements.

        Raises:
            DataNotFoundError: If the requested data is not found (404).
            ConnectionTimeoutError: If the connection times out (522, 524).
            AmbrAPIError: For other API-related errors.
        """
        data = await self._request("upgrade", use_cache=use_cache)
        return UpgradeData(**data["data"])

    async def fetch_manual_weapon(self, use_cache: bool = True) -> dict[str, str]:
        """Fetches manual weapon data (purpose unclear from API structure).

        Args:
            use_cache: Whether to use cached data if available. Defaults to True.

        Returns:
            A dictionary containing the manual weapon data.

        Raises:
            DataNotFoundError: If the requested data is not found (404).
            ConnectionTimeoutError: If the connection times out (522, 524).
            AmbrAPIError: For other API-related errors.
        """
        data = await self._request("manualWeapon", use_cache=use_cache)
        return data["data"]

    async def fetch_readable(self, id: str, use_cache: bool = True) -> str:
        """Fetches the text content of a specific readable item (like a book volume) by its ID.

        Args:
            id: The ID of the readable item to fetch.
            use_cache: Whether to use cached data if available. Defaults to True.

        Returns:
            The text content of the readable item, with HTML tags removed.

        Raises:
            DataNotFoundError: If the requested data is not found (404).
            ConnectionTimeoutError: If the connection times out (522, 524).
            AmbrAPIError: For other API-related errors.
        """
        data = await self._request(f"readable/{id}", use_cache=use_cache)
        return remove_html_tags(data["data"])

    async def fetch_avatar_curve(
        self, use_cache: bool = True
    ) -> dict[str, dict[str, dict[str, float]]]:
        """Fetches the character stat growth curves.

        Args:
            use_cache: Whether to use cached data if available. Defaults to True.

        Returns:
            A nested dictionary representing character growth curves.
            Structure: { level: { curve_id: { stat_id: value } } }

        Raises:
            DataNotFoundError: If the requested data is not found (404).
            ConnectionTimeoutError: If the connection times out (522, 524).
            AmbrAPIError: For other API-related errors.
        """
        data = await self._request("avatarCurve", static=True, use_cache=use_cache)
        return data["data"]

    async def fetch_weapon_curve(
        self, use_cache: bool = True
    ) -> dict[str, dict[str, dict[str, float]]]:
        """Fetches the weapon stat growth curves.

        Args:
            use_cache: Whether to use cached data if available. Defaults to True.

        Returns:
            A nested dictionary representing weapon growth curves.
            Structure: { level: { curve_id: { stat_id: value } } }

        Raises:
            DataNotFoundError: If the requested data is not found (404).
            ConnectionTimeoutError: If the connection times out (522, 524).
            AmbrAPIError: For other API-related errors.
        """
        data = await self._request("weaponCurve", static=True, use_cache=use_cache)
        return data["data"]

    async def fetch_monster_curve(
        self, use_cache: bool = True
    ) -> dict[str, dict[str, dict[str, float]]]:
        """Fetches the monster stat growth curves.

        Args:
            use_cache: Whether to use cached data if available. Defaults to True.

        Returns:
            A nested dictionary representing monster growth curves.
            Structure: { level: { curve_id: { stat_id: value } } }

        Raises:
            DataNotFoundError: If the requested data is not found (404).
            ConnectionTimeoutError: If the connection times out (522, 524).
            AmbrAPIError: For other API-related errors.
        """
        data = await self._request("monsterCurve", static=True, use_cache=use_cache)
        return data["data"]

    async def fetch_abyss_data(self, use_cache: bool = True) -> AbyssResponse:
        """Fetches data for the current and potentially previous Spiral Abyss cycles.

        Args:
            use_cache: Whether to use cached data if available. Defaults to True.

        Returns:
            An AbyssResponse object containing details about abyss cycles, floors, enemies, etc.

        Raises:
            DataNotFoundError: If the requested data is not found (404).
            ConnectionTimeoutError: If the connection times out (522, 524).
            AmbrAPIError: For other API-related errors.
        """
        data = await self._request("tower", use_cache=use_cache)
        return AbyssResponse(**data["data"])

    async def fetch_character_guide(
        self, character_id: str, *, use_cache: bool = True
    ) -> CharacterGuide:
        """Fetches community-sourced build guides for a specific character.

        Combines data from sources like Genshin Wizard and genshin.aza.gg.

        Args:
            character_id: The ID of the character to fetch guides for.
            use_cache: Whether to use cached data if available. Defaults to True.

        Returns:
            A CharacterGuide object containing build, playstyle, and synergy recommendations.

        Raises:
            DataNotFoundError: If the requested data is not found (404).
            ConnectionTimeoutError: If the connection times out (522, 524).
            AmbrAPIError: For other API-related errors.
        """
        data = await self._request(
            f"advanced/avatarGuides/{character_id}", use_cache=use_cache, static=True
        )
        return CharacterGuide(**data["data"])

    async def _save_version(self, version: str) -> None:
        CACHE_PATH.mkdir(parents=True, exist_ok=True)
        async with aiofiles.open(CACHE_PATH / "version.txt", "w") as f:
            await f.write(f"{version},{time.time()}")

    async def _get_version(self) -> str | None:
        try:
            async with aiofiles.open(CACHE_PATH / "version.txt") as f:
                data = await f.read()
                version, timestamp = data.split(",")
                if time.time() - float(timestamp) > 60 * 60 * 24:  # 24 hours
                    return None
                return version
        except (FileNotFoundError, ValueError):
            return None

    async def fetch_latest_version(self) -> str:
        """Fetches the latest data version hash from the API.

        This hash is used internally to ensure requests use up-to-date data.

        Returns:
            The latest version hash string.

        Raises:
            DataNotFoundError: If the requested data is not found (404).
            ConnectionTimeoutError: If the connection times out (522, 524).
            AmbrAPIError: For other API-related errors.
        """
        data = await self._request("version", static=True, use_cache=False)
        return data["data"]["vh"]
