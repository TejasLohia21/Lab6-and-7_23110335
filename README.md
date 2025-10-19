```markdown
# Repository Guide (Images + Artifacts)

## Where are the images?
- All CFG images are in `Lab7/`:
  - `Lab7/cfg.png`     → Program 1 CFG (default/first program).
  - `Lab7/cfg2.png`    → Program 2 CFG.
  - `Lab7/cfg3.png`    → Program 3 CFG.
- The latest DOT source of the graph is `Lab7/cfg.dot` (can be re-rendered to PNG if needed).

### Quick navigation tips
- In VS Code Explorer: expand `Lab7/` and double‑click `cfg.png`, `cfg2.png`, or `cfg3.png`.
- Use the editor’s breadcrumb to switch across images quickly.

## Other important items (brief)
- `Lab7/code.py`: end‑to‑end script that parses the C file, builds the CFG, computes metrics, runs Reaching Definitions (RD), and writes images/CSVs.
- `Lab7/Functions.py`: library of helpers for leaders, basic blocks, CFG edges, metrics, RD (gen/kill, in/out), and DOT export.
- `Lab7/code1.c`, `Lab7/code2.c`, `Lab7/code3.c`: the three analyzed C programs.
- `Lab7/code1_defs.csv`, `Lab7/code2_defs.csv`, `Lab7/code3_defs.csv`: definition map (Dk → variable, line, block, statement) for each program.
- `Lab7/code1_sets.csv`, `Lab7/code2_sets.csv`, `Lab7/code3_sets.csv`: per‑block RD sets with `gen[B]`, `kill[B]`, `in[B]`, `out[B]` as space‑separated D‑IDs.
- `Lab7/report/23110335_A2.pdf`: compiled report that includes the figures and tables.
- `Copy-20of-2023110373_A2.pdf.pdf`: external PDF that can be prepended to the report (via LaTeX `pdfpages`).

## Show images in this README
Paste the block below in your README to display the CFG images directly (GitHub/VS Code Markdown preview will render them):

```
## Control‑Flow Graphs

### Program 1
![CFG for Program 1]( 2
![CFG for Program 2]( 3
![CFG for Program 3](at a glance
- Definitions CSV (`codeX_defs.csv`):
  - Columns: `Dk,var,line,block,stmt`
  - Purpose: canonical IDs for assignments used across tables and figures.
- RD sets CSV (`codeX_sets.csv`):
  - Columns: `Block,gen[B],kill[B],in[B],out[B]`
  - Values: space‑separated D‑IDs for readability; replace the joiner if you prefer commas.

## Minimal file naming convention
- Images: `cfg.png`, `cfg2.png`, `cfg3.png` map 1→1 to `code1.c`, `code2.c`, `code3.c`.
- CSVs: `code{n}_defs.csv` and `code{n}_sets.csv` pair with `code{n}.c`.
- Graph source: always `cfg.dot` (the most recently produced CFG).

```
