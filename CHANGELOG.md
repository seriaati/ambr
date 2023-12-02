# Changelog

All notable changes to this project will be documented in this file.

## [1.0.0] - 2023-12-02

### Bug Fixes

- Data obtain issue
- Typing issues
- Import issues
- Docstrings
- Incorrect endpoint value
- Fetch from value, not key
- Character model
- Food model
- Card tag field
- Package name
- Not typing ItemCategory
- Typo in fetch artifact set
- Typo in test
- Update story_id field to be optional in WeaponDetail model
- Fix certain models
- Fix data type assertion in test_fetch_readable
- Fix variable name in character and add new field in weapon promote
- Replace \\n with \n
- Fix cache not being used
- Fix replace pronoun function

### Features

- Add client
- Add models
- Add fetch functions
- Add DiceCost model
- Add new models
- Add pyproject.toml
- Domain models
- Tests
- Run pytest with github actions
- Change log model
- Lang test
- Upgrade data
- Beta attr for Character and CharacterDeteail
- Change log ItemCategory enum
- DataNotFound exception
- Update gh CI to use poetry
- Add italian and turkish
- Use same session across requests
- Add fetch_manual_weapon method to AmbrAPI class
- Add fetch_readable method
- Add methods to fetch avatar and weapon curves
- Add caching to API requests
- Add CharacterFetter model and fetch_character_fetter method
- Add pronoun replacement in character story

### Miscellaneous Tasks

- Add requirements.txt
- Update gitignore
- Remove ci
- Bump to v0.1.1
- Bump to v0.1.2
- Bump to v0.1.3
- Bump to v0.1.4
- Bump to v0.1.5
- Add git cliff config file
- Bump to v1.0.0

### Performance

- Export only certain classes
- Export selected classes only
- Export selected classes only

### Refactor

- Replace pip with poetry
- Change on event trigger from pull_request to push
- Replace deprecated validator func with field_validator
- Remove utils from __init__.py
- Rename name_card to namecard
- Rewrite tests with fixtures
- Remove unused argument
- Improve caching approach
- Refactor model field validators
- Replace try-except-pass with contextlib.suppress
- Replace wildcard import with specific imports

### Styling

- Remove unused imports
- Format code with black

### Testing

- Add test for character fetter

### Modify

- Change fetch function names
- Rename ItemCategory AVATAR to CHARACTER

<!-- generated by git-cliff -->