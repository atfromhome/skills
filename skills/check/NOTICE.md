# NOTICE — check

Part of the **vflow** skill family (verified flow). Licensed MIT, like its upstreams.

## Derived from

- `code-review` from https://github.com/mattpocock/skills (skills/engineering/code-review), Copyright (c) 2026 Matt Pocock, MIT. The Fowler smell baseline (after Martin Fowler, *Refactoring*, ch. 3) is adapted from it.
- The "evidence before claims" rule from `verification-before-completion` in https://github.com/obra/superpowers, Copyright (c) 2025 Jesse Vincent, MIT. Only that rule was taken, reworded.

Upstream snapshots read: mattpocock/skills @ `5863806dd4e15c63174bee4e7515a4256792ecfa`, obra/superpowers v6.1.1 (plugin cache snapshot `d884ae04edebef577e82ff7c4e143debd0bbec99`).
Authoring followed the guidance in anthropics/skills `skill-creator` (Apache-2.0); no files from it are included.

## Changes

Added a third axis, Verification (verify skill run, model re-check for level A, acceptance criteria ticked with evidence, INV-n/PROP-n coverage map, drift routed to `prove` maintain); a sequential fallback when subagents are unavailable; a fixed point that defaults to the integration or default branch; a pause point before any fix, with fixes routed back through `ship`; the evidence rule; PR opening through the `pr` skill with closing links, never merging; pluggable tracker lookup; model invocation enabled.

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
