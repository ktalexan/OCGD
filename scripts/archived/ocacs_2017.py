# ACS Geodemographics Code Execution Script
# Version 3, May 2023
# Dr. Kostas Alexandridis, GISP, OC Survey Geospatial Services


# Preliminaries
# Import necessary libraries
import os, arcpy
from getpass import getpass

# OCACS 2017
# May 2023

# Defining inputs for OCACS year, and estimate (1, 3, or 5 year). This will format the prefix for the files as well.
year = "2017"
est = "5"
prefix = f"ACS{year}Y{est}"
print(f"Year: {year}")
print(f"Estimate: {est}")
print(f"Prefix for Files: {prefix}")

# Defining the project directory (where the code is stored and executed from), and the original data storage directory (where the original downloaded datasets are located)
#  1. Code Directory: The directory where the Python execution class is located
#  2. Project Path (prjPath): The parent where the original data (unprocessed) are located and the processed data will be stored
codeDir = getpass(prompt = "Code Execution Directory: ")
prjPath = getpass(prompt= "Data Storage Parent Directory: ")

# Change the current directory, so the code class can be loaded into memory
codeDir, prjPath

# Change the current directory, so the code class can be loaded into memory, and import the '**ocacs**' Python class
os.chdir(codeDir)
from ocacs import ocacs

# Create a new *ocacs* class instantiation for the OCACS 2020 data
acs20 = ocacs(prjPath)


