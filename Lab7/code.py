from x import *

src = readfile("code3.c")
idxs, lines = leaders_from_src(src)
blocks = build_blocks_from_leaders(lines, idxs)
print(len(idxs))
print()
print("-" * 80)
print("Identified leader lines")
print()

for a in idxs:
    print(a + 1, end = " ")
    print(lines[a])
    # print()

print()
print("-" * 80)
print("Basic Blocks")
print()

print("\nbasic blocks:", len(blocks))
for bi, (s, e) in enumerate(blocks):
    print(f"B{bi} [{s},{e})")
    for k in range(s, e):
        print(f"  {k}: {lines[k]}")

# generting edges

print()
print("-" * 80)
print("Constructed Edges")
print()

names, edges = build_cfg_edges(lines, blocks)
print(len(edges))
print("\nedges:")
for u,v,lbl in edges:
    print(f"{u} -> {v} ({lbl})")

print()
print("-" * 80)
print("Obtained Metrics")
print()

N,E,CC = cfg_metrics(len(blocks), edges)
print(f"\nmetrics: N={N}, E={E}, CC={CC}")

# reaching DFA

print()
print("-" * 80)
print("Definition for Reaching")
print()

defs = collect_definitions(lines, blocks)
print(f"\nDefinitions ({len(defs)}):")
for Dk,var,li,txt,b in defs[:20]:
    print(f"{Dk} @ line {li} in {b}: {var} = ... ; [{txt}]")
if len(defs) > 20:
    print("...")

print()
print("-" * 80)
print("Obtaining Generation and Killings")
print()

gen, kill = gen_kill_per_block(defs, blocks)
print("\nGEN/KILL per block:")
for b in sorted(gen.keys(), key=lambda x:int(x[1:])):
    print(b, "gen:", sorted(gen[b]), "kill:", sorted(kill[b]))

print()
print("-" * 80)
print("Iterations (Capped at 100)")
print()



IN, OUT, logs = reaching_definitions(blocks, edges, gen, kill)
print("\nReaching Definitions Iterations:")
for it, rows in enumerate(logs, start=1):
    print(f"\nIteration {it}")
    for b,g,k,ins,outs in rows:
        print(f"{b} | gen:{g} kill:{k} in:{ins} out:{outs}")

print()
print("-" * 80)
print("Final IN and OUT")
print()


print("\nFinal IN/OUT:")
for b in sorted(IN.keys(), key=lambda x:int(x[1:])):
    print(f"{b} IN:{sorted(IN[b])} OUT:{sorted(OUT[b])}")

print()
print("-" * 80)
print("Exporting as DOT File and Image Generation")
print()


# exporting the dot files
export_cfg_dot_html(lines, blocks, edges, program_name="code1.c")

# !dot -Tpng cfg.dot -o cfg.png

print()
print("-" * 80)
print("Exporting as CSV File")
print()


export_rd_csv(defs, gen, kill, IN, OUT, prefix="code1")