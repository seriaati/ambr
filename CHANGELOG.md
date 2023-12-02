# Changelog

All notable changes to this project will be documented in this file. See [conventional commits](https://www.conventionalcommits.org/) for commit guidelines.

---
## [unreleased]

### Miscellaneous Chores

- **(cliff)** merge cliff.toml into pyproject.toml - ([07e17b3](07e17b37ebe2c04b159d08b884062e75d468559a))
- add changelog file - ([9df8c79](9df8c79d9c72828c473d43ecbbb85899e40645c3))

---
## [1.0.0] - 2023-12-02

### Bug Fixes

- data obtain issue - ([40ea745](40ea7457c6482f7e8ae4508b2f16976233cf1ec5))
- typing issues - ([ada6f14](ada6f149e0ae9ebf4d8710c6b88600da55ff8162))
- import issues - ([9d5094f](9d5094feb857f9e2fe8a218717a5c4ef646d39d8))
- docstrings - ([5fc9e2f](5fc9e2ffe2a8d2712c79c8c7313dbe03ad230bbe))
- incorrect endpoint value - ([eaaf44e](eaaf44e5812e8e292be144351e19139dd5c048e8))
- fetch from value, not key - ([91ea3b5](91ea3b5ecd47328b567380b948b85332b4430035))
- character model - ([32c9381](32c93811048c2445f97cbbb5de7cbc20bb73b2f3))
- food model - ([a92c492](a92c4922a2ddc10f63642b35a5d9a63ac43eef18))
- card tag field - ([da6c154](da6c154a30e4e742841404ad428ee73fe29aabf5))
- package name - ([31c65ae](31c65aebf72d86e2271b6d15c51cde24d1a02652))
- not typing ItemCategory - ([ef5f91f](ef5f91fd46902a2047b3f76d03323fdf95e251ea))
- typo in fetch artifact set - ([10bb3a0](10bb3a04b4444e16cf9ae0edd57b25eb7dc3ebc9))
- typo in test - ([1c3adff](1c3adfff9338cf4518ab36079430d5cabe032a04))
- Update story_id field to be optional in WeaponDetail model - ([2cbda55](2cbda5567ad618485462378a618dd8ed1eb8a9df))
- fix certain models - ([9dc497f](9dc497fafc76368f99a4009bb188e8e8a970acac))
- Fix data type assertion in test_fetch_readable - ([44dcb46](44dcb464622b00da61373e43bfe9a4ed093dd2f1))
- Fix variable name in character and add new field in weapon promote - ([fc75dd9](fc75dd94509d6c2a8caf26c5cdaa289d1008626e))
- replace \\n with \n - ([4e9cced](4e9ccedfca44803ae4b95a4439d9355e07193d44))
- Fix cache not being used - ([dddeddf](dddeddfbe45c944d387d04ea60bf7612703de6ff))
- Fix replace pronoun function - ([7ad5731](7ad5731c95443a9cb3ff534b7a049c4d5cc329c9))

### Features

- add client - ([7f13df0](7f13df033d084db9b3a9f0dc1eff66a83897b951))
- add models - ([8f8a785](8f8a78579d322221ca370ca37e70c04d9c385745))
- add fetch functions - ([98719b1](98719b1ff48abeadc896dcdd19df6e4e08d7274b))
- add DiceCost model - ([c9c4c2c](c9c4c2c46920be3387340d05a7c6edfdc0c3b774))
- add new models - ([ee27b1e](ee27b1e350bccd97e035eeb7930aa9e6e1856f96))
- add pyproject.toml - ([d7daa19](d7daa19aa126ab71ea4bcdd07f30c743cc797f90))
- domain models - ([6d9acc7](6d9acc7b19820a62f39f1ff96153c827dbbe48c8))
- tests - ([34b0b02](34b0b020f34082c2c55161b86d2165a496c5cc58))
- run pytest with github actions - ([c0d8bd8](c0d8bd8b1e0672cbd747fdcf97af114adda31a6f))
- change log model - ([6f0c422](6f0c422d8165f3d31c72b86e9c9a6e684ed8c111))
- lang test - ([445c31c](445c31c5176010ee5219d99d6954c8e837c42877))
- upgrade data - ([5962e00](5962e0099d762cda38d074040a0cb31634950d33))
- beta attr for Character and CharacterDeteail - ([7a42231](7a422314c7beb114e0a22d7e893dc1d68c2fda6a))
- change log ItemCategory enum - ([4c509d2](4c509d2b649cce64ee8b1a4cd70ac9b9ed67722e))
- DataNotFound exception - ([a590801](a590801dafb32cb998aee7d8a7cdc35e9c3ba38a))
- update gh CI to use poetry - ([36e5aec](36e5aecd78775cc13e5c7b768376b7760ace647c))
- add italian and turkish - ([e418657](e418657dc87c0bd99b0bafe83b2af241802fe6a5))
- use same session across requests - ([cb2debf](cb2debf5de063563b017f8f3c5db3f9cdb1ea399))
- Add fetch_manual_weapon method to AmbrAPI class - ([f361107](f361107b03cf7ad7d249b2210da2b30848079131))
- Add fetch_readable method - ([89c6e96](89c6e9609b31dd3bd657d5e41c8e296fab79496a))
- Add methods to fetch avatar and weapon curves - ([4c03df9](4c03df974127ac9e97eb8504da66457de2da0541))
- Add caching to API requests - ([bc519ce](bc519ced7d4c33847871eaec3c0694b4eca9ffe5))
- Add CharacterFetter model and fetch_character_fetter method - ([c6d6fd0](c6d6fd0f150dc7e484561fa40920dbbd1b392a83))
- Add pronoun replacement in character story - ([181260b](181260b2fd7330c24d100069b233102cabe3ddda))

### Miscellaneous Chores

- **(cliff)** add git cliff config file - ([2586266](2586266d3cd5c9add2ec605cf21caf6a9e014f45))
- **(deps)** add diskcache - ([3bb76ac](3bb76acd53b0264bcfb65cd4b255ac22ae606fb6))
- **(deps)** add ruff - ([eadbe2e](eadbe2ee1ce6945ba14bf2f6a1e9a76b321e9188))
- **(deps)** update lock file - ([d2995f1](d2995f17649bd0a7dcdf5fa65b88212255ca3a2a))
- **(deps)** add git cliff - ([2591f29](2591f2905cca74fbe8fd3cf2e9b50895dcf21bd8))
- add requirements.txt - ([50a504c](50a504c270fdcbe5caf6ae12663101ad47285b00))
- update gitignore - ([780e1c1](780e1c1a9e2614509b45984f9b5b4364747b003f))

### Performance

- export only certain classes - ([ae33301](ae3330185a12758f91b18e9ae78890a20a4c0685))
- export selected classes only - ([3b4fbd4](3b4fbd421cd978766021f8bc5a1aacf084933198))
- export selected classes only - ([c2fc3d6](c2fc3d65f4355a86c39fcae49f7d4bf9e84a04ac))

### Refactoring

- replace pip with poetry - ([340b095](340b09521be266f2183b316a73944a299bbbae40))
- Change on event trigger from pull_request to push - ([6f044f1](6f044f1edeb2432d40730619df10a8127b42a6d6))
- replace deprecated validator func with field_validator - ([68ba7fa](68ba7faf41c4df491cffa3cadcd2d25ae38a50bd))
- remove utils from __init__.py - ([d4c0a80](d4c0a80c8f55216c6d25fad5b66c02c4fc543fda))
- rename name_card to namecard - ([e891ccf](e891ccf9aac90ceabae165127c58a5015a67a12f))
- rewrite tests with fixtures - ([385c9ef](385c9ef379a201540b1e4794c3c0aaebb5f369c0))
- remove unused argument - ([e268abb](e268abb4510cf8645c40369e7a3a23dd9493659b))
- improve caching approach - ([25f0991](25f0991425f9e4eb3ce18f83c6796a14b13fc075))
- Refactor model field validators - ([044dbbb](044dbbbade6ed7c672fe6f72aa1b91b14f72af1b))
- replace try-except-pass with contextlib.suppress - ([870892a](870892a43a9da1fcb6d02804a483555ce5b2d007))
- replace wildcard import with specific imports - ([e050de5](e050de5ce4a9f394888dbe92c122223939b02871))

### Style

- remove unused imports - ([80b1fe8](80b1fe845ea5b1adfc30ef1baffa5a0a44bda9fd))
- format code with black - ([e89086d](e89086dc09fe92f11cb1ffeb7645b74023c5a075))

### Tests

- Add test for character fetter - ([388473f](388473f351002c595895c5531a3c4c52061d7f1b))

### Ci

- remove ci - ([fef876c](fef876c519796ac3148d0f438bca413c91f3960a))

### Modify

- change fetch function names - ([14acc47](14acc4711681217728cccde840f47d41d66e7a59))
- rename ItemCategory AVATAR to CHARACTER - ([d884e2e](d884e2e10f040f4d536ef384bf3fbe8b07b4046e))

