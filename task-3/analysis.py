"""Analysis utilities for Cricket Fielding Performance Score (PS).

This module computes per-player fielding action counts and PS using
user-defined weights.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Tuple

import pandas as pd


@dataclass(frozen=True)
class Weights:
	"""Weights for the PS components."""
	WCP: float = 0.5
	WGT: float = 1.0
	WC: float = 3.0
	WDC: float = -2.0
	WST: float = 2.5
	WRO: float = 2.5
	WMRO: float = -1.0
	WDH: float = 1.5


def compute_action_counts(df: pd.DataFrame) -> pd.DataFrame:
	"""Compute per-player counts for each fielding action and runs saved.

	The schema is expected to have columns: 'Player Name', 'Pick', 'Throw', 'Runs'.

	Returns a DataFrame indexed by player with columns:
	['CP','GT','C','DC','ST','RO','MRO','DH','RS']
	"""
	# Normalize strings to lower for robust matching
	working = df.copy()
	for col in ["Pick", "Throw"]:
		working[col] = working[col].fillna("").str.strip().str.lower()

	# Map conditions
	cp = (working["Pick"] == "clean pick").groupby(working["Player Name"]).sum()
	gt = (working["Pick"] == "good throw").groupby(working["Player Name"]).sum()
	c_catch = (working["Pick"] == "catch").groupby(working["Player Name"]).sum()
	dc = (working["Pick"] == "drop catch").groupby(working["Player Name"]).sum()
	st = (working["Throw"] == "stumping").groupby(working["Player Name"]).sum()
	ro = (working["Throw"] == "run out").groupby(working["Player Name"]).sum()
	mro = (working["Throw"] == "missed run out").groupby(working["Player Name"]).sum()
	dh = (working["Short Description"].fillna("").str.lower().str.contains("direct hit")).groupby(working["Player Name"]).sum()

	# Runs saved (positive saves, negative conceded). Sum as-is
	rs = working.groupby("Player Name")["Runs"].sum()

	# Combine to one DataFrame, fill missing with zeros
	result = pd.concat(
		[
			cp.rename("CP"),
			gt.rename("GT"),
			c_catch.rename("C"),
			dc.rename("DC"),
			st.rename("ST"),
			ro.rename("RO"),
			mro.rename("MRO"),
			dh.rename("DH"),
			rs.rename("RS"),
		],
		axis=1,
	).fillna(0).astype({"CP": int, "GT": int, "C": int, "DC": int, "ST": int, "RO": int, "MRO": int, "DH": int, "RS": float})

	return result


def compute_ps(counts_df: pd.DataFrame, weights: Weights) -> pd.DataFrame:
	"""Compute Performance Score (PS) per player.

	PS = (CP×WCP) + (GT×WGT) + (C×WC) + (DC×WDC) + (ST×WST)
	     + (RO×WRO) + (MRO×WMRO) + (DH×WDH) + RS

	Returns the input DataFrame with an added 'PS' column.
	"""
	df = counts_df.copy()
	df["PS"] = (
		df["CP"] * weights.WCP
		+ df["GT"] * weights.WGT
		+ df["C"] * weights.WC
		+ df["DC"] * weights.WDC
		+ df["ST"] * weights.WST
		+ df["RO"] * weights.WRO
		+ df["MRO"] * weights.WMRO
		+ df["DH"] * weights.WDH
		+ df["RS"]
	)
	return df


def summarize_players(df: pd.DataFrame, weights: Weights) -> pd.DataFrame:
	"""Convenience: from raw dataset to summary with PS."""
	counts = compute_action_counts(df)
	return compute_ps(counts, weights)


__all__ = [
	"Weights",
	"compute_action_counts",
	"compute_ps",
	"summarize_players",
]



