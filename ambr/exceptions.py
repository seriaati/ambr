from __future__ import annotations

__all__ = ("AmbrAPIError", "ConnectionTimeoutError", "DataNotFoundError")


class AmbrAPIError(Exception):
    def __init__(self, code: int) -> None:
        self.code = code

    def __str__(self) -> str:
        return f"An error occurred while requesting the API, status code: {self.code}"


class DataNotFoundError(AmbrAPIError):
    def __init__(self) -> None:
        self.code = 404

    def __str__(self) -> str:
        return "Data not found"


class ConnectionTimeoutError(AmbrAPIError):
    def __init__(self) -> None:
        self.code = 522

    def __str__(self) -> str:
        return "Connection to the API timed out"
