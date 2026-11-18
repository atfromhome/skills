#!/usr/bin/env python3
"""Export a Multica workflow setup into a workspace-independent config.

Read-only. Uses the same multica CLI commands as the first manual export:
workflow get, issue-status list, agent list/get, agent skills list,
squad list/get, squad member list, skill list, workspace member list.

Example:
  python3 multica/export.py --workspace-id <source-id> --workflow Delivery \
      --out multica/delivery.json
"""
import argparse
import json
import re
import subprocess
import sys

MULTICA = "multica"


def cli(args, workspace_id):
    cmd = [MULTICA] + args + ["--output", "json", "--workspace-id", workspace_id]
    proc = subprocess.run(cmd, capture_output=True, text=True)
    if proc.returncode != 0:
        sys.exit("gagal: %s\n%s" % (" ".join(cmd), (proc.stderr or proc.stdout).strip()))
    try:
        return json.loads(proc.stdout)
    except ValueError:
        sys.exit("output bukan JSON: %s\n%s" % (" ".join(cmd), proc.stdout[:500]))


def as_list(data, *keys):
    """CLI list output is a JSON array; tolerate {"items": [...]} too."""
    if isinstance(data, list):
        return data
    for k in keys + ("items", "data"):
        if isinstance(data, dict) and isinstance(data.get(k), list):
            return data[k]
    return []


def slug(text):
    return re.sub(r"[^a-z0-9]+", "_", text.lower()).strip("_")


