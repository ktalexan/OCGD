from ACS.ocacs import ocacs
import os

import arcpy

#year = 2017
#est = 5
#year = 2018
#est = 5
year = 2019
est = 5

prefix = f"ACS{year}Y{est}"
#prjDir = r"E:\Dev\Repos\OCGeoDemographics\ACS"
#prjDir = r"C:\Users\ktale\Source\Repos\ktalexan\OCGeoDemographics\ACS"
prjdir = r"C:\Users\ktalexan\Documents\GitHub\OCGeoDemographics\ACS"
#dataOrigin = r"E:\ACS2017"
#dataOrigin = r"D:\OneDrive - County of Orange\Projects\OCGeodemographics\OCACS\OCACS2018"
dataOrigin = r"C:\Users\ktalexan\OneDrive - County of Orange\Projects\OCGeodemographics\OCACS\OCACS2019"

os.chdir(prjDir)


#acs17 = ocacs(year, est, dataOrigin, prjDir)
#acs18 = ocacs(dataOrigin)
acs19 = ocacs(dataOrigin)

# acs18.acsCreateGdbStructure()
# acs18.acsAddGdbAlias()

# acs17.acsCreateGdbStructure()
# acs17.acsAddGdbAlias()

acs19.acsCreateGdbStructure()
acs19.acAddGdbAlias()


xlsxMetadata = os.path.join(prjDir, "Metadata and Documentation", "MasterMetadata.xlsx")

# Dictionary containing codes and aliases for each of the project's geography levels.
geoNames = {
    "BG": "Block Groups",
    "CD115": "Congressional Districts, 115th US Congress",
    "COUNTY": "Orange County",
    "COUSUB": "County Subdivisions",
    "PLACE": "Cities",
    "PUMA": "Public Use Microdata Areas",
    "SDE": "Elementary School Districts",
    "SDS": "Secondary School Districts",
    "SDU": "Unified School Districts",
    "SLDL": "State Assembly Legislative Districts",
    "SLDU": "State Senate Legislative Districts",
    "TRACT": "Census Tracts",
    "UA": "Urban Areas",
    "ZCTA": "ZIP Code Tabulation Areas"
}
# List of all the geographic code levels
geoLevels = [key for key in geoNames.keys()]

arcpy.env.workspace = dataOrigin
arcpy.env.overwriteOutput = True

workspaces = {l: arcpy.ListWorkspaces(f"ACS*{l}*", "FileGDB")[0] for l in geoLevels}

for layer in workspaces:
    print(workspaces[layer])
