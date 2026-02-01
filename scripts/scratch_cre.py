# Import necessary libraries
from __future__ import annotations
import os
import sys
import datetime
import json
from pathlib import Path
import logging
import unicodedata
from typing import Optional, Dict, Any
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
from ocgd import DualOutput, OCcre

# Load environment variables from .env file
load_dotenv()

# Set pandas options
pd.options.mode.copy_on_write = True

# Set environment workspace to the current working directory
arcpy.env.workspace = os.getcwd()
arcpy.env.overwriteOutput = True

# Initialize OCcre instance
cre = OCcre(part= 1, version= 2026.1)

# Get the project metadata and directories from the OCcre class object
prj_meta = cre.prj_meta
prj_dirs = cre.prj_dirs

# Run and log the CRE CB Variables fetch
cre_years = cre.cre_years

YEAR = 2019
cre_cb = cre.generate_cre_codebook(year= YEAR)
cre_db = cre.fetch_cre_tables(year= YEAR)

print(json.dumps(cre_cb, indent= 4))
print(cre_db.head(5))