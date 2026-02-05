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

# scratch_path = octl.scratch_gdb()

# url = "https://api.census.gov/data.json"
# response = requests.get(url, timeout = 20)
# datasets = response.json()['dataset']
# dataset_names = [dataset['c_dataset'] for dataset in datasets]

# Get TIGERweb dictionary from the OCTL class object (do not export if it is current and recently updated)
# twr_cb = octl.get_tigerweb_dictionary(export = True)
twr_cb = octl.get_tigerweb_dictionary(export = False)

# Set up logging for the script
logger = octl.logger

# Create geodatabases from TWR REST APIs for American Community Survey (OCACS)
logger.enable(meta = prj_meta, filename = f"twr_ocacs_gdb_{octl.version}.log", replace = True)
for year in list(twr_cb["acs"].keys()):
    print(f"\nCreating TWR geodatabase for OCACS year: {year}\n")
    gdb_path = os.path.join(prj_dirs["gis"], f"twr_ocacs{year}.gdb")
    # If the geodatabase already exists, delete it
    if arcpy.Exists(gdb_path):
        arcpy.Delete_management(gdb_path)
    # Create a new geodatabase from TWR REST API
    octl.create_gdb_from_twr(year = int(year), level = "acs", out_gdb = gdb_path)
    print(f"TWR OCACS geodatabase created at: {gdb_path}\n")
logger.disable()

# Create geodatabases from TWR REST APIs for Decennial Census (OCDC)
logger.enable(meta = prj_meta, filename = f"twr_ocdc_gdb_{octl.version}.log", replace = True)
for year in list(twr_cb["census"].keys()):
    print(f"\nCreating TWR geodatabase for OCDC year: {year}\n")
    gdb_path = os.path.join(prj_dirs["gis"], f"twr_ocdc{year}.gdb")
    # If the geodatabase already exists, delete it
    if arcpy.Exists(gdb_path):
        arcpy.Delete_management(gdb_path)
    # Create a new geodatabase from TWR REST API
    octl.create_gdb_from_twr(year = int(year), level = "census", out_gdb = gdb_path)
    print(f"TWR OCDC geodatabase created at: {gdb_path}\n")
logger.disable()


# Create geodatabases from TWR REST APIs for Economic Census (OCEC)
logger.enable(meta = prj_meta, filename = f"twr_ocec_gdb_{octl.version}.log", replace = True)
for year in list(twr_cb["econ"].keys()):
    print(f"\nCreating TWR geodatabase for Economic Census year: {year}\n")
    gdb_path = os.path.join(prj_dirs["gis"], f"twr_ocec{year}.gdb")
    # If the geodatabase already exists, delete it
    if arcpy.Exists(gdb_path):
        arcpy.Delete_management(gdb_path)
    # Create a new geodatabase from TWR REST API
    octl.create_gdb_from_twr(year = int(year), level = "econ", out_gdb = gdb_path)
    print(f"TWR OCEC geodatabase created at: {gdb_path}\n")
logger.disable()

#out_gdb = octl.create_gdb_from_twr(year=2025, level="acs")






layer_dict = {}
for level, content in twr_cb.items():
    if level != "main":
        for year, year_content in content.items():
            layers = year_content["layers"]
            for layer_name, layer_info in layers.items():
                layer_code = layer_info["code"]
                if layer_name not in layer_dict:
                    layer_dict[layer_name] = layer_code

print(json.dumps(layer_dict, indent=4))


rest = twr_cb["acs"]["2025"]["layers"]["2020 Census Public Use Microdata Areas"]["rest"]

arcpy.ListFields(rest)
fields = [f.name for f in arcpy.ListFields(rest)]
fields

if "STATE" in [f.name for f in arcpy.ListFields(rest)]:
    print("STATE field exists")

if 'STATE' in fields:
    arcpy.MakeFeatureLayer_management(rest, 'temp_lyr')
else:
    raise RuntimeError(f"REST layer has no 'STATE' field: {rest}")
