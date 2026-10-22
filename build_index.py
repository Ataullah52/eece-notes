#!/usr/bin/env python3
"""Rebuilds the home page, every semester page, every subject page and AI_INDEX.md.
Edit curriculum.json (semesters -> courses -> topics), add note pages, then run: python3 build_index.py
A note page is  <semester>/<course>/module-NN-name.html  (or unit-NN-name.html) and is matched to topic number NN."""
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
    """Map topic number -> list of note pages (module-NN-*.html first, then unit-NN-*.html extras)."""
    found = {}
    folder = root / sem["id"] / course["id"]
    for pat in ("module", "unit"):
        for f in sorted(folder.glob(pat + "-*.html")):
            m = re.match(r"(?:module|unit)-(\d+)-", f.name)
            if m: found.setdefault(int(m.group(1)), []).append(f)
    return found

def sem_label(s): return f'{ORD[s["year"]]} year · {ORD[s["semester"]]} semester'
def routine(r):
    if not r: return ""
    head = "<tr><th>Day</th>" + "".join(f"<th>{e(t)}</th>" for t in r["timeSlots"]) + "</tr>"
    rows = "".join("<tr><td><b>%s</b></td>%s</tr>" % (e(x["day"]), "".join(f"<td>{e(c)}</td>" for c in x["slots"])) for x in r["rows"])
    return f'<h2>Class routine</h2><table><thead>{head}</thead><tbody>{rows}</tbody></table>'
index_lines = ["# AI_INDEX", "Read only the file you are asked to edit. Rules: AI_SPEC.md. Never edit assets/ or generated index.html pages.", ""]
cards = []
for s in data["semesters"]:
    ready = 0
    cc = []
    for c in s["courses"]:
        notes = notes_for(s, c); ready += len(notes)
        cc.append((c, notes, max(len(c["topics"]), len(notes))))
    n_c = len(s["courses"])
    meta = f'{n_c} subject{"s" if n_c != 1 else ""} · {ready} topic{"s" if ready != 1 else ""} with notes' if n_c else "No subjects added yet"
    cards.append(f'<a class="card" href="{s["id"]}/index.html"><span class="tag">{s["id"].upper()}</span><h3>{sem_label(s).capitalize()}</h3><p>{meta}</p></a>')
    sc = [f'<a class="card" href="{c["id"]}/index.html"><span class="tag">{c["id"].upper()}</span><h3>{e(c["title"])}</h3><p>{c["type"]} · {c["credits"]:g} credits</p><p>{len(notes)} of {total} topics have notes</p></a>' for c, notes, total in cc]
    body = (f'<div class="hero"><div class="eyebrow">{s["id"].upper()} · {sem_label(s)}</div><h1>Subjects</h1><p class="sub">{e(s.get("subtitle") or "")}</p></div>'
            + ('<div class="grid">' + "".join(sc) + '</div>' + routine(s.get("routine")) if sc else '<p class="card soon">No subjects added yet. Add them to curriculum.json and run build_index.py.</p>'))
    (root / s["id"]).mkdir(exist_ok=True)
    (root / s["id"] / "index.html").write_text(page(f'{s["id"].upper()} — Subjects', f'Subjects of {sem_label(s)}', "..", body), encoding="utf8")
    if s["courses"]: index_lines.append(f'## {s["id"]}')
    for c, notes, total in cc:
        tc = []
        titles = {t["n"]: t for t in c["topics"]}
        for n in sorted(set(titles) | set(notes)):
            t = titles.get(n, {}); label = (t.get("label") or f"Topic {n}").upper()
            files = notes.get(n, [])
            upd = f' · updated {e(t["updated"])}' if t.get("updated") and files else ""
            if files:
                tc.append(f'<a class="card" href="{files[0].name}"><span class="tag">{label}</span><h3>{e(t.get("title") or files[0].stem)}</h3><p>{e((t.get("summary") or "")[:170])}</p><p><small>{t.get("blocks", "")} blocks{upd}</small></p></a>')
                for f in files[1:]:
                    ti = T.search(f.read_text(encoding="utf8")); d = D.search(f.read_text(encoding="utf8"))
                    tc.append(f'<a class="card" href="{f.name}"><span class="tag">{label} · EXTRA</span><h3>{e(ti.group(1).strip() if ti else f.stem)}</h3><p>{e(d.group(1).strip()) if d else ""}</p></a>')
                for f in files: index_lines.append(f'- {s["id"]}/{c["id"]}/{f.name} — {c["code"]} · {t.get("label", "topic %d" % n)} — {t.get("title", "")}')
            else:
                tc.append(f'<div class="card soon"><span class="tag">{label}</span><h3>{e(t["title"])}</h3><p>{e((t.get("summary") or "")[:170])}</p><p><small>Notes coming soon</small></p></div>')
        books = c.get("books") or {}
        bk = "".join(f'<h3>{h}</h3><ul class="books">' + "".join(f"<li>{e(x)}</li>" for x in l) + "</ul>" for h, l in (("Professor-followed books", books.get("professor")), ("Syllabus recommended books", books.get("syllabus"))) if l)
        body = (f'<div class="hero"><div class="eyebrow">{c["code"]} · {c["type"]} · {c["credits"]:g} credits</div><h1>{e(c["title"])}</h1><p class="sub">{e(c.get("overview") or "Choose a topic to open its notes.")}</p></div>'
                + ('<div class="grid">' + "".join(tc) + '</div>' if tc else '<p class="card soon">No topics added yet.</p>') + bk)
        (root / s["id"] / c["id"]).mkdir(exist_ok=True)
        (root / s["id"] / c["id"] / "index.html").write_text(page(f'{c["code"]} — {c["title"]}', f'Topics of {c["title"]}', "../..", body), encoding="utf8")
    if s["courses"]: index_lines.append("")
home = ('<div class="hero"><div class="eyebrow">PUST · Electrical, Electronic and Communication Engineering</div><h1>EECE Notes</h1>'
        '<p>Pick a semester, then a subject, then a topic. Notes show theory, definitions, memorize points, examples and previous-year questions by priority, and print cleanly to PDF.</p></div>'
        '<div class="grid">' + "".join(cards) + '</div>')
(root / "index.html").write_text(page("EECE Notes — PUST", "Exam-focused EECE study notes for PUST, organised by semester, subject and topic.", ".", home), encoding="utf8")
(root / "AI_INDEX.md").write_text("\n".join(index_lines) + "\n", encoding="utf8")
print("Built home, semester, subject pages and AI_INDEX.md")
