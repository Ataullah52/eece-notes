# AI_SPEC — how to write a note page (read with AI_INDEX.md)
Task: write or edit ONLY the one chapter file you are given. Never edit assets/, index.html, AI_*.md.
## Page
One file per unit: `<subject>/unit-NN-name.html`. Copy the head/body skeleton from `eece1111/unit-01-circuit-variables.html` exactly (Pico CSS + ../assets/style.css + ../assets/site.js, `<body data-root="..">`, `<main class="container">`). Include `<title>` and `<meta name="description">`.
## Blocks (own classes, no inline CSS)
`definition` · `theory` · `memorize` · `example` · `pyq` (past question + solution) · `warn` (common mistakes). Final answer of a solved problem: `<p class="answer">…</p>` (boxed).
## Priority
Put `data-p="3|2|1"` on `<h2>`/`<h3>` (★★★ asked almost every year, ★★ often, ★ rare). Judge from the PYQ map, not from guesses.
## Content order per unit
Theory (definition → formula → one-line meaning) → proofs/derivations asked in exams → solved PYQ with every step (tag year + question number) → PYQ map table (year, question, marks) → quick revision → common mistakes.
## Rules
Math: KaTeX `\( … \)` inline, `\[ … \]` display; use `&lt;` for < in text. Tables: real `<table>`. Diagrams/graphs: inline `<svg class="fig">` or `<pre class="mermaid">`, never images of text. Check every number; if a figure was read from a scan, say so. Own words, no copied textbook pages. After adding a chapter run `python build_index.py`.
