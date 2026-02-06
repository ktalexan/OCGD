# -*- coding: utf-8 -*-
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Project: Orange County Tiger/Lines Processing (OCTL)
# Title: Part 1: Raw Data Processing ----
# Author: Dr. Kostas Alexandridis, GISP
# Version: 2026.1, Date: January 2026
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

print("\nOrange County Tiger/Lines Processing (OCTL): Part 1: Raw Data Processing\n")

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# 1.1 Preliminaries ----
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
print("\n1.1 Preliminaries\n")


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
## Referencing Libraries and Initialization ----
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
print("\nReferencing Libraries and Initialization\n")

# Import necessary libraries
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


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
## Basic Definitions ----
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
print("\nBasic Definitions\n")

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


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# 1.2. Process TIGERweb REST API and Create Geodatabases ----
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
print("\n1.2. Process TIGERweb REST API and Create Geodatabases\n")


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
## Crawl TIGERweb REST API to Create Full Inventory ----
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
print("\nCrawl TIGERweb REST API to Create Full Inventory\n")


### Create  TIGERweb REST API Inventory Codebook ----
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# # Crawl the TIGERweb REST API to create a full inventory and export it to a JSON file
# logger.enable(meta = prj_meta, filename = f"octl_cb_twr_crawl_{octl.version}.log", replace = True)
# print("\nCrawling TIGERweb REST API to create full inventory...\n")
# # Run the crawl_tigerweb method to get the full inventory
# full_inventory = octl.crawl_tigerweb(export = True)
# logger.disable()

# Import the full inventory JSON file (if not already in memory)
with open(os.path.join(prj_dirs["codebook"], "octl_cb_twr.json"), "r", encoding = "utf-8") as f:
    cb = json.load(f)

# Extract the years available for the American Community Survey (ACS) from the codebook
acs_years = list(cb["series"]["ACS"].keys())
census_years = list(cb["series"]["Census"].keys())
econ_years = list(cb["series"]["ECON"].keys())

# Find the min and max years for the acs_years list
range_acs_years = range(int(min(acs_years)), int(max(acs_years)) + 1)


### Create ACS geodatabases from TWR REST APIs ----
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Create geodatabases from TWR REST APIs for American Community Survey (OCACS)
logger.enable(meta = prj_meta, filename = f"octl_ocacs_gdb_{octl.version}.log", replace = True)
for year in range_acs_years:
    print(f"\nCreating OCTL geodatabase for OCACS year: {year}\n")
    gdb_path = os.path.join(prj_dirs["gis"], f"octl_ocacs{year}.gdb")
    # If the geodatabase already exists, delete it
    if arcpy.Exists(gdb_path):
        arcpy.Delete_management(gdb_path)
    # Check if the year is available in the ACS series, if not, use the closest available year
    if str(year) not in acs_years:
        # find the closest year in acs_years to the current year
        year_to_use = int(min(acs_years, key = lambda x: abs(int(x) - year)))
        print(f"Year {year} is not available in the ACS series. Using closest available year: {year_to_use}")
    else:
        year_to_use = year
    # Create a new geodatabase from TWR REST API
    octl.create_gdb_from_twr(year = year_to_use, level = "ACS", out_gdb = gdb_path)
    print(f"OCTL OCACS geodatabase created at: {gdb_path}\n")
logger.disable()


### Create geodatabases from TWR REST APIs for Decennial Census (OCDC) ----
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Create geodatabases from TWR REST APIs for Decennial Census (OCDC)
logger.enable(meta = prj_meta, filename = f"octl_ocdc_gdb_{octl.version}.log", replace = True)
for year in census_years:
    print(f"\nCreating OCTL geodatabase for OCDC year: {year}\n")
    gdb_path = os.path.join(prj_dirs["gis"], f"octl_ocdc{year}.gdb")
    # If the geodatabase already exists, delete it
    if arcpy.Exists(gdb_path):
        arcpy.Delete_management(gdb_path)
    # Create a new geodatabase from TWR REST API
    octl.create_gdb_from_twr(year = int(year), level = "Census", out_gdb = gdb_path)
    print(f"OCTL OCDC geodatabase created at: {gdb_path}\n")
logger.disable()


### Create geodatabases from TWR REST APIs for Economic Census (OCEC) ----
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Create geodatabases from TWR REST APIs for Economic Census (OCEC)
logger.enable(meta = prj_meta, filename = f"octl_ocec_gdb_{octl.version}.log", replace = True)
for year in econ_years:
    print(f"\nCreating OCTL geodatabase for Economic Census year: {year}\n")
    gdb_path = os.path.join(prj_dirs["gis"], f"octl_ocec{year}.gdb")
    # If the geodatabase already exists, delete it
    if arcpy.Exists(gdb_path):
        arcpy.Delete_management(gdb_path)
    # Create a new geodatabase from TWR REST API
    octl.create_gdb_from_twr(year = int(year), level = "ECON", out_gdb = gdb_path)
    print(f"OCTL OCEC geodatabase created at: {gdb_path}\n")
logger.disable()


### Create geodatabases from TWR REST APIs for Physical Features (OCPF) ----
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Create geodatabases from TWR REST APIs for Physical Features (OCPF)
logger.enable(meta = prj_meta, filename = f"octl_ocpf_gdb_{octl.version}.log", replace = True)
print("\nCreating OCTL geodatabase for Physical Features\n")
gdb_path = os.path.join(prj_dirs["gis"], "octl_ocpf.gdb")
# If the geodatabase already exists, delete it
if arcpy.Exists(gdb_path):
    arcpy.Delete_management(gdb_path)
# Create a new geodatabase from TWR REST API
octl.create_gdb_from_twr(year = 2025, level = "PhysicalFeatures", out_gdb = gdb_path)
print(f"OCTL OCPF geodatabase created at: {gdb_path}\n")
logger.disable()


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# End of Script ----
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
print("\nLast Execution:", datetime.datetime.now().strftime("%m/%d/%Y"))
print("End of Script")
