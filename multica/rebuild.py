#!/usr/bin/env python3
"""Rebuild a Multica workflow setup (skills, statuses, agents, squad, workflow)
in a workspace from a workspace-independent config (see multica/delivery.json).

Safe to run more than once: anything that already exists (by name or key) is
reused, an existing workflow with the same name is updated.

Always start with --dry-run:
  python3 multica/rebuild.py --workspace-id drm --status-map qa=quality_assurance --dry-run
"""
import argparse
import json
import os
import shlex
import subprocess
import sys
import tempfile

MULTICA = os.environ.get("MULTICA_BIN", "multica")
DEFAULT_CONFIG = os.path.join(os.path.dirname(os.path.abspath(__file__)), "delivery.json")
# issue-status create accepts: backlog, unstarted, started, done, closed.
# Exports show the board category instead; map it unless --raw-category.
CATEGORY_TO_CLI = {"todo": "unstarted", "in_progress": "started", "in_review": "started",
                   "blocked": "started", "cancelled": "closed"}


class Rebuild:
    def __init__(self, args, cfg):
        self.a = args
        self.cfg = cfg
        self.dry = args.dry_run
        self.ws = args.workspace_id
        self.summary = []  # (kind, name, action, id)
        self.n_writes = 0

    # ---- CLI plumbing -------------------------------------------------
    def _cmd(self, args, scoped=True):
        return [MULTICA] + args + ["--output", "json"] + (["--workspace-id", self.ws] if scoped else [])

    def read(self, args, allow_fail=False, scoped=True):
        cmd = self._cmd(args, scoped)
        proc = subprocess.run(cmd, capture_output=True, text=True)
        if proc.returncode != 0:
            if allow_fail:
                return None
            self.die("perintah baca gagal: %s\n%s" % (show(cmd), (proc.stderr or proc.stdout).strip()))
        try:
            return json.loads(proc.stdout)
        except ValueError:
            if allow_fail:
                return None
            self.die("output bukan JSON: %s\n%s" % (show(cmd), proc.stdout[:400]))

    def write(self, args, placeholder):
        cmd = self._cmd(args)
        self.n_writes += 1
        if self.dry:
            print("  [dry-run] " + show(cmd))
            return {"id": placeholder}
        print("  > " + show(cmd))
        proc = subprocess.run(cmd, capture_output=True, text=True)
        if proc.returncode != 0:
            self.die("perintah gagal: %s\n%s" % (show(cmd), (proc.stderr or proc.stdout).strip()))
        try:
            return json.loads(proc.stdout) if proc.stdout.strip() else {}
        except ValueError:
            return {"raw": proc.stdout}

    def die(self, msg):
        print("\nERROR: " + msg, file=sys.stderr)
        self.print_summary()
        print("Yang sudah jadi tetap aman. Perbaiki lalu jalankan ulang; langkah yang sudah ada akan dilewati.",
              file=sys.stderr)
        sys.exit(1)

    def note(self, kind, name, action, ident=""):
        self.summary.append((kind, name, action, ident or ""))
        print("  %-8s %-22s %s" % (kind, name, action))

    # ---- steps --------------------------------------------------------
    def resolve_workspace(self):
        """Resolve by full ID, slug, or exact name. CLI 0.10.0 list JSON has those fields only."""
        want = self.ws.lower()
        wss = as_list(self.read(["workspace", "list"], allow_fail=True, scoped=False) or [], "workspaces")
        hits = [w for w in wss if want in [str(v).lower() for k, v in w.items()
                                           if k in ("id", "slug", "name", "prefix", "issue_prefix", "identifier")]]
        if len(hits) > 1:
            self.die("'%s' cocok ke beberapa workspace: %s. Pakai ID lengkap."
                     % (self.a.workspace_id, ", ".join(w.get("name", "?") for w in hits)))
        if hits:
            self.ws = hits[0]["id"]
            print("Workspace: %s (%s)" % (hits[0].get("name"), self.ws))
            return
        # `workspace member list` takes an id, a slug, or a UUID prefix of at least
        # 4 hex chars. Its rows carry workspace_id. An issue prefix such as DRM
        # is not accepted here.
        rows = as_list(self.read(["workspace", "member", "list", self.ws], allow_fail=True, scoped=False) or [],
                       "members")
        ids = {r.get("workspace_id") for r in rows if r.get("workspace_id")}
        if len(ids) == 1:
            self.ws = ids.pop()
            names = {w["id"]: w.get("name") for w in wss}
            print("Workspace: %s (%s, dari '%s')" % (names.get(self.ws, "?"), self.ws, self.a.workspace_id))
            return
        choices = ", ".join("%s (%s)" % (w.get("name"), w.get("id")) for w in wss)
        self.die("workspace '%s' tidak ketemu.%s" % (self.a.workspace_id, (" Pilihan: " + choices) if choices else ""))

    def pick_runtime(self):
        if self.a.runtime_id:
            self.runtime_id = self.a.runtime_id
            print("Runtime: %s (dari --runtime-id)" % self.runtime_id)
            return
        provider = (self.cfg.get("runtime") or {}).get("provider", "claude")
        rts = as_list(self.read(["runtime", "list"]), "runtimes")
        ok = [r for r in rts if r.get("provider") == provider and r.get("status") == "online"
              and not r.get("archived_at") and r.get("workspace_id") in (None, self.ws)]
        if not ok:
            self.die("tidak ada runtime %s yang online di workspace ini. Nyalakan daemon, atau isi --runtime-id."
                     % provider)
        self.runtime_id = ok[0]["id"]
        print("Runtime: %s (%s) dipilih otomatis; ganti dengan --runtime-id kalau perlu"
              % (ok[0].get("name"), self.runtime_id))
        if len(ok) > 1:
            print("  runtime %s lain yang online: %s" % (provider, ", ".join(
                "%s (%s)" % (r.get("name"), r["id"]) for r in ok[1:])))

    def resolve_members(self):
        self.members = as_list(self.read(["workspace", "member", "list", self.ws]), "members")
        if self.a.member_id:
            self.owner_id = self.a.member_id
            print("Penanggung jawab manusia: %s (dari --member-id)" % self.owner_id)
            return
        owners = [m for m in self.members if m.get("role") == "owner"]
        if not owners:
            self.die("owner workspace tidak ketemu; isi --member-id <user-id>")
        self.owner_id = owners[0].get("user_id") or owners[0]["id"]
        print("Penanggung jawab manusia (@owner): %s <%s> (%s)"
              % (owners[0].get("name"), owners[0].get("email"), self.owner_id))

    def member_ref(self, ref):
        if ref == "@owner":
            return self.owner_id
        if ref.startswith("email:"):
            email = ref[6:].lower()
            for m in self.members:
                if str(m.get("email", "")).lower() == email:
                    return m.get("user_id") or m["id"]
            self.die("anggota %s tidak ada di workspace ini" % ref[6:])
        return ref

    def do_skills(self):
        print("\n1. Skill")
        have = {s["name"]: s["id"] for s in as_list(self.read(["skill", "list"]), "skills")}
        self.skill_ids = dict(have)
        imported = False
        for s in self.cfg.get("skills", []):
            if s["name"] in have:
                self.note("skill", s["name"], "sudah ada, dipakai", have[s["name"]])
                continue
            res = self.write(["skill", "import", "--url", s["url"], "--on-conflict", "skip"],
                             "<skill:%s>" % s["name"])
            imported = True
            self.skill_ids[s["name"]] = get_id(res, "skill") or "<skill:%s>" % s["name"]
            self.note("skill", s["name"], "diimpor dari " + s["url"], self.skill_ids[s["name"]])
        if imported and not self.dry:
            fresh = {s["name"]: s["id"] for s in as_list(self.read(["skill", "list"]), "skills")}
            self.skill_ids.update(fresh)

    def do_statuses(self):
        print("\n2. Status")
        existing = [s for s in as_list(self.read(["issue-status", "list"]), "statuses") if not s.get("archived_at")]
        by_key = {s["key"]: s for s in existing}
        by_name = {s["name"].casefold(): s for s in existing}
        self.key_of = {}
        for s in self.cfg.get("statuses", []):
            key = s["key"]
            if key in self.a.status_map:
                target = self.a.status_map[key]
                if target not in by_key:
                    self.die("--status-map %s=%s: status '%s' tidak ada di workspace ini" % (key, target, target))
                self.key_of[key] = target
                self.note("status", s["name"], "pakai yang ada: %s (--status-map)" % target, by_key[target]["id"])
            elif key in by_key:
                self.key_of[key] = key
                self.note("status", s["name"], "sudah ada (%s)" % key, by_key[key]["id"])
            elif s["name"].casefold() in by_name:
                found = by_name[s["name"].casefold()]
                self.key_of[key] = found["key"]
                self.note("status", s["name"], "sudah ada dengan key %s" % found["key"], found["id"])
            elif s.get("system"):
                self.die("status bawaan '%s' (%s) tidak ada. Cek workspace, atau pakai --status-map."
                         % (s["name"], key))
            else:
                cat = s["category"] if self.a.raw_category else CATEGORY_TO_CLI.get(s["category"], s["category"])
                args = ["issue-status", "create", "--name", s["name"], "--key", key,
                        "--category", cat, "--color", s.get("color") or "#6b7280"]
                if s.get("icon"):
                    args += ["--icon", s["icon"]]
                if s.get("description"):
                    args += ["--description", s["description"]]
                res = self.write(args, "<status:%s>" % key)
                self.key_of[key] = (res.get("key") if isinstance(res, dict) else None) or key
                self.note("status", s["name"], "dibuat (%s, kategori %s)" % (self.key_of[key], cat),
                          get_id(res, "status"))

    def do_agents(self):
        print("\n3. Agen")
        have = {x["name"]: x for x in as_list(self.read(["agent", "list"]), "agents") if not x.get("archived_at")}
        self.agent_ids, self.new_agents = {}, set()
        for ag in self.cfg.get("agents", []):
            if ag["name"] in have:
                self.agent_ids[ag["name"]] = have[ag["name"]]["id"]
                self.note("agen", ag["name"], "sudah ada, tidak diubah", have[ag["name"]]["id"])
                continue
            args = ["agent", "create", "--name", ag["name"], "--runtime-id", self.runtime_id]
            for flag, field in (("--model", "model"), ("--description", "description"),
                                ("--instructions", "instructions"), ("--thinking-level", "thinking_level")):
                if ag.get(field):
                    args += [flag, ag[field]]
            if ag.get("max_concurrent_tasks") and ag["max_concurrent_tasks"] != 6:
                args += ["--max-concurrent-tasks", str(ag["max_concurrent_tasks"])]
            if ag.get("permission_mode") == "public_to":
                args += ["--permission-mode", "public_to"]
                if ag.get("public_to_workspace"):
                    args += ["--public-to-workspace"]
            else:
                args += ["--permission-mode", "private"]
            res = self.write(args, "<agent:%s>" % ag["name"])
            self.agent_ids[ag["name"]] = get_id(res, "agent") or "<agent:%s>" % ag["name"]
            self.new_agents.add(ag["name"])
            self.note("agen", ag["name"], "dibuat (%s)" % (ag.get("model") or "model default"),
                      self.agent_ids[ag["name"]])

    def do_agent_skills(self):
        print("\n4. Skill per agen")
        for ag in self.cfg.get("agents", []):
            want = ag.get("skills") or []
            if not want:
                continue
            aid = self.agent_ids[ag["name"]]
            cur = set()
            if ag["name"] not in self.new_agents:
                cur = {s["name"] for s in as_list(self.read(["agent", "skills", "list", aid]), "skills")}
            missing = [n for n in want if n not in cur]
            if not missing:
                self.note("skill", ag["name"], "lengkap: " + ", ".join(want))
                continue
            unknown = [n for n in missing if n not in self.skill_ids]
            if unknown:
                self.die("skill %s untuk %s tidak ada di workspace dan tidak ada di daftar skills config"
                         % (", ".join(unknown), ag["name"]))
            self.write(["agent", "skills", "add", aid, "--skill-ids", ",".join(self.skill_ids[n] for n in missing)],
                       "")
            self.note("skill", ag["name"], "ditambah: " + ", ".join(missing))

    def do_squad(self):
        sq = self.cfg.get("squad")
        self.squad_ids = {}
        if not sq:
            return
        print("\n5. Squad")
        have = {x["name"]: x for x in as_list(self.read(["squad", "list"]), "squads") if not x.get("archived_at")}
        leader_id = self.agent_ids.get(sq["leader"])
        if not leader_id:
            self.die("leader %s tidak ada di daftar agen config" % sq["leader"])
        new = sq["name"] not in have
        if new:
            args = ["squad", "create", "--name", sq["name"], "--leader", leader_id]
            if sq.get("description"):
                args += ["--description", sq["description"]]
            res = self.write(args, "<squad:%s>" % sq["name"])
            sid = get_id(res, "squad") or "<squad:%s>" % sq["name"]
            self.note("squad", sq["name"], "dibuat, leader " + sq["leader"], sid)
            cur_ins = ""
        else:
            sid = have[sq["name"]]["id"]
            cur_ins = have[sq["name"]].get("instructions") or ""
            self.note("squad", sq["name"], "sudah ada, dipakai", sid)
            if have[sq["name"]].get("leader_id") != leader_id:
                print("  catatan: leader squad sekarang bukan %s. Tidak diubah otomatis." % sq["leader"])
        self.squad_ids[sq["name"]] = sid
        if sq.get("instructions") and sq["instructions"] != cur_ins:
            self.write(["squad", "update", sid, "--instructions", sq["instructions"]], "")
            self.note("squad", sq["name"], "instruksi diisi")
        cur = set()
        if not (new and self.dry):
            cur = {m["member_id"] for m in as_list(self.read(["squad", "member", "list", sid]), "members")}
        cur.add(leader_id)  # the leader joins on create
        for m in sq.get("members", []):
            mid = self.agent_ids.get(m["agent"])
            if not mid:
                self.die("anggota squad %s tidak ada di daftar agen config" % m["agent"])
            if mid in cur:
                self.note("anggota", m["agent"], "sudah di squad")
                continue
            args = ["squad", "member", "add", sid, "--member-id", mid, "--type", "agent"]
            if m.get("role"):
                args += ["--role", m["role"]]
            self.write(args, "")
            self.note("anggota", m["agent"], "ditambahkan ke squad")

    def build_steps(self):
        steps = []
        for st in self.cfg["workflow"]["steps"]:
            h = st.get("handler") or {"type": "none"}
            t = h.get("type", "none")
            if t == "agent":
                if h["agent"] not in self.agent_ids:
                    self.die("langkah %s: agen %s tidak dikenal" % (st["status"], h["agent"]))
                handler = {"type": "agent", "id": self.agent_ids[h["agent"]]}
            elif t == "squad":
                if h["squad"] not in self.squad_ids:
                    self.die("langkah %s: squad %s tidak dikenal" % (st["status"], h["squad"]))
                handler = {"type": "squad", "id": self.squad_ids[h["squad"]]}
            elif t == "member":
                handler = {"type": "member", "id": self.member_ref(h.get("member", "@owner"))}
            else:
                handler = {"type": "none"}
            out = {"status_key": self.status_key(st["status"]), "handler": handler,
                   "instructions": st.get("instructions") or ""}
            if st.get("next"):
                out["next_status_key"] = self.status_key(st["next"])
            if st.get("back"):
                out["back_status_key"] = self.status_key(st["back"])
            steps.append(out)
        return steps

    def status_key(self, key):
        if key not in self.key_of:
            self.die("status '%s' dipakai di workflow tapi tidak ada di daftar statuses config" % key)
        return self.key_of[key]

    def do_workflow(self):
        wf = self.cfg["workflow"]
        print("\n6. Workflow")
        steps = self.build_steps()
        fd, path = tempfile.mkstemp(prefix="multica-steps-", suffix=".json")
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            json.dump(steps, f, indent=2, ensure_ascii=False)
        print("  steps file: %s" % path)
        if self.dry:
            for s in steps:
                h = s["handler"]
                print("    %-18s %-7s %-40s next=%s back=%s" % (
                    s["status_key"], h["type"], h.get("id", ""), s.get("next_status_key", "-"),
                    s.get("back_status_key", "-")))
        have = {x["name"]: x for x in as_list(self.read(["workflow", "list"]), "workflows")}
        if wf["name"] in have:
            wid = have[wf["name"]]["id"]
            same_desc = (have[wf["name"]].get("description") or "") == (wf.get("description") or "")
            if same_desc and norm_steps(have[wf["name"]].get("steps")) == norm_steps(steps):
                self.note("workflow", wf["name"], "sudah ada dan sama, tidak diubah", wid)
                return
            args = ["workflow", "update", wid, "--steps-file", path]
            if wf.get("description"):
                args += ["--description", wf["description"]]
            self.write(args, wid)
            self.note("workflow", wf["name"], "sudah ada, langkahnya diperbarui", wid)
        else:
            args = ["workflow", "create", "--name", wf["name"], "--steps-file", path]
            if wf.get("description"):
                args += ["--description", wf["description"]]
            res = self.write(args, "<workflow:%s>" % wf["name"])
            self.note("workflow", wf["name"], "dibuat (%d langkah)" % len(steps), get_id(res, "workflow"))

    def print_summary(self):
        print("\n== Ringkasan%s ==" % (" (dry-run, belum ada yang diubah)" if self.dry else ""))
        for kind, name, action, ident in self.summary:
            print("  %-8s %-22s %s%s" % (kind, name, action, ("  [%s]" % ident) if ident else ""))
        print("  perintah tulis: %d%s" % (self.n_writes, " (hanya ditampilkan)" if self.dry else ""))

    def run(self):
        self.resolve_workspace()
        self.pick_runtime()
        self.resolve_members()
        self.do_skills()
        self.do_statuses()
        self.do_agents()
        self.do_agent_skills()
        self.do_squad()
        self.do_workflow()
        self.print_summary()
        if not self.dry:
            print("\nSelesai. Cek di Settings -> Workflows, lalu pasang workflow ke project yang perlu.")


