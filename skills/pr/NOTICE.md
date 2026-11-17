# NOTICE — pr

Standalone skill in this repository (works without the vflow family). Licensed MIT, like its upstreams.

## Derived from

- `pr` from https://github.com/mattpocock/skills (skills/engineering/pr), Copyright (c) 2026 Matt Pocock, MIT.
- The Summary section's menu of visuals (pseudocode, call trees, component trees, file trees, Mermaid, diffs) and its placement guidance come from **Dex Horthy**'s `show-me` skill (HumanLayer, https://github.com/humanlayer/skills/blob/main/plugins/show-me/skills/show-me/SKILL.md), Copyright (c) 2026 HumanLayer, MIT. mattpocock/skills reproduces it in `pr` and records the credit in its `CREDITS.md`; this skill keeps that credit here and in its frontmatter (`metadata.credits`) so it travels with the folder. `pr` does not depend on `show-me` as an installed skill.

Upstream snapshots read: mattpocock/skills @ `5863806dd4e15c63174bee4e7515a4256792ecfa`, humanlayer/skills @ `4d69d20f6e9b57b4fcf0d501ccfb1be961f0f329`.
Authoring followed the guidance in anthropics/skills `skill-creator` (Apache-2.0); no files from it are included.

## Changes

Kept the Summary / Evidence / Merge Danger template; moved the visuals menu to `references/visuals.md` with generic examples; added gathering steps (log, diff, linked issue, repo PR template, evidence from this session only), an optional Verification section for vflow tickets (ticket, spec, level, INV-n/PROP-n covered, closing keyword), and opening the PR only on request without ever merging; model invocation enabled.

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

## humanlayer/skills license

```
MIT License

Copyright (c) 2026 HumanLayer

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
