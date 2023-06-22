from enum import Enum
from typing import Any, Dict, Final, List

import aiohttp


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
