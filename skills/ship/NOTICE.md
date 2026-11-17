# NOTICE — ship

Part of the **vflow** skill family (verified flow). Licensed MIT, like its upstreams.

## Derived from

`implement`, `implement-spec`, `tdd` (with `tests.md` and `mocking.md`) and `diagnosing-bugs` (with `scripts/hitl-loop.template.sh`) from https://github.com/mattpocock/skills (skills/engineering), Copyright (c) 2026 Matt Pocock, MIT.

Upstream snapshot read: mattpocock/skills @ `5863806dd4e15c63174bee4e7515a4256792ecfa`.
Authoring followed the guidance in anthropics/skills `skill-creator` (Apache-2.0); no files from it are included.

## Changes

Merged implement and implement-spec into a single-ticket mode and a whole-spec mode; ticket lookup through the vflow tracker order; prefactor ticket 01 first, with `prove` bind for level A and property tests for level B; refusal to start a level-A spec without a current passed or human-waived formal gate; the tdd guidance rewritten so the first tests come from acceptance criteria and the INV-n/PROP-n they cite, at the spec's seams, with property tests for level B and invariant-mirroring tests for level A; examples rewritten as language-neutral pseudocode; the diagnosis loop condensed, with a route to `prove` maintain when code leaves the verified model; command discovery from repo docs; no pushes or merges to protected branches; hand-off to `check` instead of an inline review; model invocation enabled. The HITL template keeps its original logic with a generic first step and an attribution line.

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
