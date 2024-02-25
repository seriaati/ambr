__all__ = ("DataNotFoundError",)


class DataNotFoundError(Exception):
    def __init__(self, message: str) -> None:
        self.message = message

    def __str__(self) -> str:
        return self.message
