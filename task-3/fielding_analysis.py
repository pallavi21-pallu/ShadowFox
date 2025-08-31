"""Cricket Fielding Analysis (single-file version).

Reads a CSV of ball-by-ball fielding events, aggregates per-player metrics,
computes Performance Score (PS) using specified weights, and writes a
Performance Matrix as CSV and Excel. Optionally emits a PS bar chart.

Usage (PowerShell):
  python fielding_analysis.py --input .\fielding_data.csv --outdir .\outputs --chart
"""

from __future__ import annotations

import argparse
import os
from dataclasses import dataclass
from typing import Optional

import pandas as pd

try:
	import seaborn as sns  # optional
	import matplotlib.pyplot as plt
	_HAS_PLOTTING = True
except Exception:
	_HAS_PLOTTING = False


REQUIRED_COLUMNS = [
	"Match No.",
	"Innings",
	"Team",
	"Player Name",
	"Ballcount",
	"Position",
	"Short Description",
	"Pick",
	"Throw",
	"Runs",
	"Overcount",
	"Venue",
	"Stadium",
]


@dataclass(frozen=True)
class Weights:
	WCP: float = 1.0
	WGT: float = 1.0
	WC: float = 3.0
	WDC: float = -3.0
	WST: float = 3.0
	WRO: float = 3.0
	WMRO: float = -2.0
	WDH: float = 2.0


def load_csv(path: str) -> pd.DataFrame:
	if not os.path.exists(path):
		raise FileNotFoundError(f"Input file not found: {path}")
	df = pd.read_csv(path)
	missing = [c for c in REQUIRED_COLUMNS if c not in df.columns]
	if missing:
		raise ValueError(f"Dataset missing required columns: {missing}")
	return df


def compute_matrix(df: pd.DataFrame, weights: Weights) -> pd.DataFrame:
	working = df.copy()
	for col in ["Pick", "Throw", "Short Description"]:
		working[col] = working[col].fillna("").str.strip().str.lower()

	group = working.groupby("Player Name")
	matrix = pd.DataFrame(index=group.size().index)
	matrix.index.name = "Player Name"

	matrix["CP"] = group.apply(lambda g: (g["Pick"] == "clean pick").sum())
	matrix["GT"] = group.apply(lambda g: (g["Pick"] == "good throw").sum())
	matrix["C"] = group.apply(lambda g: (g["Pick"] == "catch").sum())
	matrix["DC"] = group.apply(lambda g: (g["Pick"] == "drop catch").sum())
	matrix["ST"] = group.apply(lambda g: (g["Throw"] == "stumping").sum())
	matrix["RO"] = group.apply(lambda g: (g["Throw"] == "run out").sum())
	matrix["MRO"] = group.apply(lambda g: (g["Throw"] == "missed run out").sum())
	matrix["DH"] = group.apply(lambda g: g["Short Description"].str.contains("direct hit").sum())
	matrix["RS"] = group["Runs"].sum()

	matrix["PS"] = (
		matrix["CP"] * weights.WCP
		+ matrix["GT"] * weights.WGT
		+ matrix["C"] * weights.WC
		+ matrix["DC"] * weights.WDC
		+ matrix["ST"] * weights.WST
		+ matrix["RO"] * weights.WRO
		+ matrix["MRO"] * weights.WMRO
		+ matrix["DH"] * weights.WDH
		+ matrix["RS"]
	)
	return matrix.reset_index()


def save_outputs(matrix: pd.DataFrame, outdir: str) -> None:
	os.makedirs(outdir, exist_ok=True)
	matrix.to_csv(os.path.join(outdir, "performance_matrix.csv"), index=False)
	try:
		matrix.to_excel(os.path.join(outdir, "performance_matrix.xlsx"), index=False)
	except Exception as e:
		print("Warning: Excel export failed (install openpyxl).", e)


def maybe_plot(matrix: pd.DataFrame, outdir: str) -> Optional[str]:
	if not _HAS_PLOTTING:
		return None
	sns.set(style="whitegrid")
	fig, ax = plt.subplots(figsize=(8, 5))
	sns.barplot(data=matrix, x="Player Name", y="PS", ax=ax, legend=False)
	for p in ax.patches:
		height = p.get_height()
		ax.annotate(f"{height:.1f}", (p.get_x() + p.get_width()/2, height), ha="center", va="bottom", fontsize=9)
	plt.title("Fielding Performance Score (PS)")
	plt.tight_layout()
	path = os.path.join(outdir, "performance_ps_chart.png")
	fig.savefig(path, dpi=150)
	plt.close(fig)
	return path


def parse_args() -> argparse.Namespace:
	parser = argparse.ArgumentParser(description="Cricket Fielding Analysis")
	parser.add_argument("--input", type=str, required=True, help="Path to fielding_data.csv")
	parser.add_argument("--outdir", type=str, default="outputs", help="Output directory")
	parser.add_argument("--chart", action="store_true", help="Also save PS bar chart")
	return parser.parse_args()


if __name__ == "__main__":
	args = parse_args()
	df = load_csv(args.input)
	w = Weights()
	matrix = compute_matrix(df, w)
	save_outputs(matrix, args.outdir)
	chart_path = maybe_plot(matrix, args.outdir) if args.chart else None
	print("Saved:")
	print(os.path.join(args.outdir, "performance_matrix.csv"))
	print(os.path.join(args.outdir, "performance_matrix.xlsx"))
	if chart_path:
		print(chart_path)

