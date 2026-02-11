# Import necessary libraries
from dask.array.ma import count
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




# Create a markdown document with the variable information for the current year
md_path = os.path.join(prj_dirs["documentation"], f"ocacs_cb_vars_{year}.md")
with open(md_path, "w", encoding = "utf-8") as f:
    f.write(f"# OCACS ACS CB Variables for {year}\n\n")
    f.write(f"Total variables: {len(df_cb):,}\n\n")
    for level in ["Demographic", "Social", "Economic", "Housing"]:
        f.write(f"## {level} Characteristics\n\n")
        level_df = df_cb[df_cb["level"] == level]
        for section in level_df["section"].dropna().unique():
            f.write(f"### {section}\n\n")
            section_df = level_df[level_df["section"] == section]
            for _, row in section_df.iterrows():
                f.write(f"- **{row['variable']}**: {row['alias']} ({row['label']})\n")
            f.write("\n")
    f.write("\n")
    f.write("---\n\n")



# Create a markdown document with the variable information for the current year
md_path = os.path.join(prj_dirs["documentation"], f"ocacs_cb_vars_{year}.md")
with open(md_path, "w", encoding = "utf-8") as f:
    f.write("<img align=\"left\" src=\"OCDC.jpg\" width=\"300\" hspace=25 vspace=15>\n\n")
    f.write(f"#  {year} Orange County ACS 5-Year Geodemographics Documentation\n\n")
    f.write(f"*Orange County American Community Survey (ACS) Geodemographic Repository <br> Dr. Kostas Alexandridis, GISP. OC Public Works, OC Survey/Geospatial Services*, version: {ocacs.version}, Date: {datetime.datetime.now().strftime('%B %Y')}")
    f.write("\n\n[<div align=\"right\"><< Back to ReadMe.md</div>](../README.md)\n\n<br/>")
    f.write("\n\n## Geoodemographic Tables by Group\n\nFor each of the geographies described in the previous section, four categories of geodemographic characteristics are available:\n\n")
    for level in df_cb_vars["level"].unique():
        count_sections = len(df_cb_vars[df_cb_vars["level"] == level]["section"].dropna().unique())
        count_level = len(df_cb_vars[df_cb_vars["level"] == level])
        f.write(f"- **{level} Characteristics** ({count_sections} sections, {count_level} variables)\n")
    
    f.write("\nEach of the geographies is represented by a separate geodatabase structure. Within of each of the geographic level geodatabases, each of the four characteristics is represented by a _feature class_ respectively. In order to easily identify each of the sub-groups within each category, the name of the original census table field was adjusted by prepending to it the subgroup identification code. For example, the original field B01001e1 would become D01_B01001e1 in the new feature class for the demographic characteristics.\n\nA more detailed description of each sub-group within each of the four feature classes representing the ACS table characteristics is provided below. The table's columns represent: the subgroup's code; its descriptive name;the universe (summative) level of the reference; the ACS Census table in which the original fields are located; the fields/variables of the data, and; how many fields are included in the subgroup.")
    for level in df_cb_vars["level"].unique():
        count_sections = len(df_cb_vars[df_cb_vars["level"] == level]["section"].dropna().unique())
        count_level = len(df_cb_vars[df_cb_vars["level"] == level])
        level_header = f"\n\n\n## 📚 {level} Characteristics ({count_sections} sections, {count_level} variables)\n"
        f.write(level_header)
        f.write("\nThe demographic characteristics selected for spatial representation can be found in ACS data tables X1-X5. They are divided in 8 subgroups: total population, sex and age, median age by sex and race, race, race alone or in combination with other races, hispanic or latino, and citizen voting age population.\n")
        f.write("\nCode | Name | Variable Count |\n| --- | --- | --- |\n")
        for section in df_cb_vars[df_cb_vars["level"] == level]["section"].dropna().unique():
            # find the section_name for the current level and section
            section_name = df_cb_vars[(df_cb_vars["level"] == level) & (df_cb_vars["section"] == section)]["section_name"].dropna().unique()[0]
            count_section = len(df_cb_vars[(df_cb_vars["level"] == level) & (df_cb_vars["section"] == section)])

            section_link = f"#-{section.lower()}-{section_name.replace(" ", "-").lower()}-{count_section}-variables"
            f.write(f"| [{section}]({section_link}) | {section_name} | {count_section} |\n")


        for section in df_cb_vars[df_cb_vars["level"] == level]["section"].dropna().unique():
            # find the section_name for the current level and section
            section_name = df_cb_vars[(df_cb_vars["level"] == level) & (df_cb_vars["section"] == section)]["section_name"].dropna().unique()[0]
            count_section = len(df_cb_vars[(df_cb_vars["level"] == level) & (df_cb_vars["section"] == section)])
            section_header = f"\n### 🏷️ {section}: {section_name} ({count_section} variables)\n"
            f.write(section_header)
            f.write("\n> ")
            for markdown in df_cb_vars[(df_cb_vars["level"] == level) & (df_cb_vars["section"] == section)]["markdown"].unique():
                f.write(f"{markdown}; ")
                f.write("\n")
    f.write("\n")
    f.write("---\n\n")
    f.close()


