# Import necessary libraries
import os
import sys
import datetime as dt
import json
from pathlib import Path
import shutil
import importlib
import wmi
import pandas as pd
import arcpy
from arcpy import metadata as md
from arcgis.features import GeoAccessor, GeoSeriesAccessor
from dotenv import load_dotenv
from ocgd import OCtgl

# Load environment variables from .env file
load_dotenv()

# Set pandas options
pd.options.mode.copy_on_write = True

# Set environment workspace to the current working directory
arcpy.env.workspace = os.getcwd()
arcpy.env.overwriteOutput = True

# Initialize OCTL instance
tgl = OCtgl(part= 1, version= 2026.1)

# Get the project metadata and directories from the OCTL class object
prj_meta = tgl.prj_meta
prj_dirs = tgl.prj_dirs
# Get the master codebook (load from JSON file)
cb = tgl.master_codebook(create = False)

# Get the feature list from the OCTL class object
fl = tgl.get_feature_list()

check_fields = ["TLID", "LINEARID", "TFID", "AREAID", "HYDROID"]

check_list = dict()

for f in check_fields:
    print(f"Checking field: {f}")
    check_list[f] = {}
    for year, value in fl.items():
        print(f"  Year: {year}")
        for key, fc in value["features"].items():
            fc_type = fc["type"]
            fc_alias = fc["alias"]
            for field, value in fc["fields"].items():
                if field == f and fc_type == "Feature Class":
                    print(f"      Field: {key}")
                    check_list[f][key] = fc_alias


# Print the check list with proper indentation
print(json.dumps(check_list, indent=4))
