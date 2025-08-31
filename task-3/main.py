"""Main runner for Cricket Fielding Analysis.

Usage:
- Run directly: python main.py
- Or import functions in notebooks.
"""

from __future__ import annotations

import argparse
import os
from typing import Optional

import pandas as pd

from data_collection import generate_sample_dataset, load_dataset, save_cleaned_data
from analysis import Weights, summarize_players
from visualization import plot_ps_bar
from report_generator import create_excel_report


def ensure_outputs_dir(path: str) -> None:
	if not os.path.exists(path):
		os.makedirs(path, exist_ok=True)


def run_analysis(dataset_path: Optional[str], output_dir: str, output_format: str = "csv") -> pd.DataFrame:
	"""Run the full pipeline: load/generate, analyze, save, visualize."""
	ensure_outputs_dir(output_dir)

	if dataset_path:
		df = load_dataset(dataset_path)
	else:
		df = generate_sample_dataset()

	# Save cleaned ball-by-ball data
	clean_path = os.path.join(output_dir, f"fielding_data.{output_format}")
	save_cleaned_data(df, clean_path)

	# Compute summary
	weights = Weights()  # Adjust here if needed
	summary_df = summarize_players(df, weights)

	# Save summary
	summary_out = os.path.join(output_dir, f"summary.{output_format}")
	if output_format == "csv":
		summary_df.to_csv(summary_out, index=True)
	else:
		summary_df.to_excel(summary_out, index=True)

	# Visualization
	fig_path = os.path.join(output_dir, "ps_bar_chart.png")
	plot_ps_bar(summary_df, fig_path)

	# Excel report
	report_path = os.path.join(output_dir, "fielding_report.xlsx")
	create_excel_report(df, summary_df, weights, report_path)

	return summary_df


def parse_args() -> argparse.Namespace:
	parser = argparse.ArgumentParser(description="Cricket Fielding Analysis")
	parser.add_argument("--dataset", type=str, default=None, help="Path to CSV/Excel dataset. If omitted, generates sample data.")
	parser.add_argument("--output-dir", type=str, default="outputs", help="Directory to save outputs.")
	parser.add_argument("--format", type=str, default="csv", choices=["csv", "xlsx", "xls"], help="Output file format for data and summary.")
	return parser.parse_args()


if __name__ == "__main__":
	args = parse_args()
	summary = run_analysis(args.dataset, args.output_dir, args.format)
	print("Summary (with PS):")
	print(summary)