def clean_key(status):
    """'ready_2' (name 'Ready') -> 'ready'. The _2 suffix only exists because
    an archived status took the plain key in the source workspace."""
    key, name = status["key"], status["name"]
    m = re.match(r"^(.*)_\d+$", key)
    if not status.get("is_system") and m and m.group(1) == slug(name):
        return m.group(1)
    return key


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--workspace-id", required=True, help="source workspace id")
    ap.add_argument("--workflow", default="Delivery", help="workflow name")
    ap.add_argument("--out", default="-", help="output file (default stdout)")
    ap.add_argument("--only-used-skills", action="store_true",
                    help="only export skills assigned to exported agents")
    ap.add_argument("--agent", action="append", default=[],
                    help="extra agent name to export (repeatable)")
    a = ap.parse_args()
    ws = a.workspace_id

    wf = cli(["workflow", "get", a.workflow], ws)
    statuses = [s for s in as_list(cli(["issue-status", "list"], ws), "statuses")
                if not s.get("archived_at")]
    agents = [x for x in as_list(cli(["agent", "list"], ws), "agents") if not x.get("archived_at")]
    squads = [x for x in as_list(cli(["squad", "list"], ws), "squads") if not x.get("archived_at")]
    skills = as_list(cli(["skill", "list"], ws), "skills")
    members = as_list(cli(["workspace", "member", "list", ws], ws), "members")

    agent_by_id = {x["id"]: x for x in agents}
    squad_by_id = {x["id"]: x for x in squads}
    member_by_user = {m.get("user_id"): m for m in members}

    key_map = {s["key"]: clean_key(s) for s in statuses}
    used_keys = set()
    for st in wf["steps"]:
        for k in ("status_key", "next_status_key", "back_status_key"):
            if st.get(k):
                used_keys.add(st[k])

    # agents and squads the workflow points at
    want_agents, want_squads = [], []
    for st in wf["steps"]:
        h = st.get("handler") or {}
        if h.get("type") == "agent":
            want_agents.append(h["id"])
        elif h.get("type") == "squad":
            want_squads.append(h["id"])
    if len(set(want_squads)) > 1:
        sys.exit("lebih dari satu squad di workflow; config ini baru mendukung satu squad")

    squad_cfg = None
    if want_squads:
        sq = cli(["squad", "get", want_squads[0]], ws)
        sq_members = as_list(cli(["squad", "member", "list", sq["id"]], ws), "members")
        leader = agent_by_id[sq["leader_id"]]["name"]
        want_agents.insert(0, sq["leader_id"])
        mem_cfg = []
        for m in sq_members:
            if m.get("member_type") != "agent":
                print("lewati anggota squad non-agent: %s" % m.get("member_id"), file=sys.stderr)
                continue
            if m["member_id"] == sq["leader_id"]:
                continue
            want_agents.append(m["member_id"])
            mem_cfg.append({"agent": agent_by_id[m["member_id"]]["name"], "role": m.get("role") or ""})
        squad_cfg = {"name": sq["name"], "description": sq.get("description") or "",
                     "instructions": sq.get("instructions") or "", "leader": leader,
                     "members": mem_cfg}
    for name in a.agent:
        want_agents += [x["id"] for x in agents if x["name"] == name]

    seen, agent_cfgs, used_skills = set(), [], set()
    for aid in want_agents:
        if aid in seen:
            continue
        seen.add(aid)
        ag = cli(["agent", "get", aid], ws)
        ag_skills = sorted(s["name"] for s in as_list(cli(["agent", "skills", "list", aid], ws), "skills"))
        used_skills.update(ag_skills)
        targets = ag.get("invocation_targets") or []
        agent_cfgs.append({
            "name": ag["name"],
            "description": ag.get("description") or "",
            "instructions": ag.get("instructions") or "",
            "model": ag.get("model") or "",
            "thinking_level": ag.get("thinking_level") or "",
            "max_concurrent_tasks": ag.get("max_concurrent_tasks") or 6,
            "permission_mode": ag.get("permission_mode") or "private",
            "public_to_workspace": any(t.get("target_type") == "workspace" for t in targets),
            "avatar": ag.get("avatar_url") or "",
            "skills": ag_skills,
            # custom_env, mcp_config, runtime_id are left out on purpose
        })

    skill_cfgs = []
    for s in sorted(skills, key=lambda x: x["name"]):
        origin = ((s.get("config") or {}).get("origin") or {})
        url = origin.get("source_url")
        if a.only_used_skills and s["name"] not in used_skills:
            continue
        if not url:
            print("skill %s tidak punya source_url, dilewati" % s["name"], file=sys.stderr)
            continue
        skill_cfgs.append({"name": s["name"], "url": url})

    status_cfgs = []
    for s in statuses:
        if s["key"] not in used_keys:
            continue
        status_cfgs.append({
            "key": key_map[s["key"]], "name": s["name"], "category": s["category"],
            "color": s.get("color") or "#6b7280", "icon": s.get("icon") or "",
            "description": s.get("description") or "", "system": bool(s.get("is_system")),
        })

    def handler_cfg(h):
        t = h.get("type", "none")
        if t == "agent":
            return {"type": "agent", "agent": agent_by_id[h["id"]]["name"]}
        if t == "squad":
            return {"type": "squad", "squad": squad_by_id[h["id"]]["name"]}
        if t == "member":
            m = member_by_user.get(h["id"]) or {}
            if m.get("role") == "owner" or h["id"] == wf.get("owner_id"):
                return {"type": "member", "member": "@owner"}
            return {"type": "member", "member": "email:%s" % m.get("email", "?")}
        return {"type": "none"}

    steps = []
    for st in wf["steps"]:
        step = {"status": key_map.get(st["status_key"], st["status_key"]),
                "handler": handler_cfg(st.get("handler") or {}),
                "instructions": st.get("instructions") or ""}
        if st.get("next_status_key"):
            step["next"] = key_map.get(st["next_status_key"], st["next_status_key"])
        if st.get("back_status_key"):
            step["back"] = key_map.get(st["back_status_key"], st["back_status_key"])
        steps.append(step)

    cfg = {
        "version": 1,
        "runtime": {"provider": "claude"},
        "skills": skill_cfgs,
        "statuses": status_cfgs,
        "agents": agent_cfgs,
        "squad": squad_cfg,
        "workflow": {"name": wf["name"], "description": wf.get("description") or "", "steps": steps},
    }
    text = json.dumps(cfg, indent=2, ensure_ascii=False) + "\n"
    if a.out == "-":
        sys.stdout.write(text)
    else:
        with open(a.out, "w", encoding="utf-8") as f:
            f.write(text)
        print("ditulis: %s (%d agen, %d skill, %d status, %d langkah)"
              % (a.out, len(agent_cfgs), len(skill_cfgs), len(status_cfgs), len(steps)), file=sys.stderr)


if __name__ == "__main__":
    main()
