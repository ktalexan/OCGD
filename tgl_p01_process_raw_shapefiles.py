# -*- coding: utf-8 -*-
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Project: Orange County Tiger/Lines Processing (OCTL)
# Title: Part 1: Process Raw Shapefiles ----
# Author: Dr. Kostas Alexandridis, GISP
# Version: 2026.1, Date: January 2026
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

print("\nOrange County Tiger/Lines Processing (OCTL): Part 1: Process Raw Shapefiles\n")


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# 1. Preliminaries ----
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
print("\n1. Preliminaries\n")

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
## 1.1. Referencing Libraries and Initialization ----
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
print("\n1.1. Referencing Libraries and Initialization\n")

# Import necessary libraries
import os
import sys
import datetime
from pathlib import Path
import shutil
import pandas as pd
import arcpy
from arcpy import metadata as md
from arcgis.features import GeoAccessor, GeoSeriesAccessor
from ocgd import OCtgl


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
## 1.2. Basic Definitions ----
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
print("\n1.2. Basic Definitions\n")

# Set pandas options
pd.options.mode.copy_on_write = True

# Set environment workspace to the current working directory
arcpy.env.workspace = os.getcwd()
arcpy.env.overwriteOutput = True

# Initialize the OCTL class object
tgl = OCtgl(part = 1, version = 2026.1)

# Get the project metadata and directories from the OCTL class object
prj_meta = tgl.prj_meta
prj_dirs = tgl.prj_dirs
# Get the raw metadata
# folder_metadata = tgl.get_raw_data(remote = True, export = True)

# Get the codebook from the OCTL class object
# cb, cbdf = tgl.load_cb(folder_metadata["year"],  cbdf = True)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# 2. Process Shapefiles to Geodatabase ----
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
print("\n2. Process Shapefiles to Geodatabase\n")

# Process the shapefiles and get the dictionary of feature classes and codes
process_dict = tgl.process_raw_data(year = 2010, remote = True, export = True)
process_dict = tgl.process_raw_data(year = 2011, remote = True, export = True)
process_dict = tgl.process_raw_data(year = 2012, remote = True, export = True)
process_dict = tgl.process_raw_data(year = 2013, remote = True, export = True)
process_dict = tgl.process_raw_data(year = 2014, remote = True, export = True)
process_dict = tgl.process_raw_data(year = 2015, remote = True, export = True)
process_dict = tgl.process_raw_data(year = 2016, remote = True, export = True)
process_dict = tgl.process_raw_data(year = 2017, remote = True, export = True)
process_dict = tgl.process_raw_data(year = 2018, remote = True, export = True)
process_dict = tgl.process_raw_data(year = 2019, remote = True, export = True)
process_dict = tgl.process_raw_data(year = 2020, remote = True, export = True)
process_dict = tgl.process_raw_data(year = 2021, remote = True, export = True)
process_dict = tgl.process_raw_data(year = 2022, remote = True, export = True)
process_dict = tgl.process_raw_data(year = 2023, remote = True, export = True)
process_dict = tgl.process_raw_data(year = 2024, remote = True, export = True)
process_dict = tgl.process_raw_data(year = 2025, remote = True, export = True)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# 3. Update Master Codebook ----
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
print("\n3. Update Master Codebook\n")

# Create or load the master codebook
cb_master = tgl.master_codebook(create = True)


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# End of Script ----
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
