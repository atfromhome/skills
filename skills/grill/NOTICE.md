# NOTICE — grill

Part of the **vflow** skill family (verified flow). Licensed MIT, like its MIT upstreams.

## Derived from

- `grilling` (skills/productivity/grilling) and `domain-modeling` (skills/engineering/domain-modeling, including GLOSSARY-FORMAT.md and ADR-FORMAT.md) from https://github.com/mattpocock/skills, Copyright (c) 2026 Matt Pocock, MIT. This is the core of the skill: the design tree, rounds that ask the whole frontier with recommended answers, facts looked up instead of asked, glossary challenges, and the three-criteria ADR test. `references/glossary-format.md` and `references/adr-format.md` are adapted copies of the two format files.
- `brainstorming` (skills/brainstorming) from https://github.com/obra/superpowers (v6.1.1), Copyright (c) 2025 Jesse Vincent, MIT. Adapted ideas only: the scope check up front, proposing 2–3 approaches with trade-offs and a recommendation, and the hard gate against implementation before the human confirms. Its design-doc writing and writing-plans transition were not taken.
- `doc-coauthoring` from https://github.com/anthropics/skills: the opening context dump and its sufficiency test (see below).

Upstream snapshots read: mattpocock/skills @ `5863806dd4e15c63174bee4e7515a4256792ecfa`, obra/superpowers v6.1.1 (plugin cache snapshot `d884ae04edebef577e82ff7c4e143debd0bbec99`), anthropics/skills @ `e4bb5d960d87126ff3b3a8af1a104b7db67560ba`.
Authoring followed the guidance in anthropics/skills `skill-creator` (Apache-2.0); no files from it are included.

## Changes

Merged grilling and domain-modeling into one interview step that sits before `spec`; added the context dump, the scope check that hands big efforts to `chart`, design forks with 2–3 approaches, verification questions inside the design tree, a hard gate against code and spec writing, two pause points (scope check, shared-understanding confirmation), and a Decision summary handoff with a provisional verification level (A/B/C) that `spec` consumes and that can be posted on the tracker issue. Glossary and ADR formats now defer to a repo's existing conventions.

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
