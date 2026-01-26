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
from ocgd import OCtgl, OCacs, OCucs
# Add new imports

# Load environment variables from .env file
load_dotenv()


# Set pandas options
pd.options.mode.copy_on_write = True

# Set environment workspace to the project root (repo root)
arcpy.env.workspace = str(os.getcwd())
arcpy.env.overwriteOutput = True

#gd = GDInit(part= 1, version= 2026.1)

# Initialize OCucs, OCacs, and OCtgl instances
tgl = OCtgl(part= 1, version= 2026.1)
acs = OCacs(part= 1, version= 2026.1)
ucs = OCucs(part= 1, version= 2026.1)

# Get the project metadata and directories from the OCucs, OCacs, and OCtgl class objects
prj_meta = {
    "tgl": tgl.prj_meta,
    "acs": acs.prj_meta,
    "ucs": ucs.prj_meta
}
# The project directories are the same for all classes since they inherit from ocgdm, so we can just get it from one of them.
prj_dirs = tgl.prj_dirs

"https://api.census.gov/data/2023/acs/acs5/variables.json"

# New helper: fetch Census ACS variables JSON for a given year


master_var_cb_2023 = get_census_variables(year = 2023, estimates_only = True, write_json = True)

