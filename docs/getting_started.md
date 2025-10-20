# Getting Started

## Installation

```bash
pip install ambr-py
```

## Usage

Every API call goes through the `AmbrAPI` class. You can see more details in the [API Reference](./reference/client.md#ambr.client.AmbrAPI).

```py
import ambr

async with ambr.AmbrAPI(ambr.Language.CHT) as api:
    characters = await api.fetch_characters()
    print(characters)
```

Overall, it's pretty straightforward. You can find all the available methods in the [API Reference](./reference/client.md#ambr.client.AmbrAPI).

## Tips

### Starting and Closing the Client Properly

Remember to call `start()` and `close()` or use `async with` to ensure proper connection management.

```py
import ambr

async with ambr.AmbrAPI() as api:
    ...

# OR
api = ambr.AmbrAPI()
await api.start()
...
await api.close()
```

### Finding Model Attributes

Refer to the [Models](./reference/models/abyss.md) section for a list of all available models and their attributes.

### Catching Errors

Refer to the [Exceptions](./reference/exceptions.md) section for a list of all available exceptions, catch them with `try/except` blocks.

```py
import ambr

async with ambr.AmbrAPI() as api:
    try:
        await api.fetch_character(0)
    except ambr.exceptions.DataNotFoundError:
        print("Character does not exist.")
```