for level in df_cb_vars["level"].unique():

        print(df_cb_vars[(df_cb_vars['level'] == level) & (df_cb_vars['section'] == section)])

ocacs_cb_vars = ocacs.construct_master_variables_dict(write_to_file = True)



#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
## fx: ACS variables codebook ----
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def acs_cb_variables(year: int, write_to_disk: Optional[bool] = False) -> pd.DataFrame:
    """
    Fetches the ACS CB variables for the specified year(s) and returns a DataFrame containing the variable information.

    Parameters:
    - year: Integer specifying the ACS year to fetch variables for.
    - write_to_disk: Optional boolean indicating whether to write the fetched variables to a file. Default is False.

    Returns:
    - A pandas DataFrame containing the variable information for the specified year(s).
    """
    # Get the list of available ACS years
    years = ocacs.acs5_years
    # If the year is provided and is integer

    if year is not None:
        if isinstance(year, int) and year in years:
            print(f"Year {year} is valid. Proceeding with variable fetch.")
        else:
            if not isinstance(year, int):
                raise ValueError("Year must be an integer.")
            elif year not in years:
                raise ValueError(f"Year must be one of the following: {years}")

    # # Initialize an empty DataFrame to store the variable information across all years
    # master_df = pd.DataFrame()
    # cum_df = pd.DataFrame()

    # Load the master JSON variables codebook
    ocacs_cb_vars_path = os.path.join(prj_dirs["codebook"], f"ocacs_cb_vars.json")
    if os.path.exists(ocacs_cb_vars_path):
        with open(ocacs_cb_vars_path, "r", encoding = "utf-8") as f:
            ocacs_cb_vars = json.load(f)
        print(f"Master variables codebook loaded from {ocacs_cb_vars_path}")
    else:
        print(f"Master variables codebook not found at {ocacs_cb_vars_path}")
        return None

    # Get the variable dictionary for the specified year from the master codebook
    var_cb = ocacs_cb_vars.get(str(year), {})

    # Get the list of variables for each level and section for the specified year from the master codebook
    demographic_variables = var_cb.get("Demographic", {}).get("all_variables", [])
    social_variables = var_cb.get("Social", {}).get("all_variables", [])
    economic_variables = var_cb.get("Economic", {}).get("all_variables", [])
    housing_variables = var_cb.get("Housing", {}).get("all_variables", [])

    # Combine all variables into a single list for easier filtering
    all_variables = set(demographic_variables) | set(social_variables) | set(economic_variables) | set(housing_variables)

    # Initialize the variable dictionary for the current year
    cb = dict()
    
    # Construct the API URL for the specified year
    print(f"\nFetching ACS variables for year {year}...")
    api_url = f"https://api.census.gov/data/{year}/acs/acs5/variables.json"
    s = requests.Session()

    # Make the API request and parse the JSON response
    resp = s.get(api_url)
    resp.raise_for_status()
    data = resp.json()

    # Extract variables from the response
    raw_variables = data.get("variables", {})
    print(f"- Total variables fetched for {year}: {len(raw_variables):,}")

    # Keep only variables that start with a letter, followed by a digit,
    # and end with a capital 'E' (e.g. 'B01001_001E').
    pattern = re.compile(r'^[A-Za-z]\d.*E$')

    # Filter variables based on the pattern
    variables = {k: v for k, v in raw_variables.items() if pattern.match(k)}
    print(f"- Variables after filtering for {year}: {len(variables):,}")

    # Selecting only the variables that are in the master codebook for the current year
    variables = {k: v for k, v in variables.items() if k in all_variables}
    print(f"- Variables after selection for {year}: {len(variables):,}")

    for var, values in variables.items():
        if "label" in values:
            # make sure the label is string
            if not isinstance(values["label"], str):
                values["label"] = str(values["label"])

        s = values["label"]
        # First pass
        s = s.replace("!!", ": ")
        s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode("ascii")
        s = re.sub(r"[^A-Za-z0-9\s:\-]", "", s)
        s = re.sub(r"\s*-\s*", "-", s)
        s = re.sub(r"-{2,}", "-", s)
        s = re.sub(r"(?<![A-Za-z0-9])-|-(?![A-Za-z0-9])", "", s)
        s = re.sub(r":{2,}", ":", s)
        s = re.sub(r"\s*:\s*", ": ", s)
        s = re.sub(r"\s+", " ", s)
        s = s.strip(" \t\n\r:-")

        # Second pass to ensure idempotency (remove any artifacts left by first pass)
        s = re.sub(r"-{2,}", "-", s)
        s = re.sub(r"(?<![A-Za-z0-9])-|-(?![A-Za-z0-9])", "", s)
        s = re.sub(r":{2,}", ":", s)
        s = re.sub(r"\s*:\s*", ": ", s)
        s = re.sub(r"\s+", " ", s)
        s = s.strip(" \t\n\r:-")

        values["label"] = s
        values["table"] = var[:3]
        values["alias"] = re.sub(r"^Estimate\s*: *", "", s)
        # # Convert all words in alias to lowercase
        # values["alias_match"] = values["alias"].lower()

        if var in demographic_variables:
            values["level"] = "Demographic"
            for section, section_content in var_cb.get("Demographic", {}).items():
                if section == "all_variables":
                    continue
                if var in section_content.get("variables", []):
                    values["section"] = section_content["section"]
                    values["section_name"] = section_content["section_name"]
                    values["alias"] = section_content["variables"].get(var, values["alias"])    
                    break                
        elif var in social_variables:
            values["level"] = "Social"
            for section, section_content in var_cb.get("Social", {}).items():
                if section == "all_variables":
                    continue
                if var in section_content.get("variables", []):
                    values["section"] = section_content["section"]
                    values["section_name"] = section_content["section_name"]
                    values["alias"] = section_content["variables"].get(var, values["alias"])
                    break
        elif var in economic_variables:
            values["level"] = "Economic"
            for section, section_content in var_cb.get("Economic", {}).items():
                if section == "all_variables":
                    continue
                if var in section_content.get("variables", []):
                    values["section"] = section_content["section"]
                    values["section_name"] = section_content["section_name"]
                    values["alias"] = section_content["variables"].get(var, values["alias"])
                    break
        elif var in housing_variables:
            values["level"] = "Housing"
            for section, section_content in var_cb.get("Housing", {}).items():
                if section == "all_variables":
                    continue
                if var in section_content.get("variables", []):
                    values["section"] = section_content["section"]
                    values["section_name"] = section_content["section_name"]
                    values["alias"] = section_content["variables"].get(var, values["alias"])
                    break
        else:
            values["level"] = "Unknown"
            values["section"] = None
            values["section_name"] = None
            values["alias"] = None

        # Construct the variable dictionary for the current variable and add it to the main dictionary under the current year
        cb[var] = {
            "year": year,
            "table": values.get("table", None),
            "group": values.get("group", None),
            "variable": var,
            "alias": values.get("alias", None),
            "level": values.get("level", None),
            "section": values.get("section", None),
            "section_name": values.get("section_name", None),
            "markdown": f"🆔 {var}: {values.get('alias', None)}",
            "label": values.get("label", None),
            "concept": values.get("concept", None),
            "type": values.get("predicateType", None),
            "limit": values.get("limit", None),
            "attributes": values.get("attributes", None),
            "note": None
        }

    # Order the variable dictionary by the variable code
    cb = dict(sorted(cb.items(), key=lambda item: item[0]))

    if write_to_disk:
        print("- Writing to JSON file...")
        # Write the variable dictionary to a JSON file
        output_path = os.path.join(prj_dirs["codebook"], f"ocacs_cb_vars_{year}.json")
        with open(output_path, "w", encoding = "utf-8") as f:
            json.dump(cb, f, indent = 4)

    # Convert the variable dictionary to a pandas DataFrame for easier analysis and manipulation
    cb_rows = []
    for var_info in cb.values():
        cb_rows.append(var_info)
    df_cb = pd.DataFrame(cb_rows)
    # Sort the DataFrame by variable, level, and section
    df_cb = df_cb.sort_values(by=["level", "section", "variable"]).reset_index(drop = True)

    print(f"DataFrame for {year} created with {len(df_cb):,} rows and {len(df_cb.columns):,} columns.")
    print(df_cb.head())

    print(f"- Variable dictionary and data frame construction for {year} complete.\n")

    md_header = "# Orange County ACS 5-Year Geodemographics Documentation <br> **Demographic Characteristics**"

















    # Loop through the ACS years
    for acs_year in years:

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
