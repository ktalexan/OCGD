# Import necessary libraries
from __future__ import annotations
import os
import sys
import datetime
import json
from pathlib import Path
import logging
import unicodedata
from typing import Union, Optional, Dict, Any
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
from ocgd import OCACS

# Load environment variables from .env file
load_dotenv()

# Set pandas options
pd.options.mode.copy_on_write = True

# Set environment workspace to the current working directory
arcpy.env.workspace = os.getcwd()
arcpy.env.overwriteOutput = True

# Initialize OCACS instance
ocacs = OCACS(part= 1, version= 2026.1)

# Get the project metadata and directories from the OCACS class object
prj_meta = ocacs.prj_meta
prj_dirs = ocacs.prj_dirs


# Get the logger from the OCACS class object
logger = ocacs.logger

logger.enable(meta = prj_meta, filename = f"ocacs_cb_vars_{str(ocacs.version).replace(".", "0")}.log", replace = True)
print("OCACS CB Variables Log\n")
df_cb_vars = ocacs.acs_cb_variables(write_to_disk = True)
print("\nACS CB Variables fetch and write to disk completed. Check the log file for details.")
logger.disable()











# Import excel file to dataframe
df_cb_vars = pd.read_excel(os.path.join(prj_dirs["codebook"], f"ocacs_cb_vars_master_{str(ocacs.version).replace(".", "0")}.xlsx"))


years = ocacs.acs5_years

master_schema = {
    "year": "object",
    "count_years": "int32",
    "all_years": "bool",
    "table": "object",
    "group": "object",
    "variable": "object",
    "alias": "object",
    "oid": "int32",
    "used": "bool",
    "level": "object",
    "level_group": "object",
    "category": "object",
    "label": "object",
    "concept": "object",
    "type": "object",
    "limit": "int32",
    "attributes": "object",
    "note": "object",
    "markdown": "object"
}

# For each year, add a column to the schema with bool type
for acs_year in years:
    master_schema[str(acs_year)] = "bool"

# Create an empty DataFrame with the defined schema called master_df
master_df = pd.DataFrame(columns=master_schema.keys()).astype(master_schema)

# For each year of the df_cb_vars "year" column, get the variables in the "variables" column
for year in df_cb_vars["year"].unique():
    # For each unique variable in the "variable" column for the current year, create a new row in the master_df dataframe with the year and variable
    for variable in df_cb_vars[df_cb_vars["year"] == year]["variable"].unique():
        if variable not in master_df["variable"].values:
            new_row = {
                "year": f"{master_df["year"]}, {year}",
                "variable": variable,
            }
            master_df = master_df._append(new_row, ignore_index=True)

cb_vars = {}
for level in ["Demographics", "Social", "Economic", "Housing"]:
    cb_vars[level] = {}
    if level == "Demographics":
        no_sections = 7
        for i in range(1, no_sections + 1):
            section_code = f"D{str(i).zfill(2)}"
            cb_vars[level][section_code] = {}
    elif level == "Social":
        no_sections = 23
        for i in range(1, no_sections + 1):
            section_code = f"S{str(i).zfill(2)}"
            cb_vars[level][section_code] = {}
    elif level == "Economic":
        no_sections = 19
        for i in range(1, no_sections + 1):
            section_code = f"E{str(i).zfill(2)}"
            cb_vars[level][section_code] = {}
    elif level == "Housing":
        no_sections = 23
        for i in range(1, no_sections + 1):
            section_code = f"H{str(i).zfill(2)}"
            cb_vars[level][section_code] = {}

for year in ocacs.years:
    cb_vars["Demographics"]["D01"][year] = ["B01003_001E"]
    cb_vars["Demographics"]["D02"][year] = ["B01001_001E", "B01001_002E", "B01001_026E", "B01001_003E", "B01001_004E", "B01001_005E", "B01001_006E", "B01001_007E", "B01001_008E", "B01001_009E", "B01001_010E", "B01001_011E", "B01001_012E", "B01001_013E", "B01001_014E", "B01001_015E", "B01001_016E", "B01001_017E", "B01001_018E", "B01001_019E", "B01001_020E", "B01001_021E", "B01001_022E", "B01001_023E", "B01001_024E", "B01001_025E", "B01001_027E", "B01001_028E", "B01001_029E", "B01001_030E", "B01001_031E", "B01001_032E", "B01001_033E", "B01001_034E", "B01001_035E", "B01001_036E", "B01001_037E", "B01001_038E", "B01001_039E", "B01001_040E", "B01001_041E", "B01001_042E", "B01001_043E", "B01001_044E", "B01001_045E", "B01001_046E", "B01001_047E", "B01001_048E", "B01001_049E"]





# Run and log the ACS CB Variables fetch
logger.enable(meta = prj_meta, filename = f"cb_variables_{ocacs.version}.log", replace = True)
print("ACS CB Variable Log\n")
df_vars_master = ocacs.acs_cb_variables(year= None)
print("\nExample preview of ACS CB Variables DataFrame:")
print(df_vars_master.head())
print("\nExample row data of ACS CB Variables DataFrame:")
print(df_vars_master.iloc[1])
logger.disable()


# sample_vars = ocacs.get_acs_list(year, "Demographic")
# df_co_d = ocacs.fetch_acs_tables(year = year, variables = sample_vars, geography = "CO")

