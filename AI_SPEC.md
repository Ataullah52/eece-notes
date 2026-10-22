# AI_SPEC — how to write a note page (read with AI_INDEX.md)
Task: write or edit ONLY the one chapter file you are given. Never edit assets/, any index.html, AI_*.md.
## Page
One file per topic: `<semester>/<course>/module-NN-name.html` (older hand-written pages use `unit-NN-name.html`) (e.g. `eece11/eece1111/module-02-basic-laws.html`; NN = topic number in curriculum.json). Copy the head/body skeleton from `eece11/eece1111/module-02-basic-laws.html` exactly, but set `<body data-root="../..">` (../assets/style.css + ../assets/site.js, no framework, `<body data-root="../..">`, `<main class="container">`). Include `<title>` and `<meta name="description">`.
## Blocks (own classes, no inline CSS)
`definition` · `theory` · `memorize` · `example` · `pyq` (past question + solution) · `warn` (common mistakes). Final answer of a solved problem: `<p class="answer">…</p>` (boxed).
## Priority
Put `data-p="3|2|1"` on `<h2>`/`<h3>` (★★★ asked almost every year, ★★ often, ★ rare). Judge from the PYQ map, not from guesses.
## Content order per unit
Theory (definition → formula → one-line meaning) → proofs/derivations asked in exams → solved PYQ with every step (tag year + question number) → PYQ map table (year, question, marks) → quick revision → common mistakes.
## Rules
Math: KaTeX `\( … \)` inline, `\[ … \]` display; use `&lt;` for < in text. Tables: real `<table>`. Diagrams/graphs: inline `<svg class="fig">` or `<pre class="mermaid">`, never images of text. Check every number; if a figure was read from a scan, say so. Own words, no copied textbook pages. After adding a chapter run `python build_index.py`.

## Adding structure
Semesters (eece11-eece42), subjects and topic titles live in `curriculum.json`. To add a subject or topic edit that file, then run `python3 build_index.py`: it regenerates the home page, every semester page, every subject page and AI_INDEX.md. Never hand-edit those generated index.html files.

Note pages for EECE1111, MATH1101 and PHY1101 were imported from the Gemini portal's data (one page per chapter, blocks tagged P1-P4: Class Note, PYQ, Professor-Followed Book, Syllabus Book). Keep that block meta line when editing them.
