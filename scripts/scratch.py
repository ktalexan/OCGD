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
from ocgd import OCGD, OCACS, OCTL
# Load environment variables from .env file
load_dotenv()

# Set pandas options
pd.options.mode.copy_on_write = True

# Set environment workspace to the current working directory
arcpy.env.workspace = os.getcwd()
arcpy.env.overwriteOutput = True

#gd = GDInit(part= 1, version= 2026.1)

# Initialize OCGD, OCACS, and OCTL instances
ocgd = OCGD(part= 1, version= 2026.1)
ocacs = OCACS(part= 1, version= 2026.1)
octl = OCTL(part= 1, version= 2026.1)

# Get the project metadata and directories from the OCGD, OCACS, and OCTL class objects
prj_meta = {
    "ocgd": ocgd.prj_meta,
    "ocacs": ocacs.prj_meta,
    "octl": octl.prj_meta
}
# The project directories are the same for all classes since they inherit from GDInit, so we can just get it from one of them.
prj_dirs = ocgd.prj_dirs
