import pandas as pd
import re
import re
from collections import defaultdict
import html;
import csv

p = {
    "label": re.compile(r'^\s*([A-Za-z_]\w*)\s*:\s*(?!:)'),
    "case": re.compile(r'^\s*case\b[^:]*:\s*$'),
    "default": re.compile(r'^\s*default\s*:\s*$'),
    "iff": re.compile(r'^\s*if\s*\('),
    "else": re.compile(r'^\s*else\b'),
    "for": re.compile(r'^\s*for\s*\('),
    "while": re.compile(r'^\s*while\s*\('),
    "do": re.compile(r'^\s*do\s*(?:\{)?\s*$'),
    "goto": re.compile(r'\bgoto\s+([A-Za-z_]\w*)\s*;'),
    "break": re.compile(r'^\s*break\s*;'),
    "cont": re.compile(r'^\s*continue\s*;'),
    "ret": re.compile(r'^\s*return\b'),
    "func": re.compile(r'^\s*(?:[A-Za-z_]\w*\s+)*[A-Za-z_]\w*\s*\([^;]*\)\s*\{?\s*$'),
}

def readfile(fn):
    with open(fn, "r", encoding="utf-8", errors="ignore") as f:
        return f.read()

def structural_only(s):
    t = s.strip()
    return t in ("{","}","};")

def next_stmt(lines, j):
    k = j + 1
    while k < len(lines):
        t = lines[k]
        if t.strip() and not t.lstrip().startswith("#") and not structural_only(t):
            return k
        k += 1
    return None

def first_stmt_in_block(lines, start_line):
    k = start_line
    if "{" not in lines[k]:
        while k < len(lines) and "{" not in lines[k]:
            k += 1
    k += 1
    while k < len(lines):
        t = lines[k]
        if t.strip() and not t.lstrip().startswith("#") and not structural_only(t):
            return k
        k += 1
    return None

def leaders_from_src(src):
    lines = src.splitlines()
    ls = set()
    labels = {}

    for i, s in enumerate(lines):
        if p["func"].match(s):
            ls.add(i)
            k = first_stmt_in_block(lines, i)
            if k is not None:
                ls.add(k)

    for i, s in enumerate(lines):
        if s.strip() and not s.lstrip().startswith("#"):
            ls.add(i)
            break

    for i, s in enumerate(lines):
        m = p["label"].match(s)
        if m:
            labels[m.group(1)] = i
            ls.add(i)
        if p["case"].match(s) or p["default"].match(s):
            ls.add(i)

    header_keys = ("iff","else","for","while","do")
    for i, s in enumerate(lines):
        if any(p[k].search(s) for k in header_keys):
            ls.add(i)
            k = next_stmt(lines, i)
            if k is not None:
                ls.add(k)

        if p["break"].search(s) or p["cont"].search(s) or p["ret"].search(s):
            k = next_stmt(lines, i)
            if k is not None:
                ls.add(k)

        if s.strip() == "}":
            k = next_stmt(lines, i)
            if k is not None:
                ls.add(k)

        m = p["goto"].search(s)
        if m and m.group(1) in labels:
            ls.add(labels[m.group(1)])

    idxs = sorted(ls)
    return idxs, lines


def nonstruct(s):
    t = s.strip()
    return t and t not in ("{","}","};") and not t.startswith("#")

def build_blocks_from_leaders(lines, leaders):
    leaders = sorted(set(leaders))
    leaders.append(len(lines))
    blocks = []
    for idx in range(len(leaders)-1):
        start = leaders[idx]
        end = leaders[idx+1]
        s = start
        while s < end and not nonstruct(lines[s]):
            s += 1
        e = end
        while e > s and not nonstruct(lines[e-1]):
            e -= 1
        if s < e:
            blocks.append((s, e))
    return blocks


is_branch_hdr = re.compile(r'^\s*(if|while|for)\b')
is_return     = re.compile(r'^\s*return\b')
is_break      = re.compile(r'^\s*break\s*;')
is_continue   = re.compile(r'^\s*continue\s*;')

def nonstruct(s):
    t = s.strip()
    return t and t not in ("{","}","};") and not t.startswith("#")

def last_stmt_line(lines, s, e):
    for k in range(e - 1, s - 1, -1):
        if nonstruct(lines[k]):
            return k
    return None

