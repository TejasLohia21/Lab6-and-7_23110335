```markdown
# LAB6 & LAB7 – CFG and Reaching Definitions

This repository contains a full pipeline to parse C programs, build Control‑Flow Graphs (CFGs), compute metrics, run Reaching Definitions (RD), and export figures/CSVs for LaTeX.

---

## Folder Map

- Lab7/
  - cfg.dot, cfg.png, cfg2.png, cfg3.png
  - code.py, csvgen.py, Functions.py, finalcode.ipynb
  - code1.c, code2.c, code3.c
  - code1_defs.csv, code1_sets.csv, code2_defs.csv, code2_sets.csv, code3_defs.csv, code3_sets.csv
  - report/23110335_A2.pdf (+ aux build files)
- Copy-20of-2023110373_A2.pdf.pdf (PDF to prepend to the Lab 7 report if needed)

---

## Quick Start (single block)

```
# 1) Create and activate venv
python3 -m venv .venv && source .venv/bin/activate

# 2) Install Python deps (Graphviz Python bindings if used)
pip install graphviz

# 3) Install system Graphviz (required to render DOT -> PNG)
# macOS (Homebrew):
brew install graphviz
# Ubuntu/Debian:
sudo apt-get update && sudo apt-get install -y graphviz
# Fedora:
sudo dnf install -y graphviz

# 4) Run the pipeline (from the repo root)
cd Lab7

# Option A: full pipeline via code.py (parses, builds CFG, metrics, RD, exports)
python code.py

# Option B: only regenerate CSVs via csvgen.py
python csvgen.py

# 5) Outputs you should see/update under Lab7/
# - cfg.dot (latest CFG in DOT)
# - cfg.png, cfg2.png, cfg3.png (rendered CFGs)
# - code1_defs.csv, code1_sets.csv
# - code2_defs.csv, code2_sets.csv
# - code3_defs.csv, code3_sets.csv
# - report/23110335_A2.pdf (compiled LaTeX report if you run LaTeX builds)
```

---

## What Each File Is

- Functions.py: parsing and analysis library
  - leaders_from_src, build_blocks_from_leaders
  - build_cfg_edges, cfg_metrics
  - collect_definitions, gen_kill_per_block
  - reaching_definitions (returns IN/OUT and iteration logs)
  - export_cfg_dot_html (writes cfg.dot; DOT can be rendered to PNG)

- code.py: end‑to‑end driver (CFG → metrics → RD → PNG/CSV exports)
- csvgen.py: only CSV exports for defs/sets (useful for LaTeX tables)
- codeX.c: three example C inputs (code1.c, code2.c, code3.c)
- cfg.dot: Graphviz DOT for the latest CFG
- cfg.png/cfg2.png/cfg3.png: CFG images for quick inspection and embedding
- codeX_defs.csv: Dk map (definition ID, var, line, block, stmt)
- codeX_sets.csv: per‑block gen[B], kill[B], in[B], out[B] (space‑separated Dk IDs)
- report/23110335_A2.pdf: built report PDF

---

## Viewing and Navigating Images

- In VS Code Explorer: Lab7/cfg.png, Lab7/cfg2.png, Lab7/cfg3.png
- Double‑click any PNG to preview.
- If you changed cfg.dot and need a fresh image:
  ```
  dot -Tpng cfg.dot -o cfg.png
  ```
- Recommended mapping:
  - Program 1 → cfg.png
  - Program 2 → cfg2.png
  - Program 3 → cfg3.png

---

## Embed Images in README (optional)

```
## Control‑Flow Graphs

### Program 1
![CFG for Program 1]( 2
![CFG for Program 2]( 3
![CFG for Program 3](emas (for LaTeX tables)

- Definitions
  - codeX_defs.csv columns: Dk,var,line,block,stmt
- Per‑block sets
  - codeX_sets.csv columns: Block,gen[B],kill[B],in[B],out[B]
  - IDs are space‑separated for readability (change joiner in csvgen.py if needed).

---

## LaTeX Snippets (copy into your .tex)

- Prepend an external PDF to the start of Lab 7:
```
% Preamble:
\usepackage{pdfpages}

% Immediately after \begin{document}:
\includepdf[pages=-,pagecommand={},fitpaper=true]{Copy-20of-2023110373_A2.pdf.pdf}
```

- Insert a CFG image:
```
\begin{figure}[H]
\centering
\includegraphics[width=\linewidth]{Lab7/cfg.png}
\caption{CFG for Program 1.}
\end{figure}
```

- Metrics table (example values):
```
\begin{table}[H]
\centering
\renewcommand{\arraystretch}{1.2}
\setlength{\tabcolsep}{10pt}
\begin{tabular}{|c|c|c|c|}
\hline
\textbf{Program No.} & \textbf{No. of Nodes (N)} & \textbf{No. of Edges (E)} & \textbf{Cyclomatic Complexity (CC)} \\
\hline
Code 1 & 131 & 202 & 73 \\
Code 2 & 122 & 203 & 83 \\
Code 3 & 104 & 167 & 65 \\
\hline
\end{tabular}
\caption{CFG metrics summary for each program.}
\end{table}
```

---

## Interpretation Guide

- gen[B]: new definitions created in block B
- kill[B]: prior definitions of the same vars overwritten in B
- in[B] = ⋃ out[P] over predecessors P of B
- out[B] = gen[B] ∪ (in[B] \ kill[B])
- Convergence: observed within two iterations for these programs

---
