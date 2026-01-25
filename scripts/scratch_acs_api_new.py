from __future__ import annotations
import os
import json
from typing import List, Dict, Optional, Union
import requests
from dotenv import load_dotenv
load_dotenv()
from ocgd import OCacs

acs = OCacs(part=1, version=2026.1)

# Get the project metadata and directories from the OCACS class object
prj_meta = acs.prj_meta
prj_dirs = acs.prj_dirs

# https://api.census.gov/data/2010/acs/acs5?get=NAME,B00001_001E&for=county%20subdivision:*&in=state:06&in=county:059&key=YOUR_KEY_HERE

def fetch_acs_api(
	year: int,
	variables: List[str],
	geography: str = "CO",
	chunk_size: int = 49,
) -> List[Dict[str, str]]:
	"""Fetch ACS data for a given year and list of variables.

	This function will chunk requests when `variables` is large and merge
	results by `GEO_ID` so the caller receives a single record per geography
	with all requested variables.

	Args:
		year: ACS year (e.g., 2010).
		variables: List of ACS variable codes (e.g., ["B01003_001E"]).
		for_clause: Value for the `for` parameter (e.g., "county:059").
		in_clause: Value for the `in` parameter (e.g., "state:06").
		chunk_size: Number of variables per API request (default 50).

	Returns:
		List of dictionaries mapping header->value for each geography.
	"""
	api_key = os.getenv("CENSUS_API_KEY1")
	if not api_key:
		raise RuntimeError("Environment variable CENSUS_API_KEY1 is not set")

	if not isinstance(variables, (list, tuple)):
		raise TypeError("variables must be a list or tuple of ACS variable codes")

	base_url = f"https://api.census.gov/data/{year}/acs/acs5"

	# Census API accepts a maximum of 50 fields per request including GEO_ID.
	# Ensure we chunk variables so that each request has at most 49 variables
	# plus the GEO_ID field.
	chunk_size = min(int(chunk_size), 49)
	# Prepare chunks (exclude GEO_ID from chunking)
	def _chunk_list_local(items: List[str], size: int) -> List[List[str]]:
		return [items[i : i + size] for i in range(0, len(items), size)]

	chunks = _chunk_list_local(list(variables), chunk_size)

	merged: Dict[str, Dict[str, str]] = {}

	match geography:
		case "CO":
			print("Fetching county data")
			geoids = acs.get_geoids(str(year), "CO")
			for_clause = "county:059"
			in_clause = "state:06"
		case "CS":
			print("Fetching county subdivision data")
			geoids = acs.get_geoids(str(year), "CS")
			for_clause = "county subdivision:*"
			in_clause = ["state:06", "county:059"]

	for chunk in chunks:
		get_vars = ",".join(["GEO_ID"] + chunk)
		# Build params as a list of tuples so repeated keys (e.g. multiple
		# 'in=' parameters) are preserved in the query string.
		params_list = [("get", get_vars), ("key", api_key)]

		# 'for' is a single value (string)
		if for_clause:
			params_list.append(("for", for_clause))

		# Support multiple 'in' values by repeating the 'in' parameter.
		if in_clause:
			if isinstance(in_clause, (list, tuple)):
				for val in in_clause:
					params_list.append(("in", val))
			else:
				params_list.append(("in", in_clause))

		resp = requests.get(base_url, params=params_list, timeout=60)
		resp.raise_for_status()

		try:
			data = resp.json()
		except ValueError:
			raise RuntimeError("Invalid JSON response from Census API")

		if not data or len(data) < 2:
			continue

		headers = data[0]
		for row in data[1:]:
			rec = dict(zip(headers, row))
			geo_id = rec.get("GEO_ID")
			if geo_id is None:
				# skip malformed row
				continue
			if geo_id not in merged:
				merged[geo_id] = {}
			# Only keep GEO_ID and variables requested by the caller
			allowed = set(variables)
			filtered = {k: v for k, v in rec.items() if k == "GEO_ID" or k in allowed}
			merged[geo_id].update(filtered)
	
	# Get the merged response list
	merged_list = list(merged.values())

	# If any of the merged_ids are not in the geoids["values"], remove it from the merged_list
	final_list = [rec for rec in merged_list if rec["GEO_ID"].split("US")[-1] in geoids["values"]]

	# Count of final_list and geoids
	len_final = len(final_list)
	len_geoids = len(geoids["values"])

	# Get counts of variables in each record (excluding GEO_ID)
	raw_counts =[len(d) - 1 for d in final_list]
	# Make sure all counts are the same
	if len(set(raw_counts)) == 1:
		print(f"Response has {len_final} records (of {len_geoids} in the TigerLine geodatabase) with {raw_counts[0]} variables each.")
	elif len(set(raw_counts)) > 1:
		print("Warning: Inconsistent variable counts in final_list")
	
	# Return list of filtered records
	return final_list

sample_vars = acs.get_acs_list(2010, "Demographic")[:20]
res = fetch_acs_api(year = 2010, variables = sample_vars, geography = "CO")
print(json.dumps(res[:3], indent=2))

sample_vars = acs.get_acs_list(2010, "Demographic")
res = fetch_acs_api(year = 2010, variables = sample_vars, geography = "CO")
print(json.dumps(res[:3], indent=2))

