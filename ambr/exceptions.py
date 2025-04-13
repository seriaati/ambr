from __future__ import annotations

__all__ = ("AmbrAPIError", "ConnectionTimeoutError", "DataNotFoundError")


class AmbrAPIError(Exception):
    """Base exception class for Ambr API errors.

    Attributes:
        code: The HTTP status code associated with the error.
    """

    def __init__(self, code: int) -> None:
        self.code = code

    def __str__(self) -> str:
        return f"An error occurred while requesting the API, status code: {self.code}"


class DataNotFoundError(AmbrAPIError):
    """Exception raised when requested data is not found (404).

    Attributes:
        code: The HTTP status code, always 404.
    """

    def __init__(self) -> None:
        self.code = 404

    def __str__(self) -> str:
        return "Data not found"


class ConnectionTimeoutError(AmbrAPIError):
    """Exception raised when the connection to the API times out (522).

    Attributes:
        code: The HTTP status code, always 522.
    """

    def __init__(self) -> None:
        self.code = 522

    def __str__(self) -> str:
        return "Connection to the API timed out"
