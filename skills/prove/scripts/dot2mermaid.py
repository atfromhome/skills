#!/usr/bin/env python3
"""prove fallback statechart: turn a TLC state-graph dump into a Mermaid stateDiagram.

Use when the pstack `statechart` skill is unavailable. Run TLC with `-dump dot,actionlabels`
(scripts/tlc.sh --dot does this), then:

  dot2mermaid.py states.dot --vars status [--trace tlc.out] [--words words.json] [--title T] > chart.mmd

--vars     comma list of variables that define a chart state (projection). Default: all variables.
--trace    a tlc.out with a counterexample: states on it get class bugPath, the last one gets breaks.
--words    JSON {"states": {"<projected label>": "Reader words"}, "actions": {"Action": "what the user sees happen"},
                 "hide": ["Action", ...]}  -- reader-facing wording, like pstack's view module.
--keep-self  draw steps that stay in the same chart state (dropped by default).
Standard library only.
"""
import argparse, json, re, sys
from collections import defaultdict, OrderedDict

NODE = re.compile(r'^\s*(-?\d+)\s+\[label="((?:[^"\\]|\\.)*)"(.*)\]\s*;?\s*$')
EDGE = re.compile(r'^\s*(-?\d+)\s*->\s*(-?\d+)\s*\[label="((?:[^"\\]|\\.)*)"')

def parse_assignments(text):
    """'/\\ x = 1\\n/\\ y = "a"' (dot-escaped) -> OrderedDict(x='1', y='"a"')"""
    text = text.replace('\\"', '"').replace('\\\\', '\\')
    out = OrderedDict()
    for part in re.split(r'\\n|\n', text):
        part = part.strip()
        if part.startswith('/\\'):
            part = part[2:].strip()
        if ' = ' in part:
            k, v = part.split(' = ', 1)
            out[k.strip()] = v.strip()
    return out

def parse_trace(path):
    states, cur = [], None
    for line in open(path, encoding='utf-8', errors='replace'):
        if re.match(r'^State \d+:', line):
            cur = OrderedDict(); states.append(cur); continue
        if cur is not None:
            m = re.match(r'^/\\\s+(\S+)\s+=\s+(.*)$', line.rstrip())
            if m: cur[m.group(1)] = m.group(2)
            elif not line.strip(): cur = None
    return states

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('dot'); ap.add_argument('--vars'); ap.add_argument('--trace')
    ap.add_argument('--words'); ap.add_argument('--title'); ap.add_argument('--keep-self', action='store_true')
    a = ap.parse_args()
    words = json.load(open(a.words)) if a.words else {}
    swords, awords, hide = words.get('states', {}), words.get('actions', {}), set(words.get('hide', []))
    keys = [k.strip() for k in a.vars.split(',')] if a.vars else None

    def project(assign):
        ks = keys or list(assign.keys())
        raw = ', '.join(f"{k}={assign.get(k, '?')}" for k in ks) if len(ks) > 1 else assign.get(ks[0], '?').strip('"')
        return swords.get(raw, raw)

    nodes, init, edges = {}, set(), defaultdict(set)
    for line in open(a.dot, encoding='utf-8', errors='replace'):
        m = EDGE.match(line)
        if m:
            edges[(m.group(1), m.group(2))].add(m.group(3)); continue
        m = NODE.match(line)
        if m:
            nodes[m.group(1)] = parse_assignments(m.group(2))
            if 'filled' in m.group(3): init.add(m.group(1))
    if not nodes:
        sys.exit('no states found in dot file (did TLC run with -dump dot,actionlabels?)')

    label = {n: project(v) for n, v in nodes.items()}
    ids = {}
    def sid(lbl):
        if lbl not in ids: ids[lbl] = f"s{len(ids)}"
        return ids[lbl]
    for n in nodes: sid(label[n])

    arrows = defaultdict(set)
    for (s, d), acts in edges.items():
        ls, ld = label.get(s), label.get(d)
        if ls is None or ld is None: continue
        if ls == ld and not a.keep_self: continue
        for act in acts:
            if act in hide: continue
            arrows[(ls, ld)].add(awords.get(act, act))

    bug, breaks = set(), None
    if a.trace:
        tr = parse_trace(a.trace)
        if tr:
            path = [project(s) for s in tr]
            bug = set(path); breaks = path[-1]

    out = []
    if a.title: out += ['---', f'title: {a.title}', '---']
    out.append('stateDiagram-v2')
    for lbl, i in ids.items():
        safe = lbl.replace('"', "'")
        out.append(f'    state "{safe}" as {i}')
    for n in sorted(init):
        out.append(f'    [*] --> {sid(label[n])}')
    for (ls, ld), acts in sorted(arrows.items(), key=lambda kv: (ids[kv[0][0]], ids[kv[0][1]])):
        text = ' / '.join(sorted(acts)).replace(':', ' -')
        out.append(f'    {ids[ls]} --> {ids[ld]} : {text}')
    out.append('    classDef breaks fill:#f8d0d0,stroke:#b00020,color:#5a0010')
    out.append('    classDef bugPath stroke:#b00020,stroke-width:3px')
    for lbl in bug:
        if lbl != breaks and lbl in ids: out.append(f'    class {ids[lbl]} bugPath')
    if breaks in ids: out.append(f'    class {ids[breaks]} breaks')
    print('\n'.join(out))
    n_arrows = len(arrows)
    print(f'%% {len(nodes)} model states -> {len(ids)} chart states, {n_arrows} arrows' +
          ('; aim for <= ~20 arrows: coarsen --vars or hide steps' if n_arrows > 20 else ''))

if __name__ == '__main__':
    main()
