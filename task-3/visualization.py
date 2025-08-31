"""Visualization helpers for Cricket Fielding Analysis."""

from __future__ import annotations

from typing import Optional

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd


def plot_ps_bar(summary_df: pd.DataFrame, output_path: Optional[str] = None) -> plt.Figure:
	"""Create a bar chart comparing players' Performance Scores (PS).

	Parameters
	----------
	summary_df : pd.DataFrame
		DataFrame with index as player names and a 'PS' column.
	output_path : Optional[str]
		If provided, saves the figure to this path (PNG recommended).

	Returns
	-------
	matplotlib.figure.Figure
		The created figure.
	"""
	sns.set(style="whitegrid")
	fig, ax = plt.subplots(figsize=(8, 5))

	data = summary_df.reset_index().rename(columns={"index": "Player Name"})
	sns.barplot(data=data, x="Player Name", y="PS", ax=ax, palette="viridis")
	ax.set_title("Fielding Performance Score (PS) by Player")
	ax.set_xlabel("Player")
	ax.set_ylabel("Performance Score (PS)")
	for p in ax.patches:
		height = p.get_height()
		ax.annotate(f"{height:.1f}", (p.get_x() + p.get_width() / 2, height),
					 ha="center", va="bottom", fontsize=9)

	plt.tight_layout()
	if output_path:
		fig.savefig(output_path, dpi=150)
	return fig


__all__ = ["plot_ps_bar"]



