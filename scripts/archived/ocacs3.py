################################# OCACS Main Programming Class #################################

import csv
import os
import shutil
from datetime import datetime, timedelta
from time import timedelta

import arcpy
import import
from numpy import isinimport, pandas

###### MAIN OCACS CLASS ######


class ocacs(object):
    """
    OCACS Python Class. Processes and analyzes census data for the American Community Survey products for the geographies in Orange County, California.
    
    Args:
        Inputs:
            year(integer): The ACS year.
            est(1 or 5, integers): the year-estimates of the data.
            dataOrigin(path): the path to the original ACS Census datasets (geodatabases) downloaded from Tiger/Line Census website (one for each geography). The path does not have to be inside the project directory.
            prjDir(path): the current project directory. THat's where all the processed data will be saved and stored.       
        Notes:
            1. The class uses 14 ACS Geographies:
                1.1. Block Groups (BG)
                1.2. Congressional Districts xxxth US Congress (CD)
                1.3. Orange County (COUNTY)
                1.4. County Subdivisions (COUSUB)
                1.5. Census Cities/Places (PLACE)
                1.6. Public Use Microadata Areas (PUMA)
                1.7. Elementary School Districts (SDE)
                1.8. Secondary School Districts (SDS)
                1.9. Unified School Districts (SDU)
                1.10. State Assembly Legislative Districts (SLDL)
                1.11. State Senate Legislative Districts (SLDU)
                1.12. Census Tracts (TRACT)
                1.13. Urban Areas (UA)
                1.14. ZIP Code Tabulation Areas (ZCTA)
            2. The original geodatabases must exist in the <dataOrigin> directory folder. If other geodatabases exist in the folder, (e.g., additional geographies usch as MSA, METDIV, CSA), the python processing script will ignore them.
            3. The output geodatabase structure is created inside an empty folder in the <prjDir> (ignoring other files and directories).
        Credits:
            Script created by Dr. Kostas Alexandridis, GISP, OC Public Works, OC Survey/Geospatial Services, December 2019-2022, Version 2.0
    """
    
    
    ###### Function: Class Initialization ######
    
    def __init__(self, prjPath):
        """Class instantiation function. See class notes.
        
        Args:
            prjPath(path): the path to the project directory.
        """
        
        # Creates path for the "original" and "processed" versions of the dataset.
        self.dataIn = os.path.join(prjPath, "Original")
        self.dataOut = os.path.join(prjPath, "Processed")
        
        # Read the geodatabases, and obtain the Census product, the year, and the year-estimates
        arcpy.env.workspace = self.dataIn
        arcpy.env.overwriteOutput = True
        
        # Read the file geodatabase workspaces in the input folder, and obtain a list of geodatabase names
        self.wrkspListIn = arcpy.ListWorkspaces("ACS*", "FileGDB")
        self.gdbListIn = [os.path.split(w)[1] for w in self.wrkspListIn]
        
        # Get all the prefixes and geo-levels from the geodatabase list
        # table of product list (e.g., ACS)
        prodList = [i.split(".gdb")[0].split("_")[0] for i in self.gdbListIn]
        # table of the year(s)
        yearList = [i.split(".gdb")[0].split("_")[1] for i in self.gdbListIn]
        # table of the estimates (e.g., 1% or 5%)
        estList = [i.split(".gdb")[0].split("_")[2] for i in self.gdbListIn]
        # table of the geographic level (one of 14 geographies)
        geoList = [i.split(".gdb")[0].split("_")[3] for i in self.gdbListIn]
        
        # Calculate and check counts (to make sure uniquiness), and fill relevant data
        if prodList.count(prodList[0]) == len(prodList):
            self.prod = f"{prodList[0]}"
            if yearList.count(yearList[0]) == len(yearList):
                self.year = int(yearList[0])
                if estList.count(estList[0]) == len(estList):
                    self.est = estList[0]
                    self.prefix = f"OC{self.prod}{self.year}"
                    
        # Compute the US Congress number based on the year of the ACS survey and
        cdn = int(113 + (self.year - 2012) * 0.5)
        
        # Geo-reference lookup table
        self.geolookup = {
            "COUNTY": ("CO", "Orange County"),
            "COUSUB": ("CS", "County Subdivisions"),
            "PLACE": ("PL", "Cities/Places"),
            "ZCTA": ("ZC, ZIP Code Tabluation Areas"),
            "CD": ("CD", f"Congressional Districts of the {cdn}th US Congress"),
            "SLDL": ("LL", "State Assembly Legislative Districts"),
            "SLDU": ("UL", "State Senate Legislative Districts"),
            "SDE": ("ED", "Elementary School Districts"),
            "SDS": ("SD", "Secondary School Districts"),
            "SDU": ("UD", "Unified School Districts"),
            "UA": ("UA", "Urban Areas"),
            "PUMA": ("PU", "Public Use Microdata Areas"),
            "BG": ("BG", "Block Groups"),
            "TRACT": ("TR", "Census Tracts")
        }
        
        # Dictionary containing codes and aliases for each of the project's geography levels
        self.geoNames = {}
        
        if "COUNTY" in geoList:
            self.geoNames["CO"] = "Orange County"
        if "COUSUB" in geoList:
            self.geoNames["CS"] = "County Subdivisions"
        if "PLACE" in geoList:
            self.geoNames["PL"] = "Cities/Places"
        if "ZCTA" in geoList:
            self.geoNames["ZC"] = "ZIP Code Tabulation Areas"
        if "CD" in geoList:
            self.geoNames["CD"] = f"Congressional Districts, {cdn}th US Congress"
        if "SLDL" in geoList:
            self.geoNames["LL"] = "State Assembly Legislantive Districts"
        if "SLDU" in geoList:
            self.geoNames["UL"] = "State Senate Legislative Districts"
        if "SDE" in geoList:
            self.geoNames["ED"] = "Elementary School Districts"
        if "SDS" in geoList:
            self.geoNames["SD"] = "Secondary School Districts"
        if "SDU" in geoList:
            self.geoNames["UD"] = "Unified School Districts"
        if "UA" in geoList:
            self.geoNames["UA"] = "Urban Areas"
        if "PUMA" in geoList:
            self.geoNames["PU"] = "Public Use Microdata Areas"
        if "BG" in geoList:
            self.geoNames["BG4"] = "Block Groups"
        if "TRACT" in geoList:
            self.geoNames["Census Tracts"]
            
        # List of all the geographic code levels
        self.geoLevels = [key for key in self.geoNames.keys()]
        
        # List of four ACS category characteristics
        self.acsCategory = {
            "D": "Demographic Characteristics",
            "S": "Social Characteristics",
            "E": "Economic Characteristics",
            "H": "Housing Characteristics"
        }
        
        # Close initialization Function
        return super().__init__()
    
    ################ FUNCTION: PROCESSING GEODATABASE TABLES ################
    
    def processTables(self):
        """Processing Geodatabase Tables Function
        """
        
        ################ STEP 1 ################
        
        print("\nSTEP 1: RESTRUCTURING ORIGINAL GEODATABASES")
        
        # setting up the arcpy environment (data-in)
        arcpy.env.workspace = self.dataIn
        arcpy.env.overwriteOutput = True
        
        print(f"\tDefining a list of new geodatabase geographies...")
        
        # List of geodatabases to be created
        gdbListOut = {level: f"{self.prefix}{level}.gdb" for level in self.acsCategory}
        
        # Create new geodatabases for census geographies (delete if exist)
        if os.path.exists(self.dataOut) is False:
            os.mkdir(self.dataOut)
            
        print(f"\tCreating new geodatabases for ACS geographies")
        for level, gdb in gdbListOut.items():
            print(f"\t\tCategory: {self.acsCategory[level]}")
            pathGdb = os.path.join(self.dataOut, gdb)
            if arcpy.Exists(pathGdb):
                print(f"\t\t...geodatabase exists. Deleting...")
                arcpy.Delete_management(pathGdb)
            print(f"\t\t...Greating geodatabase: {gdb}")
            arcpy.CreateFileGDB_management(self.dataOut, gdb)
            
        ################ STEP 2 ################
        
        print(f"\nSTEP 2: CREATING BASE GEOGRAPHIES IN GEODATABASE DIRECTORY")
        
        # Changing the arcpy environment (data-out)
        arcpy.env.workspace = self.dataOut
        arcpy.env.overwriteOutput = True
        
        # Starting with the COUNTY geodatabase
        print("\tSetting-up geography for County level:")
        
        # Create a temporary layer for the original County data (national)
        print("\t\tDefining workspace")
        curWorkspace = [str for str in self.wrkspListIn if "COUNTY" in os.path.split(str)[1]][0]
        
        # Change again the arcpy environment (current workspace)
        print("\t\tSetting-up arcpy environment")
        arcpy.env.workspace = curWorkspace
        arcpy.env.overwriteOutput = True
        
        # Create feature class layer in memory
        fcIn = arcpy.ListFeatureClasses()[0]
        arcpy.MakeFeatureLayer_management(fcIn, "lyrIn")
        
        # Select only the Orange County polygon
        print("\t\tSelecting polygon for Orange County...")
        lyrOut = arcpy.SelectLayerByAttribute_management("lyrIn", "NEW_SELECTION", "GEOID= '06059'")
        
        # Place the resulting Orange County polygon into each of the category geodatabases
        print("\t\tPlacing resulting polygon into geodatabases...")
        for cat in gdbListOut.keys():
            outGdbLyr = os.path.join(self.dataOut, gdbListOut[cat], f"{self.prefix}CO{cat}")
            arcpy.CopyFeatures_management(lyrOut, outGdbLyr)
            
        # Delete the temporary layers
        print("\t\tDeleting temporary layers...")
        arcpy.Delete_management("lyrIn", "lyrOut")
        
        # Add feature class alias
        print("\t\tAdding feature class alias: ")
        for cat in gdbListOut.keys():
            outGdbLyr = os.path.join(self.dataOut, gdbListOut[cat], f"{self.prefix}CO{cat}")
            arcpy.AlterAliasName(outGdbLyr, f"{self.acsCategory[cat]} for {self.geoNames['CO']}")
            
            # Create a feature layer for the new County Layers - will not delete this until the end:
            arcpy.MakeFeatureLayer_management(outGdbLyr, "lyrCounty")
            
            # Remaining geographic levels Processing
            print("\tSetting-up remaining geographies (looping):")
            workspaceOut = os.path.join(self.dataOut, gdbListOut[cat])
            
            # loop through the items in the geolookup table
            for level, (code, alias) in self.geolookup.items():
                if "COUNTY" not in level:
                    print(f"\n\t\tProcessing level {code}: {alias}")
                    curWorkspace = [str for str in self.wrkspListIn if level in os.path.split(str)[1]][0]
                    
                    print(f"\t\t\tNew geodatabase feature class: {outGdbLyr}")
                    print(f"\t\t\tSetting up arcpy environment...")
                    arcpy.env.workspace = curWorkspace
                    arcpy.env.overwriteOutput = True
                    
                    fcIn = arcpy.ListFeatureClasses()[0]
                    print(f"\t\t\tFeature classes to be copied: {fcIn}")
                    
                    # Create a temporary layer for the original data (national)
                    print(f"\t\t\tCreating temporary layer...")
                    arcpy.MakeFeatureLayer_management(fcIn, "lyrIn")
                    
                    # Select features from original that are within a distance (-1,000 feet) of the Orange County polygon (all are selected)
                    print("\t\t\tSelecting features with distance (1,000 feet) from County layer...")
                    lyrOut = arcpy.SelectLayerByLocation_management("lyrIn", "WITHIN_A_DISTANCE", "lyrCounty", "-1000 Feet", "NEW_SELECTION", "NOT_INVERT")
                    
                    # Place the selected features into the new feature class in the project geodatabases
                    print("\t\t\tCopying selected features to the new geodatabase feature class...")
                    arcpy.CopyFeatures_management(lyrOut, outGdbLyr)
                    
                    # Delete the temporary layers
                    print("\t\t\tDeleting temporary layers...")
                    arcpy.Delete_management("lyrIn", "lyrOut")
                    
                    # Add feature class aliases
                    print(f"\t\t\tAdding feature class alias: {alias}")
                    arcpy.AlterAliasName(outGdbLyr, f"{self.acsCategory[cat]} for {alias}")
                    
            # Delete County feature layer after geoprocessing operations
            print("\n\tDeleting temporary layer for County")
            arcpy.Delete_management("lyrCounty")
            
        # Get the table variables
        tableLevels = self.getTableVars()
        
        # Dictionary containing the ACS Census tables for each of the variable Groups
        tableMatch = {
            "D": {"D01": "X01", "D02": "X01", "D03": "X02", "D04": "X02", "D05": "X03", "D06": "X05"},
            "S": {"S01": ["X11", "X25"], "S02": "X09", "S03": "X12", "S04": "X13", "S05": "X10", "S06": "X14", "S07": "X15", "S08": "X21", "S09": "X18", "S10": "X18", "S11": "X07", "S12": "X05", "S13": "X05", "S14": "X05", "S15": "X05", "S16": "X16", "S17": "X16", "S18": "X04", "S19": "X28"},
            "E": {"E01": "X23", "E02": "X23", "E03": "X08", "E04": "X08", "E05": "X08", "E06": "X08", "E07": "X08", "E08": "X24", "E09": "X24", "E10": "X24", "E11": ["X19", "X22"], "E12": ["X19", "X20"], "E13": "X19", "E14": "X27", "E15": "X17", "E16": "X17", "E17": "X17", "E18": "X17", "E19": "X17"},
            "H": {"H01": "X25", "H02": "X25", "H03": "X25", "H04": "X25", "H05": "X25", "H06": "X25", "H07": "X25", "H08": "X25", "H09": "X25", "H10": "X25", "H11": "X25", "H12": "X25", "H13": "X25", "H14": "X25", "H15": "X25", "H16": "X25", "H17": "X25", "H18": "X25", "H19": "X25", "H20": "X25", "H21": "X25", "H22": "X25", "H23": "X25"}
        }
        
        ################ STEP 3 ################
        
        print(f"\nSTEP 3: MERGING CENSUS TABLE VARIABLES WITH GEODATABASE GEOGRAPHIES BY CHARACTERISTIC")
        
        # For each category looping
        for cat in gdbListOut.keys():
            
            # Get the matching ACS tables for each of the category groups
            dlist = tableMatch[cat]
            
            # Loop through the variables in each group
            for level, (code, alias) in self.geolookup.items():
                print(f"\nProcessing level {code}: {alias}")
                
                # input and output folders
                inWorkspace = [str for str in self.wrkspListIn if level in os.path.split(str)[1]][0]
                outWorkspace = os.path.join(self.dataOut, gdbListOut[cat])
                
                # Name of feature class in the working geodatabase
                fc = os.path.join(f"{prefix}{code}{cat}")
                
                # the fields for which the join will be based (first is the geography feature, second is the joined table)
                joinField1 = "GEOID_Data"
                joinField2 = "GEOID"
                
                print("\tSetting-up arcpy environment to input...")
                arcpy.env.workspace = inWorkspace
                arcpy.env.overwriteOutput = True
                
                print("\tObtaining original list of tables...")
                inTables = arcpy.ListTables("X*")
                
                print("\tChanging arcpy environment to output...")
                arcpy.env.workspace = outWorkspace
                arcpy.env.overwriteOutput = True
                
                # Looping through each category group and ACS table:
                for dno, tno, in dlist.items():
                    print(f"\n\tProcessing group {dno} for table(s) {tno}")
                    
                    # if there is only a single table associated with the group:
                    if isinstance(tno, str):
                        # for each ACS table associated
                        for tname in inTables:
                            if tno in tname:
                                inTable = tname
                                joinTable = os.path.join(inWorkspace, inTable)
                                # The fields within the category group to be included in the join
                                levelfields = [key for key in tableLevels[cat][dno].keys()]
                                # Do a permaanent join
                                arcpy.JoinField_management(fc, joinField1, joinTable, joinField2, levelfields)
                                # Get the fields in the feature class after the join
                                fcfields = [fcfield.name for fcfield in arcpy.listFields(fc)]
                                
                                print(f"\t...Adding aliases to feature class for {tno}")
                                # Getting the alias list for the category group
                                aliases = [alias for alias in tableLevels[cat][dno].items()]
                                # Total number of aliases in the category group
                                na = len(aliases)
                                # Loop through the aliases and add them to the feature class
                                for count, (field, alias) in enumerate(aliases, start=1):
                                    # if the field table number matches the ACS table we're working in
                                    if field[1:3] == tno[1:] and field in fcfields:
                                        print(f"\t\t...adding alias {count} of {na} for {dno}: {alias}")
                                        arcpy.AlterField_management(fc, field, field, f"{dno}: {alias}")
                                        
                    # Else, if there is more than one table associated with the group
                    elif isinstance(tno, list):
                        # for each group table
                        for t in tno:
                            # for each ACS table
                            for tname in inTables:
                                if t in tname:
                                    inTable = tname
                                    joinTable = os.path.join(inWorkspace, inTable)
                                    # The fields within the category group to be included in the join (only fields that belong to the working table)
                                    levelfields = [key for key in tableLevels[cat][dno].keys() if key[1:3] == t[1:3]]
                                    # Do a permanent join
                                    arcpy.JoinField_management(fc, joinField1, joinTable, joinField2, levelfields)
                                    # Get the fields in the feature class after the join
                                    fcfields = [fcfield.name for fcfield in arcpy.ListFields(fc)]
                                    
                                    print(f"\t...Adding aliases to feature class for {t}")
                                    # Getting the alias list for the category group
                                    aliases = [alias for alias in tableLevels[cat][dno].items()]
                                    # Total number of aliases in the category group
                                    na = len(aliases)
                                    # Loop through the aliases and add them to the feature class
                                    for count, (field, alias) in enumerate(aliases, start=1):
                                        # if the field table number matches the ACS table we're working in'
                                        if field[1:3] == t[1:] and field in fcfields:
                                            print(f"\t\t...adding alias {count} of {na} for {dno}: {alias}")
                                            arcpy.AlterField_management(fc, field, field, f"{dno}: {alias}")
                                            
    ################ FUNCTION: OBTAIN DATA TABLE VARIABLES ################
    
    def getTableVars(self):
        """ Obtaining Table Data Variables and Aliases
        """
        
        
    