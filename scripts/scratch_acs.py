# Import necessary libraries
from __future__ import annotations
import os
import sys
import datetime as dt
import json
from pathlib import Path
import shutil
import importlib
import wmi
import pandas as pd
import requests
import logging
import unicodedata
from typing import Optional, Dict, Any
import re
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
cb_census_var = acs.cb_census_var(estimates_only = True)

# Process ACS data for all years
acs.process_acs_data(process_year = 2010, all_years = False)            


def fetch_acs_variables(
	year: int, 
	session: Optional[requests.Session] = None
	) -> pd.DataFrame:
	"""
	Fetch ACS variables metadata for a given year from the Census API.
	Args:
		year: Four-digit year (e.g. 2019).
		session: Optional `requests.Session` for connection reuse.
	Returns:
		pandas.DataFrame: index is variable name, columns are variable properties.
	"""
	api_url = f"https://api.census.gov/data/{year}/acs/acs5/variables.json"
	s = session or requests
	resp = s.get(api_url)
	resp.raise_for_status()
	data = resp.json()
	variables = data.get("variables", {})
	# Keep only variables that start with a letter, followed by a digit,
	# and end with a capital 'E' (e.g. 'B01001_001E').
	pattern = re.compile(r'^[A-Za-z]\d.*E$')
	filtered_vars = {k: v for k, v in variables.items() if pattern.match(k)}
	df = pd.DataFrame.from_dict(filtered_vars, orient="index")
	# Move the index (variable names) into a regular column named 'variable'
	# so the variable names appear as the first column in the returned DataFrame.
	df = df.reset_index().rename(columns={"index": "variable"})
	# Clean the 'label' column per user rules
	if "label" in df.columns:
		def _clean_label(val: object) -> str:
			text = str(val)
			# Replace '!!' with ':'
			text = text.replace("!!", ":")
			# Remove leading 'Estimate' token
			text = re.sub(r'^Estimate\s*', '', text)
			# Normalize and remove diacritic marks (accents)
			text = unicodedata.normalize('NFKD', text)
			text = ''.join(ch for ch in text if not unicodedata.combining(ch))
			# Remove semicolons explicitly
			text = text.replace(';', '')
			# Remove punctuation except commas and colons (keep letters, numbers, whitespace, commas, colons)
			text = re.sub(r"[^A-Za-z0-9\s,:]", '', text)
			# Collapse multiple spaces
			text = re.sub(r'\s+', ' ', text)
			# Trim leading/trailing spaces and punctuation (commas, colons, semicolons, dots)
			text = text.strip(" \t\n\r\.,;:")
			return text
		df["label"] = df["label"].apply(_clean_label)
	# If a 'group' column exists, sort by group then variable, then reset index
	if "group" in df.columns:
		df = df.sort_values(by=["group", "variable"]).reset_index(drop=True)
	return df





year = 2023

# Fetch ACS variables metadata for the target year and show a preview
df_vars = fetch_acs_variables(year)
print(df_vars.head())
df_vars.columns
df_vars

# print the values of the third row of the df_vars_2010 dataframe
print(df_vars.iloc[4])

sample_vars = acs.get_acs_list(year, "Demographic")
df_co_d = acs.fetch_acs_tables(year = year, variables = sample_vars, geography = "CO")

df_cs_d = acs.fetch_acs_tables(year = year, variables = sample_vars, geography = "CS")
print(df_cs_d)

df_pl_d = acs.fetch_acs_tables(year = year, variables = sample_vars, geography = "PL")
print(df_pl_d)

# Not working
df_zc_d = acs.fetch_acs_tables(year = year, variables = sample_vars, geography = "ZC")
print(df_zc_d)

df_cd_d = acs.fetch_acs_tables(year = year, variables = sample_vars, geography = "CD")
print(df_cd_d)

df_ll_d = acs.fetch_acs_tables(year = year, variables = sample_vars, geography = "LL")
print(df_ll_d)

df_lu_d = acs.fetch_acs_tables(year = year, variables = sample_vars, geography = "LU")
print(df_lu_d)

df_se_d = acs.fetch_acs_tables(year = year, variables = sample_vars, geography = "SE")
print(df_se_d)

df_ss_d = acs.fetch_acs_tables(year = year, variables = sample_vars, geography = "SS")
print(df_ss_d)

df_su_d = acs.fetch_acs_tables(year = year, variables = sample_vars, geography = "SU")
print(df_su_d)

df_ua_d = acs.fetch_acs_tables(year = year, variables = sample_vars, geography = "UA")
print(df_ua_d)

df_pu_d = acs.fetch_acs_tables(year = year, variables = sample_vars, geography = "PU")
print(df_pu_d)

df_bg_d = acs.fetch_acs_tables(year = year, variables = sample_vars, geography = "BG")
print(df_bg_d)

df_tr_d = acs.fetch_acs_tables(year = year, variables = sample_vars, geography = "TR")
print(df_tr_d)


