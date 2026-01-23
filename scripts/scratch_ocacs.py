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
