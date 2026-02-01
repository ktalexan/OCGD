# -*- coding: utf-8 -*-
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Project: Orange County Community Resilience Estimates Processing (OCCRE)
# Title: Part 1: Create CRE Feature Classes ----
# Author: Dr. Kostas Alexandridis, GISP
# Version: 2026.1, Date: January 2026
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

print("\nOrange County Community Resilience Estimates Processing (OCCRE): Part 1: Create CRE Feature Classes\n")


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# 1. Preliminaries ----
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
print("\n1. Preliminaries\n")

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
## 1.1. Referencing Libraries and Initialization ----
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
print("\n1.1. Referencing Libraries and Initialization\n")

# Import necessary libraries
#from __future__ import annotations # pylint: disable=misplaced-future
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


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
## 1.2. Basic Definitions ----
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
print("\n1.2. Basic Definitions\n")

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

# Load the CRE codebook
cb_cre = cre.cb

# Run and log the CRE CB Variables fetch
cre_years = cre.cre_years

# Run and log the ACS CB Variables fetch
logger = cre.logger


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# 2. Process CRE Feature Classes ----
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
print("\n2. Process CRE Feature Classes\n")

# Create CRE feature classes for each year (with logging)
logger.enable(meta = prj_meta, filename = f"cre_feature_classes_{cre.version}.log", replace = True)
print("CRE Feature Classes Log\n")
for year in cre_years:
    print(f"\nCRE feature class for year {year}\n")
    cre.create_cre_feature_class(year)
print("\nCRE feature classes creation completed.")
logger.disable()


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# End of Script ----
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
print("\nLast Execution:", datetime.datetime.now().strftime("%Y-%m-%d"))
print("End of Script")
