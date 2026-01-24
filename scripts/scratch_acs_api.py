from arcgis._impl.common._spatial import arcpy
import os
import sys
import urllib.request
import urllib.parse
import json
import sys
import requests
import arcpy
from arcgis.features import GeoAccessor, GeoSeriesAccessor
from dotenv import load_dotenv
load_dotenv()
from ocgd import OCacs

acs = OCacs(part= 1, version= 2026.1)
prj_meta = acs.prj_meta
prj_dirs = acs.prj_dirs


geoids_co = acs.get_geoids("2010", "CO")
geoids_cs = acs.get_geoids("2023", "CS")


# Original URL: https://api.census.gov/data/2023/acs/acs5/subject?get=NAME,S0101_C01_001E&for=county:059&in=state:06

# https://api.census.gov/data/2010/acs/acs5?get=group(B01001)&for=county:059&in=state:06

url = "https://api.census.gov/data/2010/acs/acs5?get=group(B01003)&for=county:059&in=state:06"


def get_response(url: str):
    with urllib.request.urlopen(url) as resp:
        charset = resp.headers.get_content_charset() or "utf-8"
        text = resp.read().decode(charset)
        raw = json.loads(text)
        # Census API returns a top-level list where the first sublist
        # is the headers and subsequent sublists are rows of values.
        if isinstance(raw, list) and len(raw) >= 1 and all(isinstance(r, list) for r in raw):
            headers = raw[0]
            rows = raw[1:]
            zipped_raw = [dict(zip(headers, row)) for row in rows]
            filtered_raw = []
            for item in zipped_raw:
                filtered_item = {k: v for k, v in item.items() if k == "GEO_ID" or (k.startswith("B01003") and k.endswith("E"))}
                filtered_raw.append(filtered_item)
            return filtered_raw
        return raw

data = get_response(url)
# For each item in data, only keep the keys and values where the key starts with 'B01003' or is 'GEO_ID'.
filtered_data = []
for item in data:
    filtered_item = {k: v for k, v in item.items() if k == "GEO_ID" or (k.startswith("B01003") and k.endswith("E"))}
    filtered_data.append(filtered_item)

print(json.dumps(filtered_data, indent=4))



# Census Documentation: https://www2.census.gov/data/api-documentation/api-user-guide.pdf

# Year used in the Census API path (appears after /data/)
year = 2023


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

data = fetch_census(year = 2023, table_id = "S0101", var_id = "C01_001E", geography = "cousub")
print(json.dumps(data, indent=4))

data = fetch_census(year = 2023, table_id = "S0101", var_id = "C01_001E", geography = "tract")
print(json.dumps(data, indent=4))

data = fetch_census(year = 2023, table_id = "S0101", var_id = "C01_001E", geography = "place")
print(json.dumps(data, indent=4))

data = fetch_census(year = 2023, table_id = "S0101", var_id = "C01_001E", geography = "congressional district")
print(json.dumps(data, indent=4))


data2 = fetch_census(year = 2010, table_id = "S0101", geography = "county")
print(json.dumps(data2, indent=4))

def fetch_acs_variables(year: int):
    """Fetch ACS variable metadata using requests (external dependency)."""
    url = f"https://api.census.gov/data/{year}/acs/acs5/variables.json"
    resp = requests.get(url, timeout = 10)
    resp.raise_for_status()
    return resp.json()

acs_vars_2023 = fetch_acs_variables(2023)
print(json.dumps(acs_vars_2023, indent=4))

# Convert the acs_vars_2023 dict to a pandas DataFrame for easier viewing, where the keys are the variable rows and the values are the columns.
import pandas as pd
df = pd.DataFrame.from_dict(acs_vars_2023['variables'], orient='index')
print(df)