# def build_cfg_edges(lines, blocks):
#     edges = []
#     names = [f"B{i}" for i in range(len(blocks))]
#     for i, (s, e) in enumerate(blocks):
#         name = names[i]
#         k = last_stmt_line(lines, s, e)
#         fall = True
#         branch2 = False
#         if k is not None:
#             tail = lines[k]
#             if is_return.match(tail) or is_break.match(tail) or is_continue.match(tail):
#                 fall = False
#             elif is_branch_hdr.match(tail):
#                 branch2 = True
#         if fall and i + 1 < len(blocks):
#             edges.append((name, names[i + 1], "fall"))
#         if branch2:
#             if i + 1 < len(blocks):
#                 edges.append((name, names[i + 1], "true"))
#             if i + 2 < len(blocks):
#                 edges.append((name, names[i + 2], "false"))
#     return names, edges

def build_line_to_block(blocks):
    line2b = {}
    for bi, (s,e) in enumerate(blocks):
        for k in range(s, e):
            line2b[k] = bi
    return line2b

def find_follow_block(lines, blocks, hdr_line, line2b):
    depth = 0
    i = hdr_line
    opened = False
    while i < len(lines):
        if '{' in lines[i]: 
            depth += 1; opened = True
        if '}' in lines[i]:
            depth -= 1
            if opened and depth == 0:  # region closed
                k = next_stmt(lines, i)
                if k is not None and k in line2b:
                    return line2b[k]
                break
        i += 1
    # fallback: next block
    b = line2b.get(hdr_line, None)
    return (b+1) if b is not None and b+1 < len(blocks) else None

def find_body_block(lines, hdr_line, line2b):
    k = first_stmt_in_block(lines, hdr_line)
    return line2b.get(k, None) if k is not None else None

def build_cfg_edges(lines, blocks):
    names = [f"B{i}" for i in range(len(blocks))]
    edges = []
    line2b = build_line_to_block(blocks)
    loop_headers = [] 

    for i, (s,e) in enumerate(blocks):
        name = names[i]
        k = last_stmt_line(lines, s, e)
        if k is None:
            if i+1 < len(blocks): edges.append((name, names[i+1], "fall"))
            continue

        tail = lines[k]

        if is_return.match(tail):
            continue

        if is_branch_hdr.match(tail):
            body_b = find_body_block(lines, k, line2b)
            follow_b = find_follow_block(lines, blocks, k, line2b)
            if body_b is not None:  edges.append((name, names[body_b], "true"))
            if follow_b is not None: edges.append((name, names[follow_b], "false"))
            continue

        if is_continue.match(tail):
            if loop_headers:
                hdr_b = loop_headers[-1][1]
                edges.append((name, names[hdr_b], "continue"))
            continue

        if is_break.match(tail):
            if loop_headers:
                hdr_line = last_stmt_line(lines, *blocks[loop_headers[-1][1]])
                out_b = find_follow_block(lines, blocks, hdr_line, line2b)
                if out_b is not None:
                    edges.append((name, names[out_b], "break"))
            continue

        if i+1 < len(blocks):
            edges.append((name, names[i+1], "fall"))

    return names, edges


def cfg_metrics(num_blocks, edges):
    N = num_blocks
    E = len(edges)
    CC = E - N + 2
    return N, E, CC


assign_pat = re.compile(r'\b([A-Za-z_]\w*(?:\[[^\]]+\])?)\s*=')

def nonstruct(s):
    t = s.strip()
    return t and t not in ("{","}","};") and not t.startswith("#")

def block_names(blocks):
    return [f"B{i}" for i in range(len(blocks))]

def collect_definitions(lines, blocks):
    defs = []
    names = block_names(blocks)
    for bi,(s,e) in enumerate(blocks):
        bname = names[bi]
        for li in range(s, e):
            sline = lines[li]
            if not nonstruct(sline):
                continue
            parts = [p for p in sline.split(';') if p.strip()]
            for stmt in parts:
                if '=' in stmt and '==' not in stmt:
                    m = assign_pat.search(stmt)
                    if m:
                        var = m.group(1).strip()
                        defs.append((None, var, li, stmt.strip(), bname))
    out = []
    for k,(nid,var,li,txt,bname) in enumerate(defs, start=1):
        out.append((f"D{k}", var, li, txt, bname))
    return out

