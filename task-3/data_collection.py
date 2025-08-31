"""Data collection and loading utilities for Cricket Fielding Analysis.

This module provides:
- generate_sample_dataset: Create a sample ball-by-ball dataset for three players
- load_dataset: Load CSV/Excel dataset into a pandas DataFrame
- save_cleaned_data: Save the cleaned/processed dataset to CSV/Excel
"""

from __future__ import annotations

import os
from typing import Optional

import pandas as pd


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
]


def _ensure_parent_directory(path: str) -> None:
	"""Create parent directories for a file path if they do not exist."""
	directory = os.path.dirname(path)
	if directory and not os.path.exists(directory):
		os.makedirs(directory, exist_ok=True)


def generate_sample_dataset() -> pd.DataFrame:
	"""Generate a small sample dataset for three players (dummy data).

	Returns
	-------
	pd.DataFrame
		A DataFrame with the required schema and plausible dummy values.
	"""
	data = [
		# Player A (Wicketkeeper)
		{"Match No.": 1, "Innings": 1, "Team": "ShadowFox XI", "Player Name": "Player A", "Ballcount": 1, "Position": "WK", "Short Description": "clean take, quick release", "Pick": "clean pick", "Throw": "", "Runs": 1, "Overcount": "0.1", "Venue": "Alpha Stadium"},
		{"Match No.": 1, "Innings": 1, "Team": "ShadowFox XI", "Player Name": "Player A", "Ballcount": 2, "Position": "WK", "Short Description": "direct hit attempt, missed by inches", "Pick": "good throw", "Throw": "missed run out", "Runs": -1, "Overcount": "0.2", "Venue": "Alpha Stadium"},
		{"Match No.": 1, "Innings": 1, "Team": "ShadowFox XI", "Player Name": "Player A", "Ballcount": 3, "Position": "WK", "Short Description": "quick stumping", "Pick": "clean pick", "Throw": "stumping", "Runs": 0, "Overcount": "2.4", "Venue": "Alpha Stadium"},

		# Player B (Inner ring fielder)
		{"Match No.": 1, "Innings": 1, "Team": "ShadowFox XI", "Player Name": "Player B", "Ballcount": 4, "Position": "Point", "Short Description": "dive stop, saved a certain single", "Pick": "clean pick", "Throw": "", "Runs": 1, "Overcount": "3.2", "Venue": "Alpha Stadium"},
		{"Match No.": 1, "Innings": 1, "Team": "ShadowFox XI", "Player Name": "Player B", "Ballcount": 5, "Position": "Point", "Short Description": "bullet throw to bowler, direct hit!", "Pick": "good throw", "Throw": "run out", "Runs": 0, "Overcount": "4.1", "Venue": "Alpha Stadium"},
		{"Match No.": 1, "Innings": 1, "Team": "ShadowFox XI", "Player Name": "Player B", "Ballcount": 6, "Position": "Point", "Short Description": "dropped a tough chance", "Pick": "drop catch", "Throw": "", "Runs": -2, "Overcount": "5.6", "Venue": "Alpha Stadium"},

		# Player C (Boundary rider)
		{"Match No.": 1, "Innings": 1, "Team": "ShadowFox XI", "Player Name": "Player C", "Ballcount": 7, "Position": "Long-on", "Short Description": "catch taken near boundary", "Pick": "catch", "Throw": "", "Runs": 0, "Overcount": "10.3", "Venue": "Alpha Stadium"},
		{"Match No.": 1, "Innings": 1, "Team": "ShadowFox XI", "Player Name": "Player C", "Ballcount": 8, "Position": "Long-on", "Short Description": "misfield near rope", "Pick": "fumble", "Throw": "", "Runs": -1, "Overcount": "12.5", "Venue": "Alpha Stadium"},
		{"Match No.": 1, "Innings": 1, "Team": "ShadowFox XI", "Player Name": "Player C", "Ballcount": 9, "Position": "Long-on", "Short Description": "rocket arm, batsman stayed home", "Pick": "good throw", "Throw": "", "Runs": 1, "Overcount": "14.2", "Venue": "Alpha Stadium"},
	]

	df = pd.DataFrame(data, columns=REQUIRED_COLUMNS)
	return df


def load_dataset(path: str) -> pd.DataFrame:
	"""Load a dataset from CSV or Excel.

	Parameters
	----------
	path : str
		File path to CSV (.csv) or Excel (.xlsx, .xls).

	Returns
	-------
	pd.DataFrame
		DataFrame containing the dataset with required columns.

	Raises
	------
	ValueError
		If the file extension is unsupported or columns are missing.
	"""
	if not os.path.exists(path):
		raise ValueError(f"Dataset not found at: {path}")

	_, ext = os.path.splitext(path.lower())
	if ext == ".csv":
		df = pd.read_csv(path)
	elif ext in {".xlsx", ".xls"}:
		df = pd.read_excel(path)
	else:
		raise ValueError("Unsupported file type. Use CSV or Excel.")

	missing = [c for c in REQUIRED_COLUMNS if c not in df.columns]
	if missing:
		raise ValueError(f"Dataset missing required columns: {missing}")

	return df


def save_cleaned_data(df: pd.DataFrame, path: str) -> None:
	"""Save DataFrame to CSV or Excel, inferring by file extension."""
	_ensure_parent_directory(path)
	_, ext = os.path.splitext(path.lower())
	if ext == ".csv":
		df.to_csv(path, index=False)
	elif ext in {".xlsx", ".xls"}:
		df.to_excel(path, index=False)
	else:
		raise ValueError("Unsupported output type. Use CSV or Excel.")


__all__ = [
	"REQUIRED_COLUMNS",
	"generate_sample_dataset",
	"load_dataset",
	"save_cleaned_data",
]



