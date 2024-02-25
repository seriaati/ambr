# ambr
 An async API wrapper for [Project Amber](https://ambr.top/) written in Python. Project Ambr displays Genshin Impact game data on a beautiful website.
 > Note: I am not the developer of Project Amber.  

## Quick Links
Developing something for Hoyoverse games? Check out my other API wrappers:
 - [enka.py](https://github.com/seriaati/enka-py) is an Enka Network API wrapper for fetching in-game showcase.
 - [yatta](https://github.com/seriaati/yatta) is a Project Yatta API wrapper for fetching Honkai Star Rail game data.

## Features
 - Fully typed.
 - Provides direct icon URLs.
 - Fully asynchronous by using `aiosqlite`, `aiohttp`, and `asyncio`.
 - Supports persistent caching using SQLite.
 - Supports [Pydantic V2](https://github.com/pydantic/pydantic).
 - Supports the majority of popular endpoints (create an issue if the one you need is missing).
 - 100% test coverage.

## Installing
```
# poetry
poetry add git+https://github.com/seriaati/ambr

# pip
pip install git+https://github.com/seriaati/ambr
```

## Quick Example
```py
from ambr import AmbrAPI, Language

async with AmbrAPI(lang=Language.CHT) as api:
    characters = await api.fetch_characters()
    for character in characters:
        print(character.name)

    light_cones = await api.fetch_light_cones(use_cache=False)
    for light_cone in light_cones:
        print(light_cone.id)
```

# Usage
## Starting and closing the client properly
To use the client properly, you can either:  
Manually call `start()` and `close()`  
```py
import ambr
import asyncio

async def main() -> None:
    api = ambr.AmbrAPI()
    await api.start()
    response = await api.fetch_characters()
    await api.close()

asyncio.run(main())
```
Or use the `async with` syntax:  
```py
import ambr
import asyncio

async def main() -> None:
   async with ambr.AmbrAPI() as api:
     await api.fetch_characters()

asyncio.run(main())
```
> [!IMPORTANT]  
> You ***need*** to call `start()` or the api client will not function properly; the `close()` method closes the request session and database properly.

## Client parameters
Currently, the `EnkaAPI` class allows you to pass in 4 parameters:
### Language
This will affect the languages of names of weapon, character, constellations, etc. You can find all the languages [here](https://github.com/seriaati/ambr/blob/d20969fb0e69d398391040afa823c798c3acac22/ambr/client.py#L43-L58).
### Headers
Custom headers used when requesting the Enka API, it is recommended to set a user agent, the default is `{"User-Agent": "ambr-py"}`.
### Cache TTL
Default is 3600 seconds (1 hour), the cache is evicted when this time expires. Note that setting a longer TTL might result in inconsistent data.

## Finding models' attributes
If you're using an IDE like VSCode or Pycharm, then you can see all the attributes and methods the model has in the autocomplete.
> [!TIP]
> If you're using VSCode, `alt` + `left click` on the attribute, then the IDE will bring you to the source code of this wrapper for you to see all the fields defined, most classes and methods have docstrings for you to reference to.

## Catching exceptions
If data is not found (API returns 404), then `ambr.exceptions.DataNotFoundError` will be raised.

# Questions, issues, contributions
For questions, you can contact me on [Discord](https://discord.com/users/410036441129943050) or open an [issue](https://github.com/seriaati/ambr/issues).  
To report issues with this wrapper, open an [issue](https://github.com/seriaati/ambr/issues).  
To contribute, fork this repo and submit a [pull request](https://github.com/seriaati/ambr/pulls).