import os
from typing import Dict, Set, Tuple
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


files = "/Users/zainab/Evaluation-of-Vulnerability-Analysis-Tools-using-CWE-based-Comparison/aggregated_findings.csv"
res= "/Users/zainab/Evaluation-of-Vulnerability-Analysis-Tools-using-CWE-based-Comparison/res"

def normalize_cwe(cwe: str) -> str:
    # Normalize CWE IDs (e.g., 'cwe-79 ' -> 'CWE-79')
    if pd.isna(cwe):
        return ""
    s = str(cwe).strip().upper()
    if not s.startswith("CWE-") and s.isdigit():
        s = f"CWE-{s}"
    return s

def ensure_columns(df: pd.DataFrame, required: Tuple[str, ...]) -> None:
    missing= [c for c in required if c not in df.columns]
    if missing:
        raise ValueError(f"Input CSV missing required columns: {missing}")

def iou_between_sets(a: Set[str], b: Set[str]) -> float:
    if not a and not b:
        return 1.0
    union = a | b
    inter = a & b
    return len(inter) / len(union) if union else 0.0

def compute_tool_sets(df: pd.DataFrame) -> Dict[str, Set[str]]:
    dfp = df[df["Number of Findings"] > 0].copy()
    tool_sets: Dict[str, Set[str]] = {}
    for tool, sub in dfp.groupby("Tool_name"):
        tool_sets[tool] = set(sub["CWE_ID"].unique())
    return tool_sets

def compute_top25_coverage(df: pd.DataFrame) -> pd.DataFrame:
    top25_col = "Is_In_CWE_Top_25?"
    top25_bool = df[top25_col]
    if df[top25_col].dtype == object:
        top25_bool = df[top25_col].astype(str).str.strip().str.lower().isin({"1", "true", "yes", "y"})
    df_top = df.copy()
    df_top[top25_col] = top25_bool

    dfp = df_top[df_top["Number of Findings"] > 0].copy()
    uniq_counts = dfp.groupby("Tool_name")["CWE_ID"].nunique().rename("Unique_CWEs")

    top25 = dfp[dfp[top25_col]]
    top25_counts = top25.groupby("Tool_name")["CWE_ID"].nunique().rename("Top25_CWEs")

    out = pd.concat([uniq_counts, top25_counts], axis=1).fillna(0).reset_index()
    out["Top25_CWEs"] = out["Top25_CWEs"].astype(int)
    out["Top25_Coverage(%)"] = np.where(out["Unique_CWEs"] > 0,
                                        100.0 * out["Top25_CWEs"] / out["Unique_CWEs"],
                                        0.0)
    return out.sort_values(by="Top25_Coverage(%)", ascending=False)

def compute_iou_matrix(tool_sets: Dict[str, Set[str]]) -> pd.DataFrame:
    tools = sorted(tool_sets.keys())
    mat = np.zeros((len(tools), len(tools)), dtype=float)
    for i, ti in enumerate(tools):
        for j, tj in enumerate(tools):
            mat[i, j] = iou_between_sets(tool_sets[ti], tool_sets[tj])
    return pd.DataFrame(mat, index=tools, columns=tools)

def compute_iou_per_project(df: pd.DataFrame) -> Dict[str, pd.DataFrame]:
    out = {}
    for proj, sub in df.groupby("Project_name"):
        tool_sets = compute_tool_sets(sub)
        if len(tool_sets) >= 2:
            out[proj] = compute_iou_matrix(tool_sets)
    return out


# Visualization
def plot_top25_coverage(coverage_df: pd.DataFrame, outpath: str) -> None:
    plt.figure(figsize=(9, 5))
    vals = coverage_df["Top25_Coverage(%)"].values
    bars = plt.bar(coverage_df["Tool_name"], vals, color="skyblue")
    for b, v in zip(bars, vals):
        plt.text(b.get_x() + b.get_width() / 2, b.get_height() + 0.5,
                 f"{v:.1f}%", ha="center", va="bottom", fontsize=9)
    plt.title("Top-25 CWE Coverage by Tool")
    plt.ylabel("Coverage (%)")
    plt.xticks(rotation=30, ha="right")
    plt.tight_layout()
    plt.savefig(outpath, dpi=200)
    plt.show()  
    plt.close()

def plot_iou_heatmap(iou_df: pd.DataFrame, outpath: str, title: str) -> None:
    plt.figure(figsize=(6 + 0.3 * len(iou_df), 5 + 0.3 * len(iou_df)))
    im = plt.imshow(iou_df.values, aspect="auto", cmap="viridis")
    plt.colorbar(im, fraction=0.046, pad=0.04)
    plt.xticks(ticks=np.arange(len(iou_df.columns)), labels=iou_df.columns, rotation=45, ha="right")
    plt.yticks(ticks=np.arange(len(iou_df.index)), labels=iou_df.index)
    plt.title(title)
    for i in range(iou_df.shape[0]):
        for j in range(iou_df.shape[1]):
            plt.text(j, i, f"{iou_df.iat[i, j]:.2f}", ha="center", va="center", fontsize=9)
    plt.tight_layout()
    plt.savefig(outpath, dpi=200)
    plt.show() 
    plt.close()

def main():
    os.makedirs(res, exist_ok=True)
    print("Reading CSV...")
    df = pd.read_csv(files)

    required_cols = ("Project_name", "Tool_name", "CWE_ID", "Number of Findings", "Is_In_CWE_Top_25?")
    ensure_columns(df, required_cols)

    df["CWE_ID"] = df["CWE_ID"].apply(normalize_cwe)
    df["Number of Findings"] = pd.to_numeric(df["Number of Findings"], errors="coerce").fillna(0).astype(int)

    # Tool-level Top-25 coverage
    print("Computing Top-25 coverage per tool...")
    coverage_df = compute_top25_coverage(df)
    coverage_csv = os.path.join(res, "tool_top25_coverage.csv")
    coverage_df.to_csv(coverage_csv, index=False)
    plot_top25_coverage(coverage_df, os.path.join(res, "tool_top25_coverage.png"))

    # Overall IoU
    print("Computing overall IoU matrix...")
    tool_sets_all = compute_tool_sets(df)
    iou_all = compute_iou_matrix(tool_sets_all)
    iou_all.to_csv(os.path.join(res, "iou_matrix_overall.csv"))
    plot_iou_heatmap(iou_all, os.path.join(res, "iou_matrix_overall.png"), title="Tool×Tool IoU (Overall)")

    # Per-project IoU
    print("Computing IoU per project...")
    iou_by_project = compute_iou_per_project(df)
    perproj_dir = os.path.join(res, "per_project_iou")
    os.makedirs(perproj_dir, exist_ok=True)
    for proj, mat in iou_by_project.items():
        safe_name = "".join(c if c.isalnum() or c in "-_." else "_" for c in proj)
        mat.to_csv(os.path.join(perproj_dir, f"iou_{safe_name}.csv"))
        plot_iou_heatmap(mat, os.path.join(perproj_dir, f"iou_{safe_name}.png"),
                         title=f"Tool×Tool IoU (Project: {proj})")

    print("\n=== Top-25 Coverage by Tool ===")
    print(coverage_df.to_string(index=False))

    print("\n=== Overall IoU Matrix ===")
    print(iou_all.round(2).to_string())

    print(f"\nReports saved in: {os.path.abspath(res)}")

if __name__ == "__main__":
    main()

