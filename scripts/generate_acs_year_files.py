#!/usr/bin/env python3
"""
generate_acs_year_files.py

Reads `codebook/acs_variables_master.json`, creates year-specific copies
for ACS years 2010 through 2023, and filters/updates variables using the
`check_census_var` module. Invalid variables for a year are removed; valid
variables have their metadata fields updated per instructions.

Usage: python generate_acs_year_files.py

Note: This script imports `.github/scripts/check_census_var.py` which
queries the Census API. A working internet connection is required to
validate variables against the Census variables endpoint.
"""
from __future__ import annotations

import json
import sys
from copy import deepcopy
from pathlib import Path
from typing import Any, Dict

ROOT = Path(__file__).resolve().parents[1]
MASTER_PATH = ROOT / "codebook" / "acs_variables_master.json"

try:
    from .check_census_var import get_variable_metadata
except Exception:
    # allow running the script when executed from repo root
    from check_census_var import get_variable_metadata  # type: ignore


def sentence_case(s: str) -> str:
    """Convert a string to sentence case: first char upper, rest lower."""
    if not s:
        return s
    s = s.strip()
    return s[0].upper() + s[1:].lower() if len(s) > 1 else s.upper()


def process_year(year: int, master: Dict[str, Any]) -> Dict[str, Any]:
    """Create a filtered/updated variables dict for `year` from `master`."""
    out: Dict[str, Any] = {}
    for category, vars_dict in master.items():
        # vars_dict expected to be a dict mapping var_key -> metadata
        new_vars: Dict[str, Any] = {}
        for var_key, var_meta in vars_dict.items():
            meta = get_variable_metadata(year, var_key)
            if meta is None:
                # variable not valid for this year; skip
                continue
            # start with a deepcopy of the original entry and update
            entry = deepcopy(var_meta)
            entry["label"] = meta.get("label", "")
            entry["group_category"] = sentence_case(meta.get("concept", ""))
            entry["type"] = meta.get("predicateType", "")
            entry["group"] = meta.get("group", "")
            entry["limit"] = meta.get("limit", "")
            entry["attributes"] = meta.get("attributes", "")
            new_vars[var_key] = entry
        if new_vars:
            out[category] = new_vars
    return out


def main() -> int:
    if not MASTER_PATH.exists():
        print(f"Master file not found: {MASTER_PATH}", file=sys.stderr)
        return 2
    with MASTER_PATH.open("r", encoding="utf-8") as fh:
        master = json.load(fh)

    years = list(range(2010, 2024))
    for year in years:
        print(f"Processing year {year}...")
        year_data = process_year(year, master)
        out_path = ROOT / "codebook" / f"acs_variables_{year}.json"
        with out_path.open("w", encoding="utf-8") as fh:
            json.dump(year_data, fh, ensure_ascii=False, indent=2)
        print(f"Wrote {out_path}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
