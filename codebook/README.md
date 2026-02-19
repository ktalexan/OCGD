# OCGD Codebook Repository Folder

This folder contains codebooks that provide detailed information about the datasets used in this project. Each codebook includes descriptions of variables, data collection methods, and any relevant metadata to help users understand and utilize the datasets effectively.

Most codebooks are in JSON format for easy integration with data processing tools, while some are provided in csv, excel, or Markdown format for better readability.

## Basic Codebook Structure and Files

### OCTL Codebook Data Collection

- `octl_cb_twr.json`: This codebook contains information about the Tigerweb REST API data collection process, including variable descriptions and data collection methods.
- `octl_cb_master.json`: This codebook provides a comprehensive overview of the master dataset, including variable descriptions, data sources, metadata, and any transformations applied to the data.
- `octl_cb_{year}.json`: These codebooks contain information about the ACS datasets for each year, including variable descriptions, data sources, metadata, and any transformations applied to the data.

### OCACS Codebook Data Collection

- `ocacs_cb_vars.json/xlsx`: This codebook contains information about the variables in the OCACS datasets, including variable descriptions, data sources, metadata, and any transformations applied to the data. It exists in both JSON and Excel formats for ease of use.
- `ocacs_cb_vars_{year}.json`: These codebooks contain information about the variables in the OCACS datasets for each year, including variable descriptions, data sources, metadata, and any transformations applied to the data. They are provided in JSON format for easy integration with data processing tools.