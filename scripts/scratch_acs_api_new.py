#from __future__ import annotations
import os
import json
from typing import List, Dict, Optional, Union
#from fontTools.misc.plistlib import Data
#import requests
import pandas as pd
from dotenv import load_dotenv
load_dotenv()
from ocgd import OCacs

acs = OCacs(part=1, version=2026.1)

# Get the project metadata and directories from the OCACS class object
prj_meta = acs.prj_meta
prj_dirs = acs.prj_dirs



def get_master_dataframe():
	"""
	Fetch sample ACS data across all years, variable categories, and geographies.
	Args:
		None
	Raises:
		None
	Returns:
		master_df (pd.DataFrame): Master DataFrame containing ACS data.
	Example:
		>>> master_df = get_master_dataframe()
	Note: 
		This function may take a while to run as it fetches data for multiple years, categories, and geographies.
	"""

	# List of ACS geographies to fetch
	acs_geographices = [
		"CO",  # County
		"CS",  # County Subdivision
		"PL",  # Cities or Places
		"ZC",  # Zip Code Tabulation Area
		"CD",  # Congressional District
		"LL",  # State Assembly Legislative Districts (Lower)
		"LU",  # State Senate Legislative Districts (Upper)
		"SE",  # Elementary School District
		"SS",  # Secondary School District
		"SU",  # Unified School District
		"UA",  # Urban Area
		"PU",  # Public Use Microdata Area
		"BG",  # Block Group
		"TR"   # Census Tract
	]

	# Use a nested dictionary to accumulate results (years -> category -> geography -> DataFrame)
	master_data: Dict[str, Dict[str, Dict[str, Optional[pd.DataFrame]]]] = {}

	# Loop through each ACS year, variable category, and geography to fetch data
	for year in acs.acs5_years:
		print(f"\nFetching sample ACS data for year {year}...")
		master_data[str(year)] = {}

		# Loop through variable categories
		for level in ["Demographic", "Social", "Economic", "Housing"]:
			print(f" Variable Category: {level}")
			master_data[str(year)][level] = {}

			# Get sample variables for the category
			sample_vars = acs.get_acs_list(year, level)

			# Loop through geographies
			for geography in acs_geographices:
				print(f"- Geography: {geography}")
				# Fetch the DataFrame for this combination
				df = acs.fetch_acs_tables(year=year, variables=sample_vars, geography=geography)
				master_data[str(year)][level][geography] = df

				if df is None:
					print("  Retrieved no records (None returned).")
				else:
					print(f"  Retrieved {df.shape[0]} records with {df.shape[1]} variables.")

	# Return the nested dict of results
	return master_data

# Get the master DataFrame by calling the function
master_df = get_master_dataframe()



