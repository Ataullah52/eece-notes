#!/usr/bin/env python3
"""Rebuilds the home page, every semester page, every subject page and AI_INDEX.md.
Edit curriculum.json (semesters -> courses -> topics), add note pages, then run: python3 build_index.py
A note page is  <semester>/<course>/unit-NN-name.html  and is matched to topic number NN."""
import json, re, html, pathlib
root = pathlib.Path(__file__).parent
data = json.loads((root / "curriculum.json").read_text(encoding="utf8"))
e = html.escape
ORD = {1: "1st", 2: "2nd", 3: "3rd", 4: "4th"}
T = re.compile(r"<title>(.*?)</title>", re.S); D = re.compile(r'<meta name="description" content="(.*?)"', re.S)

def page(title, desc, rt, body):
    return ('<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">\n'
            f'<title>{e(title)}</title>\n<meta name="description" content="{e(desc)}">\n'
            f'<link rel="stylesheet" href="{rt}/assets/style.css"><script defer src="{rt}/assets/site.js"></script></head>\n'
            f'<body data-root="{rt}"><main class="container">\n{body}\n</main></body></html>\n')

def notes_for(sem, course):
    found = {}
    for f in sorted((root / sem["id"] / course["id"]).glob("unit-*.html")):
        m = re.match(r"unit-(\d+)-", f.name)
        if m: found[int(m.group(1))] = f
    return found

def sem_label(s): return f'{ORD[s["year"]]} year · {ORD[s["semester"]]} semester'
index_lines = ["# AI_INDEX", "Read only the file you are asked to edit. Rules: AI_SPEC.md. Never edit assets/ or generated index.html pages.", ""]
cards = []
for s in data["semesters"]:
    ready = 0
    cc = []
    for c in s["courses"]:
        notes = notes_for(s, c); ready += len(notes)
        total = max(len(c["topics"]), len(notes))
        cc.append((c, notes, total))
    n_c = len(s["courses"])
    meta = f'{n_c} subject{"s" if n_c != 1 else ""} · {ready} note page{"s" if ready != 1 else ""}' if n_c else "No subjects added yet"
    cards.append(f'<a class="card" href="{s["id"]}/index.html"><span class="tag">{s["id"].upper()}</span><h3>{sem_label(s).capitalize()}</h3><p>{meta}</p></a>')
    # semester page
    sc = []
    for c, notes, total in cc:
        sc.append(f'<a class="card" href="{c["id"]}/index.html"><span class="tag">{c["id"].upper()}</span><h3>{e(c["title"])}</h3><p>{c["type"]} · {c["credits"]:g} credits</p><p>{len(notes)} of {total} topics ready</p></a>' if True else "")
    body = (f'<div class="hero"><div class="eyebrow">{s["id"].upper()} · {sem_label(s)}</div><h1>Subjects</h1><p>Choose a subject to see its topics.</p></div>'
            + ('<div class="grid">' + "".join(sc) + '</div>' if sc else '<p class="card soon">No subjects added yet. Add them to curriculum.json and run build_index.py.</p>'))
    (root / s["id"]).mkdir(exist_ok=True)
    (root / s["id"] / "index.html").write_text(page(f'{s["id"].upper()} — Subjects', f'Subjects of {sem_label(s)}', "..", body), encoding="utf8")
    if s["courses"]: index_lines.append(f'## {s["id"]}')
    for c, notes, total in cc:
        # subject page
        tc = []
        nums = sorted(set(t["n"] for t in c["topics"]) | set(notes))
        titles = {t["n"]: t["title"] for t in c["topics"]}
        for n in nums:
            f = notes.get(n)
            if f:
                txt = f.read_text(encoding="utf8"); d = D.search(txt)
                tc.append(f'<a class="card" href="{f.name}"><span class="tag">TOPIC {n}</span><h3>{e(titles.get(n, f.stem))}</h3><p>{e(d.group(1).strip()) if d else ""}</p></a>')
                index_lines.append(f'- {s["id"]}/{c["id"]}/{f.name} — {c["id"].upper()} · topic {n} — {titles.get(n, "")}')
            else:
                tc.append(f'<div class="card soon"><span class="tag">TOPIC {n}</span><h3>{e(titles[n])}</h3><p>Notes coming soon</p></div>')
        body = (f'<div class="hero"><div class="eyebrow">{c["id"].upper()} · {c["type"]} · {c["credits"]:g} credits</div><h1>{e(c["title"])}</h1><p>Choose a topic to open its notes.</p></div>'
                + ('<div class="grid">' + "".join(tc) + '</div>' if tc else '<p class="card soon">No topics added yet. Add them to curriculum.json and run build_index.py.</p>'))
        (root / s["id"] / c["id"]).mkdir(exist_ok=True)
        (root / s["id"] / c["id"] / "index.html").write_text(page(f'{c["id"].upper()} — {c["title"]}', f'Topics of {c["title"]}', "../..", body), encoding="utf8")
    if s["courses"]: index_lines.append("")
home = ('<div class="hero"><div class="eyebrow">PUST · Electrical, Electronic and Communication Engineering</div><h1>EECE Notes</h1>'
        '<p>Pick a semester, then a subject, then a topic. Notes show theory, definitions, memorize points, examples and previous-year questions by priority, and print cleanly to PDF.</p></div>'
        '<div class="grid">' + "".join(cards) + '</div>')
(root / "index.html").write_text(page("EECE Notes — PUST", "Exam-focused EECE study notes for PUST, organised by semester, subject and topic.", ".", home), encoding="utf8")
(root / "AI_INDEX.md").write_text("\n".join(index_lines) + "\n", encoding="utf8")
print("Built home, semester, subject pages and AI_INDEX.md")
