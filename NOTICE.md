# NOTICE

Skills in this repository (`skills/flow`, `chart`, `grill`, `spec`, `prove`, `slice`) form the **vflow** family (verified flow). `skills/lugas` is a standalone writing skill outside that family. Each skill folder also carries its own NOTICE.md so the attribution travels with a single copied skill.

## Derived from

Orchestration of the flow formed by mattpocock/skills (`wayfinder`, `grilling`, `domain-modeling`, `to-spec`, `to-tickets`) and pstack (`statechart`, `create-formal-verification-skill`, `maintain-formal-verification-skill`) by Matt Pocock and Lauren Tan. `grill` also adapts ideas from obra/superpowers `brainstorming` (Jesse Vincent, MIT) and anthropics/skills `doc-coauthoring` (Anthropic; idea only, no text included).

Upstream snapshots read: mattpocock/skills @ `5863806dd4e15c63174bee4e7515a4256792ecfa`, cursor/plugins (pstack) @ `bf0c7cd80abdbf7fe47b634978a7d1b4071f71a7`, obra/superpowers v6.1.1 (plugin cache snapshot `d884ae04edebef577e82ff7c4e143debd0bbec99`), anthropics/skills @ `e4bb5d960d87126ff3b3a8af1a104b7db67560ba`.
Authoring followed the guidance in anthropics/skills `skill-creator` (Apache-2.0); no files from it are included.

## lugas

Inspired by the `bahasa-indonesia-plain` gist by orepras: https://gist.github.com/orepras/3e1ca8974fc51d11825f142fa6a66635. No text copied; `skills/lugas` was written from scratch under this repository's MIT license. The RASA framework name and concept (Ritmis, Akurat, Sarat Makna, Alami) are credited to that source.

## Changes

New orchestrator: routing table, a grill step before the spec with a Decision summary handoff, verification levels A/B/C, tracker-as-source-of-truth with pluggable adapters and orchestrator mirroring, implementer/QA hooks, branch protection rules.

## mattpocock/skills license

```
MIT License

Copyright (c) 2026 Matt Pocock

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

## pstack (cursor/plugins) license

```
MIT License

Copyright (c) 2026 Lauren Tan

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

## obra/superpowers license

```
MIT License

Copyright (c) 2025 Jesse Vincent

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

## anthropics/skills doc-coauthoring

Only the idea of the opening context dump and its sufficiency test ("you can ask about edge cases and trade-offs without needing the basics explained") was adapted, rewritten in new words; no text or files from doc-coauthoring are included. The `skills/doc-coauthoring` folder carries no license file of its own; the anthropics/skills README states that many skills in that repository are open source under Apache-2.0. Credit: Anthropic, https://github.com/anthropics/skills (skills/doc-coauthoring).
