# === Reaching Definitions: compute + export CSVs for code1 ===
from Functions import *

# 1) Parse and build CFG artifacts
src = readfile("code1.c")
idxs, lines = leaders_from_src(src)
blocks = build_blocks_from_leaders(lines, idxs)
names, edges = build_cfg_edges(lines, blocks)

# 2) Metrics (optional print)
N, E, CC = cfg_metrics(len(blocks), edges)
print(f"metrics: N={N}, E={E}, CC={CC}")

# 3) RD ingredients
defs = collect_definitions(lines, blocks)
gen, kill = gen_kill_per_block(defs, blocks)

# 4) Iterate to fixed point
IN, OUT, logs = reaching_definitions(blocks, edges, gen, kill)

# 5) Export CSVs
import csv, os

prefix = "code1"

# 5a) Definitions map: one row per Dk
with open(f"{prefix}_defs.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["Dk", "var", "line", "block", "stmt"])
    for Dk, var, li, txt, b in defs:
        w.writerow([Dk, var, li, b, txt])

# 5b) Per-block sets: gen/kill/IN/OUT (space-separated IDs)
order = [f"B{i}" for i in range(len(blocks))]
with open(f"{prefix}_sets.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["Block", "gen[B]", "kill[B]", "in[B]", "out[B]"])
    for b in order:
        g = " ".join(sorted(gen.get(b, [])))
        k = " ".join(sorted(kill.get(b, [])))
        i = " ".join(sorted(IN.get(b, [])))
        o = " ".join(sorted(OUT.get(b, [])))
        w.writerow([b, g, k, i, o])

print("Wrote:", os.path.abspath(f"{prefix}_defs.csv"))
print("Wrote:", os.path.abspath(f"{prefix}_sets.csv"))
