from __future__ import annotations

from typing import TYPE_CHECKING

import pytest
from loguru import logger

if TYPE_CHECKING:
    from collections.abc import Generator

    import loguru


@pytest.fixture(autouse=True)
def fail_on_loguru_error() -> Generator[None, None, None]:
    errors: list[str] = []

    def sink(message: loguru.Message) -> None:
        if message.record["level"].name == "ERROR":
            errors.append(str(message))

    sink_id = logger.add(sink)
    yield
    logger.remove(sink_id)

    if errors:
        pytest.fail("Loguru ERROR logs were emitted:\n" + "\n".join(errors))
