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

# # Crawl the TIGERweb REST API to create a full inventory and export it to a JSON file
# logger.enable(meta = prj_meta, filename = f"octl_cb_twr_crawl_{octl.version}.log", replace = True)
# print("\nCrawling TIGERweb REST API to create full inventory...\n")
# # Run the crawl_tigerweb method to get the full inventory
# full_inventory = octl.crawl_tigerweb(export = True)
# logger.disable()

octl.create_gdb_from_twr(year = 2025, level = "PhysicalFeatures")

# Import the full inventory JSON file (if not already in memory)
with open(os.path.join(prj_dirs["codebook"], "octl_cb_twr.json"), "r", encoding = "utf-8") as f:
    cb = json.load(f)

# Extract the years available for the American Community Survey (ACS) from the codebook
acs_years = list(cb["series"]["ACS"].keys())
census_years = list(cb["series"]["Census"].keys())
econ_years = list(cb["series"]["ECON"].keys())

# Create geodatabases from TWR REST APIs for American Community Survey (OCACS)
logger.enable(meta = prj_meta, filename = f"twr_ocacs_gdb_{octl.version}.log", replace = True)
for year in acs_years:
    print(f"\nCreating TWR geodatabase for OCACS year: {year}\n")
    gdb_path = os.path.join(prj_dirs["gis"], f"twr_ocacs{year}.gdb")
    # If the geodatabase already exists, delete it
    if arcpy.Exists(gdb_path):
        arcpy.Delete_management(gdb_path)
    # Create a new geodatabase from TWR REST API
    octl.create_gdb_from_twr(year = int(year), level = "ACS", out_gdb = gdb_path)
    print(f"TWR OCACS geodatabase created at: {gdb_path}\n")
logger.disable()

# Create geodatabases from TWR REST APIs for Decennial Census (OCDC)
logger.enable(meta = prj_meta, filename = f"twr_ocdc_gdb_{octl.version}.log", replace = True)
for year in census_years:
    print(f"\nCreating TWR geodatabase for OCDC year: {year}\n")
    gdb_path = os.path.join(prj_dirs["gis"], f"twr_ocdc{year}.gdb")
    # If the geodatabase already exists, delete it
    if arcpy.Exists(gdb_path):
        arcpy.Delete_management(gdb_path)
    # Create a new geodatabase from TWR REST API
    octl.create_gdb_from_twr(year = int(year), level = "Census", out_gdb = gdb_path)
    print(f"TWR OCDC geodatabase created at: {gdb_path}\n")
logger.disable()

# Create geodatabases from TWR REST APIs for Economic Census (OCEC)
logger.enable(meta = prj_meta, filename = f"twr_ocec_gdb_{octl.version}.log", replace = True)
for year in econ_years:
    print(f"\nCreating TWR geodatabase for Economic Census year: {year}\n")
    gdb_path = os.path.join(prj_dirs["gis"], f"twr_ocec{year}.gdb")
    # If the geodatabase already exists, delete it
    if arcpy.Exists(gdb_path):
        arcpy.Delete_management(gdb_path)
    # Create a new geodatabase from TWR REST API
    octl.create_gdb_from_twr(year = int(year), level = "ECON", out_gdb = gdb_path)
    print(f"TWR OCEC geodatabase created at: {gdb_path}\n")
logger.disable()

# Create geodatabases from TWR REST APIs for Physical Features (OCPF)
logger.enable(meta = prj_meta, filename = f"twr_ocpf_gdb_{octl.version}.log", replace = True)
print("\nCreating TWR geodatabase for Physical Features\n")
gdb_path = os.path.join(prj_dirs["gis"], f"twr_ocpf.gdb")
# If the geodatabase already exists, delete it
if arcpy.Exists(gdb_path):
    arcpy.Delete_management(gdb_path)
# Create a new geodatabase from TWR REST API
octl.create_gdb_from_twr(year = 2025, level = "PhysicalFeatures", out_gdb = gdb_path)
print(f"TWR OCPF geodatabase created at: {gdb_path}\n")
logger.disable()
