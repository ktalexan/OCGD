# Import necessary libraries
from arcgis.features.feature import json
import os
import sys
import datetime
import json
from pathlib import Path
import shutil
import importlib
import re
import requests
import wmi
import pandas as pd
import arcpy
from arcpy import metadata as md
from arcgis.features import FeatureLayer # for REST API interaction
from arcgis.features import GeoAccessor, GeoSeriesAccessor
from dotenv import load_dotenv
from ocgd import OCTL

# Load environment variables from .env file
load_dotenv()

# Set pandas options
pd.options.mode.copy_on_write = True

# Set environment workspace to the current working directory
arcpy.env.workspace = os.getcwd()
arcpy.env.overwriteOutput = True

# Initialize OCTL instance
octl = OCTL(part= 1, version= 2026.1)

# Get the project metadata and directories from the OCTL class object
prj_meta = octl.prj_meta
prj_dirs = octl.prj_dirs

# Get the spatial reference from the OCTL class object (Web Mercator, WKID 3857)
out_sr = octl.sr

# Initialize the logger from the OCTL class object 
logger = octl.logger


# Import the full inventory JSON file (if not already in memory)
with open(os.path.join(prj_dirs["codebook"], "octl_cb_twr.json"), "r", encoding = "utf-8") as f:
    cb = json.load(f)

acs_years = list(cb["series"]["ACS"].keys())
range_acs_years = range(int(min(acs_years)), int(max(acs_years)) + 1)

cb_acs = dict()
for year in range_acs_years:
    if str(year) not in acs_years:
        # find the closest year in acs_years to the current year
        year_to_use = str(min(acs_years, key = lambda x: abs(int(x) - year)))
    else:
        year_to_use = str(year)
    print(f"Adding year: {year} (from year: {year_to_use})")
    # Replace layer subkeys with their internal `code` value where available
    layers = cb["series"]["ACS"][year_to_use]["layers"]
    mapped_layers = {}
    for layer_name, layer_val in layers.items():
        code_key = layer_val.get("code") if isinstance(layer_val, dict) else None
        new_key = str(code_key) if code_key else str(layer_name)
        if new_key in mapped_layers:
            msg = f"Duplicate layer code '{new_key}' for year {year}; overwriting previous entry"
            try:
                logger.warning(msg)
            except Exception:
                print(msg)
        mapped_layers[new_key] = layer_val
    cb_acs[str(year)] = mapped_layers


cb_census = dict()
for key, val in cb["series"]["Census"].items():
    layers = cb["series"]["Census"][key]["layers"]
    mapped_layers = {}
    for layer_name, layer_val in layers.items():
        code_key = layer_val.get("code") if isinstance(layer_val, dict) else None
        new_key = str(code_key) if code_key else str(layer_name)
        if new_key in mapped_layers:
            msg = f"Duplicate layer code '{new_key}' for Census year {key}; overwriting previous entry"
            try:
                logger.warning(msg)
            except Exception:
                print(msg)
        mapped_layers[new_key] = layer_val
    cb_census[str(key)] = mapped_layers


for year in cb["series"]["Census"].keys():
    print(f"\nYear: {year}")
    for layer, values in cb["series"]["Census"][year]["layers"].items():
        print(f"{values['code']}: {layer}")



print(list(cb_census.keys()))
print(list(cb_acs.keys()))

list(cb_census["2020"].keys())
list(cb_acs["2020"].keys())

print(json.dumps(cb_acs["2020"], indent = 2))

len(list(cb_acs["2025"]))