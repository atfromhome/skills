#!/usr/bin/env python3
"""Uji skill atfromhome/skills dengan Claude Code CLI.

  python3 evals/vtest.py setup                 # siapkan sandbox + pasang 10 skill
  python3 evals/vtest.py triggers [skill...]   # uji pemicu
  python3 evals/vtest.py behavior [skill...]   # uji perilaku + dinilai otomatis
  python3 evals/vtest.py report                # rekap hasil
Opsi: --model sonnet  --only 1,3 (id kasus)  --timeout 600
"""
import argparse, json, os, shutil, subprocess, sys, time, datetime

EVALS = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(EVALS)
SKILLS = os.path.join(REPO, "skills")
SANDBOX = os.path.join(EVALS, ".vtest", "sandbox")
RESULTS = os.path.join(EVALS, ".vtest", "results")
ORDER = ["grill", "chart", "spec", "prove", "slice", "ship", "check", "pr", "lugas", "flow"]

CONTEXT = """Kamu sedang diuji di sandbox, bukan proyek nyata.
- Anggap repo-nya atfromhome/halo (Go + React) dengan tracker GitHub Issues.
- Repo, GitHub, dan tracker tidak tersedia. Kalau skill menyuruh membaca kode, menjalankan perintah, membuat issue, berkomentar, atau membuka PR, tulis apa persisnya yang akan kamu lakukan (perintah, isi issue/komentar/PR), lalu karang hasil yang masuk akal dan beri label [SIMULASI].
- Jangan mengubah file apa pun.
- Kalau skill menyuruh berhenti dan menunggu manusia, berhenti di situ.

Permintaan:
"""

JUDGE = """Kamu penilai yang ketat. Nilai jawaban AI terhadap daftar harapan.
Aturan: tiap harapan LULUS atau GAGAL saja. LULUS hanya jika ada bukti di jawaban; kutip buktinya maks 20 kata. Ragu = GAGAL.
Langkah yang diberi label [SIMULASI] dihitung sebagai dilakukan, asalkan isinya benar.
Jawaban bisa terdiri dari beberapa giliran. Giliran user adalah simulasi yang menyetujui semua rekomendasi. Nilai percakapan secara keseluruhan.

Skill: {skill}
Kasus: {prompt}
Hasil yang diharapkan: {expected}
Daftar harapan:
{items}

Jawaban AI:
<<<
{answer}
>>>

Balas HANYA JSON valid, tanpa teks lain dan tanpa ```:
{{"items":[{{"no":1,"pass":true,"evidence":"..."}}],"suggestions":["saran perbaikan untuk SKILL.md, maks 3"]}}"""


FOLLOWUP = """[Jawaban user, simulasi] Tidak ada konteks tambahan selain yang sudah kamu temukan. Saya setuju dengan semua rekomendasimu (semua ya). Kalau kamu minta konfirmasi pemahaman atau summary: ya, sudah benar."""
INTERACTIVE = {"grill": 5, "chart": 3, "spec": 3, "slice": 2, "check": 2}


def claude(prompt, args, tools, stream=False, resume=None):
    cmd = ["claude", "-p", prompt, "--max-turns", str(args.max_turns)]
    if resume:
        cmd += ["--resume", resume]
    if args.model:
        cmd += ["--model", args.model]
    if tools:
        cmd += ["--allowedTools", tools]
    cmd += ["--output-format", "stream-json", "--verbose"] if stream else ["--output-format", "json"]
    p = subprocess.run(cmd, cwd=SANDBOX, capture_output=True, text=True, timeout=args.timeout)
    if p.returncode != 0 and not p.stdout:
        raise RuntimeError(p.stderr.strip()[:500])
    return p.stdout


def parse_stream(out):
    skills, text, sid = [], "", None
    for line in out.splitlines():
        try:
            ev = json.loads(line)
        except ValueError:
            continue
        if ev.get("type") == "assistant":
            for c in ev.get("message", {}).get("content", []):
                if c.get("type") == "tool_use":
                    inp = json.dumps(c.get("input", {}))
                    if c.get("name") == "Skill":
                        skills += [s for s in ORDER + ["?"] if f'"{s}"' in inp or f":{s}\"" in inp] or [inp]
                    elif c.get("name") == "Read" and "SKILL.md" in inp:
                        skills += [s for s in ORDER if f"/{s}/SKILL.md" in inp]
        sid = ev.get("session_id") or sid
        if ev.get("type") == "result":
            text = ev.get("result", "") or text
    return list(dict.fromkeys(skills)), text, sid


