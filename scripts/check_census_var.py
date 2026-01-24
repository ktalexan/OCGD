#!/usr/bin/env python3
"""
check_census_var.py

Given a year and a Census variable key, fetch the variable metadata from
the Census API variables endpoint and print a JSON object with the
relevant fields (label, concept, predicateType, group, limit, attributes).

Usage: python check_census_var.py 2019 B01001_001E

This script is written to be importable; call `get_variable_metadata(year, key)`
from other scripts to programmatically obtain metadata.
"""
from __future__ import annotations

import json
import sys
from functools import lru_cache
from typing import Any, Dict, Optional

try:
    import requests
except Exception:
    requests = None


@lru_cache(maxsize=8)
def _fetch_variables_for_year(year: int) -> Optional[Dict[str, Any]]:
    """Fetch and return the variables.json dict for the given ACS year.

    Returns the parsed JSON dictionary or None on failure.
    """
    url = f"https://api.census.gov/data/{year}/acs/acs5/variables.json"
    try:
        if requests:
            resp = requests.get(url, timeout=30)
            resp.raise_for_status()
            return resp.json().get("variables", {})
        # fallback to urllib
        from urllib.request import urlopen

        with urlopen(url, timeout=30) as fh:
            data = json.load(fh)
            return data.get("variables", {})
    except Exception:
        return None


def get_variable_metadata(year: int, var_key: str) -> Optional[Dict[str, Any]]:
    """Return metadata for `var_key` in the given `year`.

    The returned dict contains at least: label, concept, predicateType,
    group, limit, attributes. Returns None if the variable is not present
    for that year or on fetch error.
    """
    vars_for_year = _fetch_variables_for_year(year)
    if not vars_for_year:
        return None
    meta = vars_for_year.get(var_key)
    if not meta:
        return None
    # Extract expected keys with safe defaults
    return {
        "label": meta.get("label", ""),
        "concept": meta.get("concept", ""),
        "predicateType": meta.get("predicateType", ""),
        "group": meta.get("group", ""),
        "limit": meta.get("limit", ""),
        "attributes": meta.get("attributes", {}),
    }


def _cli_main(argv: list[str]) -> int:
    if len(argv) != 3:
        print("Usage: check_census_var.py YEAR VAR_KEY", file=sys.stderr)
        return 2
    year = int(argv[1])
    var_key = argv[2]
    meta = get_variable_metadata(year, var_key)
    if meta is None:
        # No output when not found; exit 1 for programmatic use
        return 1
    print(json.dumps(meta, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(_cli_main(sys.argv))
