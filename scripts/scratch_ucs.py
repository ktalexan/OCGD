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
from ocgd import OCucs

# Load environment variables from .env file
load_dotenv()

# Set pandas options
pd.options.mode.copy_on_write = True

# Set environment workspace to the current working directory
arcpy.env.workspace = os.getcwd()
arcpy.env.overwriteOutput = True

# Initialize OCGD instance
ucs = OCucs(part= 1, version= 2026.1)

# Get the project metadata and directories from the OCGD class object
prj_meta = ucs.prj_meta
prj_dirs = ucs.prj_dirs
