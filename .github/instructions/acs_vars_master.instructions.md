---
applyTo: "documentation/acs_variables.md"
---
# ACS Variables Master Instructions

Perform the following steps to the content of the markdown file:

- The markdown file contains:
    1. First level headings indicating different categories (omitting the code before the colon).
    2. Second level headings indicating group categories within each first level heading (omitting the code before the colon and parentheses).
    3. Lines of variable definitions formatted as "VariableName (Alias);".

- I want to create a new JSON structure from the variable definitions without changing the contents of the markdown file. The new JSON structure should have the following structure with the following specifications:
    1. The JSON structure should have firs level keys as the category names (from first level headings, omitting the part before the colon).
    2. Seperate the content of the variable definitions into individual lines by splitting at each ";" character when preciding a parenthesis close ")".
    3. For each line, trim any leading or trailing whitespace.
    4. Each line now contains a variable name, followed by an alias in parentheses.
    5. For each variable name, replace the e### with "_###E" where ### represents one, two, or three digits. Pad with leading zeros if necessary to ensure three digits. For example, "e1" becomes "_001E", "e12" becomes "_012E", and "e123" becomes "_123E".
    6. Convert the first part of the line (the variable name) to into a dictionary key within each of the category keys, and the alias (the part inside the parentheses) to the corresponding value with key "alias". Also add the following additional key-value pairs:
        - "id": An auto-incremented integer starting from 1. Restart the numbering for each category.
        - "name": The variable name after the e### replacement.
        - "alias": The alias extracted from the parentheses.
        - "description": An empty string.
        - "label": An empty string.
        - "type": An empty string.
        - "description": An empty string.
        - "type": An empty string.
        - "category": The category name from the first level heading, omitting the part in parentheses.
        - "group_category": The group category name from the second level heading without the part before the colon and the part in parentheses.
        - "group_count": The number in the second level heading parentheses. Should be an integer.
        - "group": the variable name part before the "_".
        - "group_code": The group code extracted from the second level heading from the part before the colon.
        - "limit": An empty string.
        - "attributes": An empty string.

- The resulting JSON structure should look like this:
{
  "CategoryName1": {
    "VariableName1": {
      "id": 1,
      "name": "VariableName1_after_replacement",
      "alias": "Alias1",
      "description": "",
      "label": "",
      "type": "",
      "category": "CategoryName1",
      "group_category": "GroupCategory1",
      "group_count": GroupCount1,
      "group": "VariableName1_part_before_underscore",
      "group_code": "",
      "limit": "",
      "attributes": ""
    },
    ...
  },
  "CategoryName2": {
    ...
  }
}

- Save the resulting JSON structure to a file named "acs_variables_master.json" in the "codebook" folder of the project.

- If using any scripting or programming language, save any code files used to generate the JSON structure in the "scripts" folder of the project.
