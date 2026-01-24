import argparse
import json
import sys
from typing import Dict, Optional

import requests


def get_census_variable_info(year: str, var: str, timeout: int = 20) -> Optional[Dict]:
    """Fetch variable metadata from the Census API for a given year and variable.

    Args:
        year: Year portion to insert into the API URL (e.g. '2010').
        var: Variable name to look up (e.g. 'B01001_001E').
        timeout: Request timeout in seconds.

    Returns:
        A dict with the variable metadata (keys: name, label, concept, predicateType,
        group, limit, attributes) or `None` if the variable is not found.

    Raises:
        requests.RequestException: On network / HTTP errors.
        ValueError: If the response JSON is malformed.
    """
    url = f"https://api.census.gov/data/{year}/acs/acs5/variables.json"
    r = requests.get(url, timeout=timeout)
    r.raise_for_status()
    payload = r.json()
    variables = payload.get("variables", {})
    v = variables.get(var)
    if not v:
        return None

    return {
        "name": var,
        "label": v.get("label"),
        "concept": v.get("concept"),
        "predicateType": v.get("predicateType"),
        "group": v.get("group"),
        "limit": v.get("limit"),
        "attributes": v.get("attributes"),
    }


def _cli():
    p = argparse.ArgumentParser(description="Check Census variable metadata for a given year")
    p.add_argument("year", help="Year portion for the API URL (e.g. 2010)")
    p.add_argument("var", help="Variable name to look up (e.g. B01001_001E)")
    args = p.parse_args()

    try:
        res = get_census_variable_info(args.year, args.var)
    except Exception as e:
        print("ERROR:", e)
        sys.exit(2)

    if res is None:
        print(f"{args.var} not found for year {args.year}")
        sys.exit(1)

    print(json.dumps(res, indent=2))


if __name__ == "__main__":
    _cli()
