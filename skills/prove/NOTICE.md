# NOTICE — prove

Part of the **vflow** skill family (verified flow). Licensed MIT, like its upstreams.

## Derived from

`statechart`, `create-formal-verification-skill`, and `maintain-formal-verification-skill` from https://github.com/cursor/plugins (pstack/skills), Copyright (c) 2026 Lauren Tan, MIT.

Upstream snapshots read: mattpocock/skills @ `5863806dd4e15c63174bee4e7515a4256792ecfa`, cursor/plugins (pstack) @ `bf0c7cd80abdbf7fe47b634978a7d1b4071f71a7`.
Authoring followed the guidance in anthropics/skills `skill-creator` (Apache-2.0); no files from it are included.

## Changes

Recast as one skill with three modes: gate (model a design before any code exists and record pass/fail on the spec), bind (prefactor ticket: commit model, map to code, generate verify skill; adapted from create-formal-verification-skill), maintain (adapted from maintain-formal-verification-skill). Statechart guidance condensed; pstack's statechart is used by name when installed, otherwise new fallback scripts (tlc.sh, dot2mermaid.py, check_toolchain.sh, all original to vflow) draw a Mermaid chart from TLC's state graph. No pstack scripts are copied. Added toolchain degradation rules, gate record template, and a worked MessageDelivery example (original).

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

