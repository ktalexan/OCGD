# Import necessary libraries
from arcgis.features.feature import arcpy
import os
import sys
import datetime
import json
from pathlib import Path
import logging
import unicodedata
from typing import List, Union, Optional, Dict, Any
import re
import shutil
import importlib
import wmi
import pandas as pd
import requests
import arcpy
from arcpy import metadata as md
from arcgis.features import GeoAccessor, GeoSeriesAccessor
from dotenv import load_dotenv
from ocgd import OCACS

# Load environment variables from .env file
load_dotenv()

# Set pandas options
pd.options.mode.copy_on_write = True

# Set environment workspace to the current working directory
arcpy.env.workspace = os.getcwd()
arcpy.env.overwriteOutput = True

# Initialize OCACS instance
ocacs = OCACS(part= 1, version= 2026.1)

# Get the project metadata and directories from the OCACS class object
prj_meta = ocacs.prj_meta
prj_dirs = ocacs.prj_dirs

# Get the logger from the OCACS class object
logger = ocacs.logger


# Import the full inventory JSON file (if not already in memory)
with open(os.path.join(prj_dirs["codebook"], "octl_cb_twr.json"), "r", encoding = "utf-8") as f:
    cb = json.load(f)["series"]["ACS"]

# Get the octl OCACS geodatabases dictionary
gdb_dict = ocacs.octl_ocacs_dict()
# Get the years available in the octl OCACS geodatabases
gdb_years = [int(y) for y in sorted(gdb_dict.keys())]

for year in gdb_years:
    logger.enable(meta = prj_meta, filename = f"ocacs_data_processing_{year}.log", replace = True)
    print(f"OCACS {year} Geodatabase Processing Log\n")
    ocacs.process_acs_data(process_year = year, all_years = False)
    print(f"\nOCACS {year} Geodatabase processing completed. Check the log file for details.")
    logger.disable()



# geo_2012 = list(gdb_dict["2012"]["layers"].keys())
# fcs_2024 = list(gdb_dict["2024"]["layers"].values())

# # Get all geography codes from all the years in the OCACS geodatabases
# all_geo_codes = set()
# for year in gdb_years:
#     all_geo_codes.update(list(gdb_dict[str(year)]["layers"].keys()))
# print(sorted(all_geo_codes))

# # Get all feature class names from all the years in the OCACS geodatabases
# all_fcs_codes = set()
# for year in gdb_years:
#     all_fcs_codes.update(list(gdb_dict[str(year)]["layers"].values()))
# print(sorted(all_fcs_codes))


# # Extract the years available for the American Community Survey (ACS) from the codebook
# acs_years = [int(key) for key in list(cb.keys())]




# ocacs.process_acs_data(process_year = 2024, all_years = False)



# # If needed, construct the master OCACS variables codebook and write to file
# ocacs_cb_vars = ocacs.construct_master_variables_dict(write_to_file = True)

# # For each ACS5 year, fetch the CB variables, write to disk, and log the process
# for year in ocacs.acs5_years:
#     logger.enable(meta = prj_meta, filename = f"ocacs_cb_vars_{year}.log", replace = True)
#     print(f"OCACS {year} CB Variables Log\n")
#     cb_vars, df_cb_vars = ocacs.acs_cb_variables(year = year, write_to_disk = True)
#     print(f"\nOCACS {year} CB Variables fetch and write to disk completed. Check the log file for details.")
#     logger.disable()




# cb_acs = cb["series"]["ACS"]["2024"]["layers"]

# geo in [key["code"][:2] for key in cb_acs.values()]


# # Find the min and max years for the acs_years list
# range_acs_years = range(int(min(acs_years)), int(max(acs_years)) + 1)

# master_fc = []
# for year in acs_years:
#     gdb_path = os.path.join(prj_dirs["gis"], f"octl_ocacs{year}.gdb")
#     arcpy.env.workspace = gdb_path
#     for fc in arcpy.ListFeatureClasses():
#         if fc[:2] not in master_fc:
#             master_fc.append(fc[:2])
# master_fc.sort()
# print(master_fc)

# process_year = 2024
# all_years = False
# year = process_year
# fd = "Demographic"
# geo = "CO"

# ocacs.geographies

# # Import the full inventory JSON file (if not already in memory)
# with open(os.path.join(prj_dirs["codebook"], "octl_cb_twr.json"), "r", encoding = "utf-8") as f:
#     cb = json.load(f)["series"]["ACS"]

