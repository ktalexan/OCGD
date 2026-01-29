# Import necessary libraries
from __future__ import annotations
import os
import sys
import datetime as dt
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
from ocgd import OCacs

# Load environment variables from .env file
load_dotenv()

# Set pandas options
pd.options.mode.copy_on_write = True

# Set environment workspace to the current working directory
arcpy.env.workspace = os.getcwd()
arcpy.env.overwriteOutput = True

# Initialize OCACS instance
acs = OCacs(part= 1, version= 2026.1)

# Get the project metadata and directories from the OCACS class object
prj_meta = acs.prj_meta
prj_dirs = acs.prj_dirs

# Create and setup the master variable codebook
#cb_census_var = acs.cb_census_var(estimates_only = True)

# Process ACS data for all years
#acs.process_acs_data(process_year = 2010, all_years = False)            



# Fetch ACS variables metadata for the target year and show a preview
df_vars_master = acs.acs_cb_variables(year= None)
print(df_vars_master.head())
df_vars_master.columns
df_vars_master

# print the values of the third row of the df_vars_2010 dataframe
print(df_vars_master.iloc[4])


# sample_vars = acs.get_acs_list(year, "Demographic")
# df_co_d = acs.fetch_acs_tables(year = year, variables = sample_vars, geography = "CO")

# df_cs_d = acs.fetch_acs_tables(year = year, variables = sample_vars, geography = "CS")
# print(df_cs_d)

# df_pl_d = acs.fetch_acs_tables(year = year, variables = sample_vars, geography = "PL")
# print(df_pl_d)

# # Not working
# df_zc_d = acs.fetch_acs_tables(year = year, variables = sample_vars, geography = "ZC")
# print(df_zc_d)

# df_cd_d = acs.fetch_acs_tables(year = year, variables = sample_vars, geography = "CD")
# print(df_cd_d)

# df_ll_d = acs.fetch_acs_tables(year = year, variables = sample_vars, geography = "LL")
# print(df_ll_d)

# df_lu_d = acs.fetch_acs_tables(year = year, variables = sample_vars, geography = "LU")
# print(df_lu_d)

# df_se_d = acs.fetch_acs_tables(year = year, variables = sample_vars, geography = "SE")
# print(df_se_d)

# df_ss_d = acs.fetch_acs_tables(year = year, variables = sample_vars, geography = "SS")
# print(df_ss_d)

# df_su_d = acs.fetch_acs_tables(year = year, variables = sample_vars, geography = "SU")
# print(df_su_d)

# df_ua_d = acs.fetch_acs_tables(year = year, variables = sample_vars, geography = "UA")
# print(df_ua_d)

# df_pu_d = acs.fetch_acs_tables(year = year, variables = sample_vars, geography = "PU")
# print(df_pu_d)

# df_bg_d = acs.fetch_acs_tables(year = year, variables = sample_vars, geography = "BG")
# print(df_bg_d)

# df_tr_d = acs.fetch_acs_tables(year = year, variables = sample_vars, geography = "TR")
# print(df_tr_d)
