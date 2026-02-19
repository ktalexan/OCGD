# Import necessary libraries
import os
import sys
import datetime
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

# Get the logger from the OCTL class
logger = octl.logger


# Import the full inventory JSON file (if not already in memory)
with open(os.path.join(prj_dirs["codebook"], "octl_cb_twr.json"), "r", encoding = "utf-8") as f:
    cb = json.load(f)

# # Import the master codebook JSON file (if not already in memory)
# with open(os.path.join(prj_dirs["codebook"], "octl_cb_master.json"), "r", encoding = "utf-8") as f:
#     master_cb = json.load(f)


# Extract the years available for the American Community Survey (ACS) from the codebook
acs_years = list(cb["series"]["ACS"].keys())
# census_years = list(cb["series"]["Census"].keys())
# econ_years = list(cb["series"]["ECON"].keys())

# Find the min and max years for the acs_years list
range_acs_years = range(int(min(acs_years)), int(max(acs_years)) + 1)


master_fc = []
for year in acs_years:
    gdb_path = os.path.join(prj_dirs["gis"], f"octl_ocacs{year}.gdb")
    arcpy.env.workspace = gdb_path
    for fc in arcpy.ListFeatureClasses():
        if fc[:2] not in master_fc:
            master_fc.append(fc[:2])


