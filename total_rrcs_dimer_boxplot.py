# -*- coding: utf-8 -*-
"""
Calculation of the total interface score for a given MD frame
"""

import os
import pandas as pd


def collect_interface_contact_totals(folder_path):
    """
    Walk through mutation folders and collect TOTAL A–B interface contact scores
    from every .cscore file (one total per file). No averaging.
    Returns: dict {mutation_label: [total_score_per_timepoint, ...]}
    """
    scores_by_mut = {}

    for root, dirs, files in os.walk(folder_path):
        for d in dirs:
            dir_path = os.path.join(root, d)

            # --- infer mutation label from folder name (same logic as your code) ---
            mut = ""
            if "V34A_S41A_" in d:
                mut = "V34A_S41A"
            elif "_" in d and d != "V34A_S41A":
                mut = d.split("_")[0]
            if not mut:
                continue
            if "_II" in d:
                mut += "_II"

            # --- collect totals from all .cscore files under this directory ---
            timepoint_totals = []
            for subroot, _, subfiles in os.walk(dir_path):
                for f in subfiles:
                    if not f.endswith(".cscore"):
                        continue

                    total_score = 0.0
                    with open(os.path.join(subroot, f), "r") as handle:
                        for line in handle:
                            line = line.strip()
                            if not line:
                                continue
                            try:
                                residue1, residue2, score = line.split()
                                chain1 = residue1.split(":")[0]
                                chain2 = residue2.split(":")[0]
                                if (chain1 == "A" and chain2 == "B") or (chain1 == "B" and chain2 == "A"):
                                    total_score += float(score)
                            except ValueError:
                                # skip malformed lines
                                continue

                    timepoint_totals.append(total_score)

            if timepoint_totals:
                scores_by_mut.setdefault(mut, []).extend(timepoint_totals)

    return scores_by_mut


# -------- paths --------
folder_path = r"C:\Users\selcuk.1\OneDrive - The Ohio State University\Desktop\dimer project"
out_csv = r"C:\Users\selcuk.1\OneDrive - The Ohio State University\Desktop\dimer project\boxplot_data_II.csv"

# -------- run --------
scores = collect_interface_contact_totals(folder_path)

df = pd.DataFrame.from_dict(scores, orient="index").T

# keep the same II set as before (only those that exist)
ii_cols = ["WT_II", "V34A_II", "S41A_II", "V34A_S41A_II", "F49A_II"]
ii_cols = [c for c in ii_cols if c in df.columns]

melted_df_II = df[ii_cols].melt(var_name="Mutation", value_name="Contact Score").dropna()
melted_df_II.to_csv(out_csv, index=False)

print("Wrote:", out_csv)