def show(cmd):
    """Shell-quoted command with long values shortened for reading."""
    parts = []
    for p in cmd:
        if len(p) > 70:
            p = p[:50].replace("\n", " ") + "...(%d karakter)" % len(p)
        parts.append(p)
    return shlex.join(parts)


def norm_steps(steps):
    out = []
    for st in steps or []:
        h = st.get("handler") or {}
        out.append((st.get("status_key"), h.get("type", "none"), h.get("id"), st.get("instructions") or "",
                    st.get("next_status_key"), st.get("back_status_key")))
    return out


def as_list(data, *keys):
    if isinstance(data, list):
        return data
    for k in keys + ("items", "data"):
        if isinstance(data, dict) and isinstance(data.get(k), list):
            return data[k]
    return []


def get_id(res, kind):
    if not isinstance(res, dict):
        return ""
    if res.get("id"):
        return res["id"]
    inner = res.get(kind)
    return inner.get("id", "") if isinstance(inner, dict) else ""


def parse_map(values):
    out = {}
    for v in values:
        for pair in v.split(","):
            if not pair.strip():
                continue
            if "=" not in pair:
                raise SystemExit("--status-map perlu format key=key_yang_ada, dapat: %s" % pair)
            k, t = pair.split("=", 1)
            out[k.strip()] = t.strip()
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--workspace-id", required=True,
                    help="workspace tujuan: ID lengkap, slug, atau nama yang persis (mis. slug drm)")
    ap.add_argument("--runtime-id", help="runtime untuk agen baru (default: runtime claude pertama yang online)")
    ap.add_argument("--config", default=DEFAULT_CONFIG, help="file config (default: multica/delivery.json)")
    ap.add_argument("--dry-run", action="store_true", help="hanya baca dan tampilkan perintah tulis")
    ap.add_argument("--status-map", action="append", default=[], metavar="KEY=EXISTING_KEY",
                    help="pakai status yang sudah ada, mis. qa=quality_assurance (bisa diulang)")
    ap.add_argument("--member-id", help="user id manusia untuk langkah @owner (default: owner workspace)")
    ap.add_argument("--raw-category", action="store_true",
                    help="kirim kategori status apa adanya (todo, in_progress, ...) tanpa dipetakan")
    a = ap.parse_args()
    a.status_map = parse_map(a.status_map)
    with open(a.config, encoding="utf-8") as f:
        cfg = json.load(f)
    if cfg.get("version") != 1:
        raise SystemExit("versi config tidak dikenal: %s" % cfg.get("version"))
    Rebuild(a, cfg).run()


if __name__ == "__main__":
    main()
