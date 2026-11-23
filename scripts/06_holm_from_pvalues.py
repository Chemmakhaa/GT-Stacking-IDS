"""Holm step-down adjustment from a list of raw p-values (one family of comparisons).

The input CSV must have two columns: comparison, p_value.
Procedure: sort the m p-values in increasing order, multiply the i-th one by
(m - i + 1), enforce monotonicity (running maximum), cap at 1.

Usage:
  python scripts/06_holm_from_pvalues.py --pvalues my_pvalues.csv
"""
import argparse

import pandas as pd
from statsmodels.stats.multitest import multipletests

p = argparse.ArgumentParser(description=__doc__)
p.add_argument("--pvalues", required=True)
p.add_argument("--alpha", type=float, default=0.05)
args = p.parse_args()

df = pd.read_csv(args.pvalues)
reject, p_holm, _, _ = multipletests(df["p_value"], alpha=args.alpha, method="holm")
df["p_holm"] = p_holm
df["significant"] = reject
out = args.pvalues.replace(".csv", "_holm.csv")
df.round(4).to_csv(out, index=False)
print(df.round(4).to_string(index=False))
print(f"Saved to {out}")