def gen_kill_per_block(defs, blocks):
    names = block_names(blocks)
    all_by_var = defaultdict(set)
    for Dk,var,li,txt,b in defs:
        all_by_var[var].add(Dk)
    gen = {b:set() for b in names}
    for Dk,var,li,txt,b in defs:
        gen[b].add(Dk)
    kill = {b:set() for b in names}
    for b in names:
        vars_in_b = set(var for (Dk,var,li,txt,bb) in defs if bb == b)
        kset = set()
        for v in vars_in_b:
            kset |= (all_by_var[v] - gen[b])
        kill[b] = kset
    return gen, kill

def preds(edges):
    P = defaultdict(set)
    for u,v,lbl in edges:
        P[v].add(u)
    return P

def reaching_definitions(blocks, edges, gen, kill):
    names = block_names(blocks)
    IN = {b:set() for b in names}
    OUT = {b:set() for b in names}
    P = preds(edges)
    changed = True
    it = 0
    logs = []
    while changed and it < 100:
        changed = False
        it += 1
        rows = []
        for b in names:
            in_new = set()
            for p in P[b]:
                in_new |= OUT[p]
            out_new = gen[b] | (in_new - kill[b])
            rows.append((b, sorted(gen[b]), sorted(kill[b]), sorted(in_new), sorted(out_new)))
            if in_new != IN[b] or out_new != OUT[b]:
                changed = True
            IN[b] = in_new
            OUT[b] = out_new
        logs.append(rows)
    return IN, OUT, logs


def stmt_lines(lines, s, e):
    out = []
    for k in range(s, e):
        parts = [p.strip() for p in lines[k].rstrip().split(';') if p.strip()]
        for p in parts:
            out.append(p + ";")
    return out

def html_block_label(lines, s, e, name):
    esc = lambda x: html.escape(x, quote=False)
    rows = "".join(f"<tr><td align='left'>{esc(p)}</td></tr>" for p in stmt_lines(lines, s, e))
    header = f"<tr><td bgcolor='#eeeeee'><b>{esc(name)} [{s},{e})</b></td></tr>"
    if not rows:
        rows = "<tr><td align='left'>(empty);</td></tr>"
    return f"<<table border='0' cellborder='1' cellspacing='0'>{header}{rows}</table>>"

def export_cfg_dot_html(lines, blocks, edges, program_name="code"):
    names = [f"B{i}" for i in range(len(blocks))]
    with open("cfg.dot", "w", encoding="utf-8") as f:
        f.write("digraph CFG {\n")
        f.write('  graph [fontname="Courier", nodesep=0.35, ranksep=0.4];\n')
        f.write('  node [shape=plaintext, fontname="Courier"];\n')
        f.write('  edge [fontname="Courier"];\n')
        for i,(s,e) in enumerate(blocks):
            label = html_block_label(lines, s, e, names[i])
            f.write(f"  {names[i]} [label={label}];\n")
        for u,v,lbl in edges:
            f.write(f'  {u} -> {v} [label="{lbl}"];\n')
        f.write(f'  labelloc="t";\n  label="CFG for {program_name}";\n')
        f.write("}\n")


def export_rd_csv(defs, gen, kill, IN, OUT, prefix="rd"):
    with open(f"{prefix}_defs.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["Dk","var","line","block","stmt"])
        for Dk,var,li,txt,b in defs:
            w.writerow([Dk,var,li,b,txt])
    order = sorted(gen.keys(), key=lambda x:int(x[1:]))
    with open(f"{prefix}_sets.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["Block","gen","kill","IN","OUT"])
        for b in order:
            w.writerow([
                b,
                " ".join(sorted(gen[b])),
                " ".join(sorted(kill[b])),
                " ".join(sorted(IN[b])),
                " ".join(sorted(OUT[b]))
            ])

def print_Dk_map(defs):
    print("Definition IDs:")
    for Dk,var,li,txt,b in defs:
        print(f"{Dk}: var={var}, line={li}, block={b}, stmt=[{txt}]")

def print_gen_kill(gen, kill):
    order = sorted(gen.keys(), key=lambda x:int(x[1:]))
    print("\nGEN/KILL:")
    for b in order:
        print(f"{b}: gen={sorted(gen[b])} kill={sorted(kill[b])}")

def print_final_in_out(IN, OUT):
    order = sorted(IN.keys(), key=lambda x:int(x[1:]))
    print("\nFinal IN/OUT:")
    for b in order:
        print(f"{b}: IN={sorted(IN[b])} OUT={sorted(OUT[b])}")
