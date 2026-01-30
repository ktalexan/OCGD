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
from ocgd import DualOutput, OCacs

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

# Run and log the ACS CB Variables fetch
logger = acs.logger
logger.enable(meta = prj_meta, filename = f"cb_variables_{acs.version}.log")
print("ACS CB Variable Log\n")
df_vars_master = acs.acs_cb_variables(year= None)
print("\nExample preview of ACS CB Variables DataFrame:")
print(df_vars_master.head())
print("\nExample row data of ACS CB Variables DataFrame:")
print(df_vars_master.iloc[1])
logger.disable()


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