def load(kind, skill):
    p = os.path.join(EVALS, "triggers" if kind == "t" else "", f"{skill}.json")
    return json.load(open(p))


def pick(names):
    bad = [n for n in names if n not in ORDER]
    if bad:
        sys.exit(f"Skill tidak dikenal: {bad}. Pilihan: {ORDER}")
    return names or ORDER


def setup(_):
    if shutil.which("claude") is None:
        sys.exit("Perintah `claude` tidak ditemukan. Pasang Claude Code dulu dan login.")
    os.makedirs(os.path.join(SANDBOX, ".claude"), exist_ok=True)
    dst = os.path.join(SANDBOX, ".claude", "skills")
    shutil.rmtree(dst, ignore_errors=True)
    shutil.copytree(SKILLS, dst)
    open(os.path.join(SANDBOX, "README.md"), "w").write("# halo (sandbox uji)\nRepo palsu untuk menguji skill. Kode asli tidak ada di sini.\n")
    if not os.path.isdir(os.path.join(SANDBOX, ".git")):
        subprocess.run(["git", "init", "-q"], cwd=SANDBOX)
    user = os.path.expanduser("~/.claude/skills")
    clash = [d for d in (os.listdir(user) if os.path.isdir(user) else []) if d in ORDER or d in ("grilling", "grill-me", "grill-with-docs", "tdd", "pr")]
    print(f"Sandbox siap: {SANDBOX}\n10 skill terpasang di {dst}")
    if clash:
        print(f"Catatan: skill pribadi di ~/.claude/skills ikut aktif dan bisa bentrok: {clash}")


def triggers(args):
    os.makedirs(RESULTS, exist_ok=True)
    rows = []
    for s in pick(args.skills):
        for i, q in enumerate(load("t", s), 1):
            try:
                got, _, _ = parse_stream(claude(q["query"], args, "Skill,Read,Glob,Grep", stream=True))
                err = ""
            except Exception as e:
                got, err = [], str(e)
            fired = s in got
            ok = fired == q["should_trigger"] and not err
            rows.append({"skill": s, "no": i, "query": q["query"], "should": q["should_trigger"], "fired": got, "ok": ok, "error": err})
            print(f"[{'OK ' if ok else 'XX '}] {s}#{i} harus={'ya' if q['should_trigger'] else 'tidak'} terpanggil={got or '-'} {err[:80]}")
    json.dump(rows, open(os.path.join(RESULTS, "triggers.json"), "w"), indent=1, ensure_ascii=False)
    print(f"\nPemicu benar: {sum(r['ok'] for r in rows)}/{len(rows)}")


