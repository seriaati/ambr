# ambr-py

## Introduction

ambr-py is an async API wrapper for [Project Ambr](https://gi.yatta.moe/) written in Python.  
Project Ambr is a beautiful website that displays Genshin Impact game data.  
Developing something for Hoyoverse games? You might be interested in [other API wrappers](https://github.com/seriaati#api-wrappers) written by me.
  
> Note: I am not the developer of Project Ambr.

### Features

- Fully typed.
- Fully asynchronous by using `aiofiles`, `aiohttp`, and `asyncio`, suitable for Discord bots.
- Provides direct icon URLs.
- Supports Python 3.11+.
- Supports all game languages.
- Supports persistent caching using SQLite.
- Supports [Pydantic V2](https://github.com/pydantic/pydantic), this also means full autocomplete support.

## Installation

```bash
# poetry
poetry add ambr-py

# pip
pip install ambr-py
```

## Quick Example

```py
import ambr
import asyncio

async def main() -> None:
    async with ambr.AmbrAPI(ambr.Language.CHT) as client:
        await client.fetch_characters()

asyncio.run(main())
```

## Getting Started

Read the [documentation](https://seria.is-a.dev/ambr) to learn more about on how to use this wrapper.

## Questions, Issues, Feedback, Contributions

Whether you want to make any bug reports, feature requests, or contribute to the wrapper, simply open an issue or pull request in this repository.  
If GitHub is not your type, you can find me on [Discord](https://discord.com/invite/b22kMKuwbS), my username is @seria_ati.
