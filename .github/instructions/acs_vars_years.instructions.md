---
applyTo: "codebook/acs_variables_master.json"
---
# ACS Variables Master Instructions

- Using the ACS Variables Master file (`codebook/acs_variables_master.json`), create multiple JSON files that organize ACS variables by year. Each output file should be named `acs_variables_{year}.json`, where `{year}` corresponds to the specific year of the ACS data. The current years available in the master file are 2010 through 2023 (inclusive).
- Copy the contents of the master file into each year-specific file
- Using the "check_census_var.py" script, filter the variables in each year-specific file to include only those that are valid for that particular year. Specifically:
    - For each of the JSON file for that year, use the year as an argument to the script to filter the variables, and for each of the JSON keys within each level one category of the JSON file, use the key as the second argument to the script.
    - The results of the "check_census_var.py" script should be used to determine whether to keep or remove each variable from the year-specific file, and to alter the contents of the key's value to reflect the valid variable information for that year.
    - For each key within each level one category of the JSON file, update the following key values based on the output of the "check_census_var.py" script:
        - "label": Update to the "label" output of the "check_census_var.py" script for that year.
        - "group_category": Update to the "concept" output of the "check_census_var.py" script for that year, converted to sentence case (i.e., first letter capitalized, rest lowercase).
        - "type": update to the "predicateType" output of the "check_census_var.py" script for that year.
        - "group": update to the "group" output of the "check_census_var.py" script for that year.
        - "limit": update to the "limit" output of the "check_census_var.py" script for that year.
        - "attributes": update to the "attributes" output of the "check_census_var.py" script for that year.
    - If a variable is not valid for that year, remove it from the year-specific file
- If using any scripting or programming language, save any code files used to generate the JSON structure in the "scripts" folder of the project.