# df_cs_d = ocacs.fetch_acs_tables(year = year, variables = sample_vars, geography = "CS")
# print(df_cs_d)

# df_pl_d = ocacs.fetch_acs_tables(year = year, variables = sample_vars, geography = "PL")
# print(df_pl_d)

# # Not working
# df_zc_d = ocacs.fetch_acs_tables(year = year, variables = sample_vars, geography = "ZC")
# print(df_zc_d)

# df_cd_d = ocacs.fetch_acs_tables(year = year, variables = sample_vars, geography = "CD")
# print(df_cd_d)

# df_ll_d = ocacs.fetch_acs_tables(year = year, variables = sample_vars, geography = "LL")
# print(df_ll_d)

# df_lu_d = ocacs.fetch_acs_tables(year = year, variables = sample_vars, geography = "LU")
# print(df_lu_d)

# df_se_d = ocacs.fetch_acs_tables(year = year, variables = sample_vars, geography = "SE")
# print(df_se_d)

# df_ss_d = ocacs.fetch_acs_tables(year = year, variables = sample_vars, geography = "SS")
# print(df_ss_d)

# df_su_d = ocacs.fetch_acs_tables(year = year, variables = sample_vars, geography = "SU")
# print(df_su_d)

# df_ua_d = ocacs.fetch_acs_tables(year = year, variables = sample_vars, geography = "UA")
# print(df_ua_d)

# df_pu_d = ocacs.fetch_acs_tables(year = year, variables = sample_vars, geography = "PU")
# print(df_pu_d)

# df_bg_d = ocacs.fetch_acs_tables(year = year, variables = sample_vars, geography = "BG")
# print(df_bg_d)

# df_tr_d = ocacs.fetch_acs_tables(year = year, variables = sample_vars, geography = "TR")
# print(df_tr_d)



cb_sections = {
    "Demographics": {
        "D01": "Total Population",
        "D02": "Sex and Age",
        "D03": "Median Age by Sex and Race",
        "D04": "Race",
        "D05": "Race Alone or in Combination with Other Races",
        "D06": "Hispanic or Latino Origin",
        "D07": "Citizen Voting Age Population"
    },
    "Social": {
        "S01": "Households by Type",
        "S02": "Families by Type",
        "S03": "Household Relationships",
        "S04": "Marital Status",
        "S05": "Fertility Characteristics",
        "S06": "Grandparent Relationships",
        "S07": "School Enrollment",
        "S08": "Educational Attainment",
        "S09": "Veteran Status",
        "S10": "Veteran Disability",
        "S11": "Disability Status and Type",
        "S12": "Disability Status and Health Insurance Coverage",
        "S13": "Food Stamp Households",
        "S14": "Residence 1 Year Ago",
        "S15": "Place of Birth",
        "S16": "Citizenship Status",
        "S17": "Citizenship Status by Year of Entry",
        "S18": "World Region of Birth of Foreign-Born Population",
        "S19": "Language Spoken in Households",
        "S20": "Language Spoken at Home",
        "S21": "Ancestry",
        "S22": "People Reporting Ancestry",
        "S23": "Computer and Internet Use"
    },
    "Economic": {
        "E01": "Employment Status",
        "E02": "Work Status by Age of Worker",
        "E03": "Commuting to Work",
        "E04": "Travel Time to Work",
        "E05": "Number of Vehicles Available for Workers",
        "E06": "Median Age by Means of Transportation to Work",
        "E07": "Means of Transportation to Work by Race",
        "E08": "Occupation",
        "E09": "Industry",
        "E10": "Class of Worker",
        "E11": "Household Income and Earnings in the Past 12 Months",
        "E12": "Income and Earnings in Dollars",
        "E13": "Family Income in Dollars",
        "E14": "Health Insurance Coverage",
        "E15": "Ratio of Income to Poverty Level",
        "E16": "Poverty in Population in the Past 12 Months",
        "E17": "Poverty in Households in the Past 12 Months",
        "E18": "Percentage of Families and People Whose Income in the Past 12 Months is Below the Poverty Level",
        "E19": "Poverty and Income Deficit in Dollars in the Past 12 Months for Families"
    },
    "Housing": {
        "H01": "Housing Occupancy",
        "H02": "Units in Structure",
        "H03": "Population in Occupied Housing Units by Tenure by Units in Structure",
        "H04": "Year Structure Built",
        "H05": "Rooms",
        "H06": "Bedrooms",
        "H07": "Housing Tenure by Race of Householder",
        "H08": "Total Population in Occupied Housing Units by Tenure",
        "H09": "Vacancy Status",
        "H10": "Occupied Housing Units by Race of Householder",
        "H11": "Year Householder Moved Into Unit",
        "H12": "Vehicles Available",
        "H13": "House Heating Fuel",
        "H14": "Selected Housing Characteristics",
        "H15": "Occupants per Room",
        "H16": "Housing Value",
        "H17": "Price Asked for Vacant For-Sale Only, and Sold, Not Occupied Housing Units",
        "H18": "Mortgage Status",
        "H19": "Selected Monthly Owner Costs",
        "H20": "Selected Monthly Owner Costs as a Percentage of Household Income",
        "H21": "Contract Rent Distribution and Rent Asked Distribution in Dollars",
        "H22": "Gross Rent",
        "H23": "Gross Rent as a Percentage of Household Income"
    }
}
