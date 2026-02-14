# Import necessary libraries
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

for year in ocacs.acs5_years:
    logger.enable(meta = prj_meta, filename = f"ocacs_cb_vars_{year}.log", replace = True)
    print(f"OCACS {year} CB Variables Log\n")
    cb_vars, df_cb_vars = ocacs.acs_cb_variables(year = year, write_to_disk = True)
    print(f"\nOCACS {year} CB Variables fetch and write to disk completed. Check the log file for details.")
    logger.disable()




ocacs_cb_vars = ocacs.construct_master_variables_dict(write_to_file = True)





















    # Loop through the ACS years
    # for acs_year in years:

    # Order the master DataFrame by year and variable code
    master_df = master_df.sort_values(by=["year", "variable"]).reset_index(drop = True)

    # Update the year_count column to the cumulative DataFrame that counts the number of years each variable appears in
    cum_df["year_count"] = cum_df["years"].apply(lambda x: len(x.split(", ")))
    # Update the column all_years to the cumulative DataFrame that is True if the variable appears in all years and False otherwise
    cum_df["all_years"] = cum_df["year_count"] == len(years)

    # Add a table column to the cumulative DataFrame that extracts the table code from the 3 first characters of the variable code (e.g. 'B01' from 'B01001_001E')
    cum_df["table"] = cum_df["variable"].apply(lambda x: x[:3])
    # Add a group column to the cumulative DataFrame that extracts the group name from the variable code before the underscore (e.g. 'B01001' from 'B01001_001E')
    cum_df["group"] = cum_df["variable"].apply(lambda x: x.split("_")[0])

    # Add oid, used, level, section, section_name, markdown, and note as empty columns to the cumulative DataFrame
    cum_df["oid"] = 0
    cum_df["used"] = False
    cum_df["level"] = None
    cum_df["section"] = None
    cum_df["section_name"] = None
    cum_df["markdown"] = None
    cum_df["note"] = None

    # Reorder the columns in the cumulative DataFrame to match the order of the master DataFrame
    cum_df = cum_df[["years", "year_count", "all_years", "table", "group", "variable", "alias", "oid", "used", "level", "section", "section_name", "markdown", "note", "label", "concept", "type", "attributes"]]

    # For each year in years, add a column to the cumulative DataFrame with bool type that is True if the variable appears in that year and False otherwise
    for acs_year in years:
        cum_df[str(acs_year)] = cum_df["years"].apply(lambda x: str(acs_year) in x.split(", "))

    # Sort the cumulative DataFrame by variable and year_count in descending order
    cum_df = cum_df.sort_values(by=["variable", "year_count"], ascending=[True, False]).reset_index(drop=True)

    print(f"\nMaster DataFrame created with {len(master_df):,} rows and {len(master_df.columns):,} columns.")
    print(f"Cumulative DataFrame created with {len(cum_df):,} rows and {len(cum_df.columns):,} columns.")
    if write_to_disk:
        print("Writing master DataFrame to Excel file...")
        # After processing all years, write the master DataFrame to an Excel file
        master_output_path = os.path.join(self.prj_dirs["codebook"], f"ocacs_cb_vars_master_{str(self.version).replace('.', '0')}.xlsx")
        master_df.to_excel(master_output_path, index = False, sheet_name = "Master")

        print("Write the cumulative variable DataFrame to an Excel file...")
        cum_output_path = os.path.join(self.prj_dirs["codebook"], f"ocacs_cb_vars_cumulative_{str(self.version).replace('.', '0')}.xlsx")
        cum_df.to_excel(cum_output_path, index = False, sheet_name = "Cumulative")

    # Return the master DataFrame containing variable information for all specified years
    return master_df

















































years = ocacs.acs5_years
for year in years:
    print(f"{year}\n- Demographic: {len(ocacs_cb_vars[str(year)]['Demographic']['all_variables'])} variables\n- Social: {len(ocacs_cb_vars[str(year)]['Social']['all_variables'])} variables\n- Economic: {len(ocacs_cb_vars[str(year)]['Economic']['all_variables'])} variables\n- Housing: {len(ocacs_cb_vars[str(year)]['Housing']['all_variables'])} variables")



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
