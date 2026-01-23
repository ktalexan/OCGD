import os

yearDict = {
    "2013": "113",
    "2014": "114",
    "2015": "114",
    "2016": "115",
    "2017": "115",
    "2018": "116",
    "2019": "116",
    "2020": "116",
    "2021": "116"
}

codeDir = os.path.expanduser("~\Box\KA Personal Folder\Projects\Github\OCACS-Geodemographics\Code")
prjPathDict = {}
for y in yearDict:
    year = int(y)
    cdn = int(yearDict[y])
    prjPath = os.path.expanduser(f"~\Box\KA Personal Folder\Projects\OCGD\OCACS\OCACS{year}")
    prjPathDict[year] = prjPath

# The following function can be run to execute the metadata structure (only metadata no ACS data processing) for either a single year's folder, or for "ALL" the years in the provided list of folders. The function takes two arguments:

# - *prjPathList*: The list or string of folder path(s). If it is a single string path, then the next argument (period) must be an integer year entry.
# - *period*: Either a single time period (year) as an integer which will run a single year metadata folder processing, or "ALL" which will run the metadata processing in a range of folders specified in the project path list. If "ALL" the path list must be a list and not a single path string.

# Any other inputs, will result in termination of the function.

def run_metadata(prjPathList, period):
    """Running Metadata instances for OCACS geodatabases and feature layers

    Args:
        prjPathList (string or list): Flexible: can be a list of project folders (OCACS years) or a single project directory containing OCACS geodatabases.
        period (integer year or "ALL"): if single year, will run the single geodatabase folder structure. If "ALL" will run all in list (path directories above must be list.)
    """
    from ocacs_metadata import ocacs_metadata
    if (isinstance(period, int)) and (period in range(2013,2022)) and (isinstance(prjPathList, list)):
        ocacs_metadata(prjPathList[period])
    elif (isinstance(period, int)) and (period in range(2013,2022)) and (isinstance(prjPathList, str)):
        ocacs_metadata(prjPathList)
    elif (isinstance(period, str)) and (period == "ALL") and (isinstance(prjPathList, list)):
        i = 0
        for path in prjPathDict:
            i += 1
            prjPath = prjPathDict[path]
            print(f"{i}. PROCESSING YEAR: {path}\n")
            ocacs_metadata(prjPath)
    else: print("Entry not valid. Exiting program...")
    
