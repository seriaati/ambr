# ambr
 An async API wrapper for [ambr.top](https://ambr.top/) written in Python.  

## Features
 - Uses `async` and `await`.
 - Support caching using [diskcache](https://github.com/grantjenks/python-diskcache).
 - Supports [pydantic](https://github.com/pydantic/pydantic) V2, all of the data is parsed into pydantic models.
 - Supports the majority of the popular endpoints.

## Installing
```
# pip
pip install git+https://github.com/seriaati/ambr

# poetry
poetry add git+https://github.com/seriaati/ambr
```

## Quick Example
```py
from ambr import AmbrAPI

async with AmbrAPI() as api:
    characters = await api.fetch_characters()
    for character in characters:
        print(character.name)
```