def behavior(args):
    os.makedirs(os.path.join(RESULTS, "answers"), exist_ok=True)
    path = os.path.join(RESULTS, "behavior.json")
    rows = json.load(open(path)) if os.path.exists(path) else []
    only = {int(x) for x in args.only.split(",")} if args.only else None
    for s in pick(args.skills):
        for e in load("b", s)["evals"]:
            if only and e["id"] not in only:
                continue
            key = f"{s}-{e['id']}"
            print(f"\n== {key}: {e['prompt'][:90]}")
            extra = ""
            for f in e.get("files", []):
                fp = os.path.join(EVALS, f)
                if os.path.exists(fp):
                    extra += f"\n\nIsi file {f}:\n" + open(fp).read()
            t0 = time.time()
            turns = args.turns if args.turns is not None else INTERACTIVE.get(s, 1)
            got, parts, sid = [], [], None
            try:
                for t in range(turns):
                    msg = CONTEXT + e["prompt"] + extra if t == 0 else FOLLOWUP
                    g, a, sid = parse_stream(claude(msg, args, "Skill,Read,Glob,Grep", stream=True, resume=sid))
                    got += [x for x in g if x not in got]
                    if t:
                        parts.append(f"### Giliran user {t+1}\n{FOLLOWUP}")
                    parts.append(f"### Giliran AI {t+1}\n{a}")
                    if not sid:
                        break
            except Exception as ex:
                parts.append(f"ERROR: {ex}")
            ans = "\n\n".join(parts)
            open(os.path.join(RESULTS, "answers", key + ".md"), "w").write(f"# {key}\n\nSkill terpanggil: {got}\n\n## Prompt\n{e['prompt']}\n\n## Jawaban\n{ans}\n")
            items = "\n".join(f"{i}. {x}" for i, x in enumerate(e["expectations"], 1))
            verdict = {"items": [], "suggestions": []}
            try:
                raw = json.loads(claude(JUDGE.format(skill=s, prompt=e["prompt"], expected=e["expected_output"], items=items, answer=ans), args, ""))["result"]
                raw = raw[raw.find("{"): raw.rfind("}") + 1]
                verdict = json.loads(raw)
            except Exception as ex:
                verdict["error"] = str(ex)[:300]
            n = sum(1 for it in verdict["items"] if it.get("pass"))
            total = len(e["expectations"])
            for it in verdict["items"]:
                idx = it.get("no", 0) - 1
                label = e["expectations"][idx] if 0 <= idx < total else "?"
                print(f"   {'LULUS' if it.get('pass') else 'GAGAL'}  {label[:80]}")
            print(f"   Skor {n}/{total}  skill={got or '-'}  {int(time.time()-t0)} dtk")
            rows = [r for r in rows if r["key"] != key] + [{"key": key, "skill": s, "fired": got, "score": n, "total": total, "verdict": verdict, "expectations": e["expectations"]}]
            json.dump(rows, open(path, "w"), indent=1, ensure_ascii=False)


def report(_):
    L = [f"# Rekap uji skill ({datetime.datetime.now():%Y-%m-%d %H:%M})\n"]
    tp = os.path.join(RESULTS, "triggers.json")
    bp = os.path.join(RESULTS, "behavior.json")
    if os.path.exists(tp):
        t = json.load(open(tp))
        L.append(f"## Pemicu: {sum(r['ok'] for r in t)}/{len(t)} benar\n")
        for r in t:
            if not r["ok"]:
                L.append(f"- {r['skill']}#{r['no']} harus {'memicu' if r['should'] else 'tidak memicu'}, terpanggil {r['fired'] or '-'}: \"{r['query']}\"")
        L.append("")
    if os.path.exists(bp):
        b = sorted(json.load(open(bp)), key=lambda r: (ORDER.index(r["skill"]), r["key"]))
        L.append(f"## Perilaku: {sum(r['score'] for r in b)}/{sum(r['total'] for r in b)} harapan lulus\n")
        L.append("| Kasus | Skor | Skill terpanggil |\n|---|---|---|")
        L += [f"| {r['key']} | {r['score']}/{r['total']} | {', '.join(r['fired']) or '-'} |" for r in b]
        L.append("\n## Yang gagal dan saran\n")
        for r in b:
            ok = {i.get("no") for i in r["verdict"].get("items", []) if i.get("pass")}
            fails = [x for n, x in enumerate(r["expectations"], 1) if n not in ok]
            if fails or r["verdict"].get("error"):
                L.append(f"### {r['key']}")
                L += [f"- GAGAL: {x}" for x in fails]
                if r["verdict"].get("error"):
                    L.append(f"- Penilai error: {r['verdict']['error']}")
                L += [f"- Saran: {x}" for x in r["verdict"].get("suggestions", [])]
                L.append("")
    out = os.path.join(RESULTS, "REKAP.md")
    open(out, "w").write("\n".join(L))
    print("\n".join(L))
    print(f"\nTersimpan di {out}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["setup", "triggers", "behavior", "report"])
    ap.add_argument("skills", nargs="*")
    ap.add_argument("--model", default=None)
    ap.add_argument("--only", default=None)
    ap.add_argument("--max-turns", type=int, default=12)
    ap.add_argument("--turns", type=int, default=None, help="jumlah giliran percakapan; default 5 untuk grill, 3 chart/spec, 2 slice/check, 1 lainnya")
    ap.add_argument("--timeout", type=int, default=600)
    a = ap.parse_args()
    {"setup": setup, "triggers": triggers, "behavior": behavior, "report": report}[a.cmd](a)