res = fetch_acs_api(year = 2010, variables = sample_vars, geography = "CS")
print(json.dumps(res[:3], indent=2))




def fetch_census(year: int, table_id: str, var_id: str = None, geography: str = "county"):
    """Fetch JSON from the Census API using urllib (no external deps).

    Args:
        get_vars: comma-separated variables for `get` param.
        for_clause: the `for` query value (e.g., 'county:059').
        in_clause: the `in` query value (e.g., 'state:06').

    Returns:
        Parsed JSON response.

    Raises:
        urllib.error.HTTPError on HTTP failures.
        json.JSONDecodeError if response isn't valid JSON.
    """
    year = str(year)
    geoids = dict()

    # If var_id is provided, construct get_vars accordingly
    get_vars = f"NAME,group({table_id})"
    if var_id:
        get_vars = f"NAME,{table_id}_{var_id}"

    base = f"https://api.census.gov/data/{year}/acs/acs5/subject"

    match geography:
        case "CO":
            print("Fetching county data")
            geoids = acs.get_geoids(str(year), "CO")
            params = {
                "get": get_vars,
                "for": "county:059",
                "in": "state:06"
            }
        case "CS":
            print("Fetching county subdivision data")
            geoids = acs.get_geoids(str(year), "CS")
            params = {
                "get": get_vars,
                "for": "county subdivision:*",
                "in": ["state:06", "county:059"]
            }
        case "TR":
            print("Fetching census tract data")
            geoids = acs.get_geoids(str(year), "TR")
            params = {
                "get": get_vars,
                "for": "tract:*",
                "in": ["state:06", "county:059"]
            }
        case "PL":
            print("Fetching cities or places data")
            geoids = acs.get_geoids(str(year), "PL")
            params = {
                "get": get_vars,
                "for": "place:*",
                "in": "state:06"
            }
        case "CD":
            print("Fetching congressional district data")
            geoids = acs.get_geoids(str(year), "CD")
            params = {
                "get": get_vars,
                "for": "congressional district:*",
                "in": "state:06"
            }
        case "ZC":
            print("Fetching zip code tabulation areas data")
            geoids = acs.get_geoids(str(year), "ZC")
            params = {
                "get": get_vars,
                "for": "zip code tabulation area:*"
            }
        case "LL":
            print("Fetching state assembly legislative districts (lower) data")
            geoids = acs.get_geoids(str(year), "LL")
            params = {
                "get": get_vars,
                "for": "state assembly district:*",
                "in": "state:06"
            }
        case "LU":
            print("Fetching state senate legislative districts (upper) data")
            geoids = acs.get_geoids(str(year), "LU")
            params = {
                "get": get_vars,
                "for": "state senate district:*",
                "in": "state:06"
            }
        case "SE":
            print("Fetching elementary school district data")
            geoids = acs.get_geoids(str(year), "SE")
            params = {
                "get": get_vars,
                "for": "school district (unified):*",
                "in": ["state:06", "county:059"]
            }
        case "SS":
            print("Fetching secondary school district data")
            geoids = acs.get_geoids(str(year), "SS")
            params = {
                "get": get_vars,
                "for": "school district (secondary):*",
                "in": ["state:06", "county:059"]
            }
        case "SU":
            print("Fetching unified school district data")
            geoids = acs.get_geoids(str(year), "SU")
            params = {
                "get": get_vars,
                "for": "school district (unified):*",
                "in": ["state:06", "county:059"]
            }
        case "UA":
            print("Fetching urban area data")
            geoids = acs.get_geoids(str(year), "UA")
            params = {
                "get": get_vars,
                "for": "urban area:*",
                "in": "state:06"
            }
        case "PU":
            print("Fetching public use microdata area data")
            geoids = acs.get_geoids(str(year), "PU")
            params = {
                "get": get_vars,
                "for": "public use microdata area:*",
                "in": "state:06"
            }
        case "BG":
            print("Fetching block group data")
            geoids = acs.get_geoids(str(year), "BG")
            params = {
                "get": get_vars,
                "for": "block group:*",
                "in": ["state:06", "county:059"]
            }
        case _:
            raise ValueError(f"Unsupported geography: {geography}")

    # Use doseq=True so sequence values (like multiple `in` clauses)
    # produce repeated query keys: &in=state:06&in=county:059
    url = base + "?" + urllib.parse.urlencode(params, doseq=True)
    try:
        with urllib.request.urlopen(url) as resp:
            charset = resp.headers.get_content_charset() or "utf-8"
            text = resp.read().decode(charset)
            raw = json.loads(text)
            # Census API returns a top-level list where the first sublist
            # is the headers and subsequent sublists are rows of values.
            if isinstance(raw, list) and len(raw) >= 1 and all(isinstance(r, list) for r in raw):
                headers = raw[0]
                rows = raw[1:]
                return [dict(zip(headers, row)) for row in rows]
            return raw
    except urllib.error.HTTPError as e:
        print(f"HTTP Error: {e.code} {e.reason}", file=sys.stderr)
        try:
            body = e.read().decode("utf-8", errors="replace")
            print(body, file=sys.stderr)
        except (UnicodeDecodeError, ValueError, TypeError, AttributeError):
            pass
        raise


data = fetch_census(year = 2023, table_id = "S0101", var_id = "C01_001E", geography = "county")
print(json.dumps(data, indent=4))