# cb_acs = cb["series"]["ACS"]["2024"]["layers"]

# for geo in ocacs.geographies:
#     if geo in [key["code"][:2] for key in cb_acs.values()]:
#         print(f"{geo} is in the codebook.")
#     else:
#         print(f"{geo} is NOT in the codebook.")


https://api.census.gov/data/2012/acs/acs5/geography.json


{
    "county": "050",
    "county subdivision": "060",
    "tract": "140",
    "place": "160",
    "consolidated city": "170",
    "metropolitan statistical area/micropolitan statistical area": "310",
    "metropolitan division": "314",
    "combined statistical area": "330",
    "urban area": "400",
    "congressional district": "500",
    "state legislative district (upper chamber)": "610",
    "state legislative district (lower chamber)": "620",
    "public use microdata area": "795",
    "zip code tabulation area": "860",
    "school district (elementary)": "950",
    "school district (secondary)": "960",
    "school district (unified)": "970"
}


# def get_census_geography_codes(year: int) -> Dict[str, Dict[str, str]]:
#     """
#     Fetches the geography codes from the Census API for a given year.

#     Parameters:
#     year (int): The year for which to fetch the geography codes.
#     api_key (str): The Census API key.

#     Returns:
#     Dict[str, Dict[str, str]]: A dictionary containing geography levels and their details.
#     """
#     api_key = os.getenv("CENSUS_API_KEY")
#     base_rest = f"https://api.census.gov/data/{year}/acs/acs5/geography.json"
#     base_params = {"f": "json", "key": api_key}

#     try:
#         response = requests.get(base_rest, params = base_params, timeout = 30)
#         response.raise_for_status()
#         data = response.json().get("fips", [])
        
#         geo_levels = {}
#         for item in data:
#             if int(item["geoLevelDisplay"]) < 50:
#                 continue
#             geo_levels[item["geoLevelDisplay"]] = {
#                 "name": item.get("name", ""),
#                 "requires": item.get("requires", ""),
#                 "wildcard": item.get("wildcard", ""),
#                 "optional": item.get("optionalWithWCFor", ""),
#                 "date": item.get("referenceDate", "")
#             }
#         return geo_levels

#     except requests.exceptions.RequestException as e:
#         print(f"Error fetching geography codes: {e}")
#         return {}

# # Example usage
# geo_levels = get_census_geography_codes(year = 2024)
# print(json.dumps(geo_levels, indent=4))




# ["50", "60", "140", "160", "170", "310", "314", "330", "400", "500", "610", "620", "795", "860", "950", "960", "970"]


# def get_census_geography_codes(year: int) -> Dict[str, Dict[str, str]]:
#     """
#     Fetches the geography codes from the Census API for a given year.

#     Parameters:
#     year (int): The year for which to fetch the geography codes.
#     api_key (str): The Census API key.

#     Returns:
#     Dict[str, Dict[str, str]]: A dictionary containing geography levels and their details.
#     """
#     api_key = os.getenv("CENSUS_API_KEY")
#     base_rest = f"https://api.census.gov/data/{year}/acs/acs5/geography.json"
#     base_params = {"f": "json", "key": api_key}

#     try:
#         response = requests.get(base_rest, params = base_params, timeout = 30)
#         response.raise_for_status()
#         data = response.json().get("fips", [])
        
#         geo_levels = {}

#         for item in data:
#             if int(item["geoLevelDisplay"]) < 50:
#                 continue
#             params = {"for": {item["name"]}, "in": {}}
#             if "state" in item["requires"]:
#                 params["in"]["state"] = "06"
#             if "county" in item["requires"]:
#                 params["in"]["county"] = "059"



#             geo_levels[item["geoLevelDisplay"]] = {
#                 "parameters": params,
#                 "name": item.get("name", ""),
#                 "requires": item.get("requires", ""),
#                 "wildcard": item.get("wildcard", ""),
#                 "optional": item.get("optionalWithWCFor", ""),
#                 "date": item.get("referenceDate", "")
#             }
#         return geo_levels

#     except requests.exceptions.RequestException as e:
#         print(f"Error fetching geography codes: {e}")
#         return {}

# # Example usage
# geo_levels = get_census_geography_codes(year = 2024)
# print(json.dumps(geo_levels, indent=4))


