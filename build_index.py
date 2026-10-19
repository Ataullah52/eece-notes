import re, pathlib
root = pathlib.Path(__file__).parent
T = re.compile(r"<title>(.*?)</title>", re.S)
D = re.compile(r'<meta name="description" content="(.*?)"', re.S)
out = ["# AI_INDEX", "Read only the file you are asked to edit. Rules: AI_SPEC.md. Never edit assets/."]
for sub in sorted(p for p in root.iterdir() if p.is_dir() and p.name not in ("assets",) and not p.name.startswith(".")):
    out.append("\n## " + sub.name)
    for f in sorted(sub.glob("*.html")):
        t = f.read_text(encoding="utf8")
        a, b = T.search(t), D.search(t)
        out.append("- %s — %s | %s" % (f.relative_to(root).as_posix(), a.group(1).strip() if a else "", b.group(1).strip() if b else ""))
(root / "AI_INDEX.md").write_text("\n".join(out) + "\n", encoding="utf8")
print("AI_INDEX.md updated")
