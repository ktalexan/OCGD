import os, arcpy
from arcpy import metadata as md

def ocacs_metadata(prjPath):
    """OCACS Python Class for Metadata Only

    Args:
        prjPath (folder path): link to geodatabase folder (processed) for updating metadatay
    """
    
    print("\nCOMPILING AND WRITING OUT METADATA TO GEODATABASES AND LAYERS")
    
    
    print("\tSetting up arcpy environment for metadata processing...")
    # Obtain the Data folders in the project directory
    dataIn = os.path.join(prjPath, "Original")
    dataOut = os.path.join(prjPath, "Processed")
    
    
    # Set and obtain the workspaces (geodatabases) in the folder
    arcpy.env.workspace = dataOut
    workspaces = arcpy.ListWorkspaces("*", "FileGDB")
    
    # Get the year and cdn
    year = int(os.path.split(prjPath)[1].split("OCACS")[1])
    cdn = int([s for s in os.listdir(dataIn) if "_CD_" in s][0].split(".gdb")[0].split("_CD_")[1])
    
    # Obtain the geodatabase list (no path)
    gdbListIn = [os.path.split(w)[1] for w in workspaces]
    
    # Define the basic Tags
    basicTags = "geodemographics, Orange County, California, US Census, OCACS, ACS, American Community Survey"
    
    print("\tSetting up metadata dictionaries...")
    # Geodatabase Metadata Template
    cDictionary = {
        "D": {
            "Name": "Demographic Characteristics",
            "Tags": f"{basicTags}, Demographic Characteristics, age, sex, race, Hispanic or Latino, citizen, voting",
            "Description": f"US Census American Community Survey (ACS) {year}, 5-year estimates of the key demographic characteristics of multiple geographic levels (county; county subdivisions; cities; ZIP codes; congressional, state assembly and state senate districts; elementary, secondary and unified educational districts; urban areas, PUMA, census tracts and block groups) for Orange County, California. The data contains 105 fields for the variable groups D01: Sex and age (universe: total population, table X1, 49 fields); D02: Median age by sex and race (universe: total population, table X1, 12 fields); D03: Race (universe: total population, table X2, 8 fields); D04: Race alone or in combination with one or more other races (universe: total population, table X2, 7 fields); D05: Hispanic or Latino and race (universe: total population, table X3, 21 fields), and; D06: Citizen voting age population (universe: citizen, 18 and over, table X5, 8 fields). The US Census geodemographic data are based on the {year} TigerLines across multiple geographies. The spatial geographies were merged with ACS data tables. See full documentation at the OCACS project github page (<a href='https://github.com/ktalexan/OCACS-Geodemographics' target='blank'>https://github.com/ktalexan/OCACS-Geodemographics</a>).",
            "Thumbnail": "https://github.com/ktalexan/OCACS-Geodemographics/blob/main/Images/OCDemographicCharacteristics.jpg?raw=true",
            "Fields": "The data contains 105 fields for the variable groups D01: Sex and age (universe: total population, table X1, 49 fields); D02: Median age by sex and race (universe: total population, table X1, 12 fields); D03: Race (universe: total population, table X2, 8 fields); D04: Race alone or in combination with one or more other races (universe: total population, table X2, 7 fields); D05: Hispanic or Latino and race (universe: total population, table X3, 21 fields), and; D06: Citizen voting age population (universe: citizen, 18 and over, table X5, 8 fields)."
        },
        "S": {
            "Name": "Social Characteristics",
            "Tags": f"{basicTags}, Social Characteristics, households, relationship, marital status, Fertility, grandparents, school enrollment, educational attainment, veteran status, disability, residence, place of birth, citizenship, region of birth, language spoken, ancestry, computer use, internet use",
            "Description": f"US Census American Community Survey (ACS) {year}, 5-year estimates of the key social characteristics of multiple geographic levels (county; county subdivisions; cities; ZIP codes; congressional, state assembly and state senate districts; elementary, secondary and unified educational districts; urban areas, PUMA, census tracts and block groups) for Orange County, California. The data contains 500 fields for the variable groups S01: Households by type (universe: total households, table X11, 17 fields); S02: Relationship (universe: population in households, table X9, 19 fields); S03: Marital status (universe: population 15 years and over, table X12, 13 fields); S04: Fertility (universe: women 15-50 years who had birth in the past 12 months, table X13, 11 fields); S05: Grandparents (universe: grandparents living or responsible for own grandchildren under 18 years, table X10, 18 fields); S06: School enrollment (universe: population 3 years old and over enrolled in school, table X14, 17 fields); S07: Educational attainment (universe: population 25 years and over, table X15, 25 fields); S08: Veteran status (universe: civilian population 18 years and over, table X21, 2 fields); S09: Disability status and type by sex and age (universe: total civilian non-institutionalized population, table X18, 77 fields); S10: Disability status by age and health insurance coverage (universe: civilian non-institutionalized population, table X18, 16 fields); S11: Residence 1 year ago (universe: population 1 year and over, table X7, 6 fields); S12: Place of birth (universe: total population, table X5, 27 fields); S13: Citizenship status by nativity in the US (universe: total population, table X5, 6 fields); S14: Year of entry (universe: population born outside the US, table X5, 21 fields); S15: World region of birth of foreign born population (universe: foreign born population, excluding population born at sea, table X5, 25 fields); S16: Language spoken in households (universe: total households, table X16, 6 fields); S17: Language spoken at home (universe: population 5 years and over, table X16, 67 fields); S18: Ancestry (universe: total population reporting ancestry, table X4, 114 fields), and; S19: Computers and internet use (universe: total population in households and total households, table X28, 13 fields). The US Census geodemographic data are based on the {year} TigerLines across multiple geographies. The spatial geographies were merged with ACS data tables. See full documentation at the OCACS project GitHub page (<a href='https://github.com/ktalexan/OCACS-Geodemographics' target='blank'>https://github.com/ktalexan/OCACS-Geodemographics</a>).",
            "Thumbnail": "https://github.com/ktalexan/OCACS-Geodemographics/blob/main/Images/OCSocialCharacteristics.jpg?raw=true",
            "Fields": "The data contains 500 fields for the variable groups S01: Households by type (universe: total households, table X11, 17 fields); S02: Relationship (universe: population in households, table X9, 19 fields); S03: Marital status (universe: population 15 years and over, table X12, 13 fields); S04: Fertility (universe: women 15-50 years who had birth in the past 12 months, table X13, 11 fields); S05: Grandparents (universe: grandparents living or responsible for own grandchildren under 18 years, table X10, 18 fields); S06: School enrollment (universe: population 3 years old and over enrolled in school, table X14, 17 fields); S07: Educational attainment (universe: population 25 years and over, table X15, 25 fields); S08: Veteran status (universe: civilian population 18 years and over, table X21, 2 fields); S09: Disability status and type by sex and age (universe: total civilian non-institutionalized population, table X18, 77 fields); S10: Disability status by age and health insurance coverage (universe: civilian non-institutionalized population, table X18, 16 fields); S11: Residence 1 year ago (universe: population 1 year and over, table X7, 6 fields); S12: Place of birth (universe: total population, table X5, 27 fields); S13: Citizenship status by nativity in the US (universe: total population, table X5, 6 fields); S14: Year of entry (universe: population born outside the US, table X5, 21 fields); S15: World region of birth of foreign born population (universe: foreign born population, excluding population born at sea, table X5, 25 fields); S16: Language spoken in households (universe: total households, table X16, 6 fields); S17: Language spoken at home (universe: population 5 years and over, table X16, 67 fields); S18: Ancestry (universe: total population reporting ancestry, table X4, 114 fields), and; S19: Computers and internet use (universe: total population in households and total households, table X28, 13 fields)."
        },
        "E": {
            "Name": "Economic Characteristics",
            "Tags": f"{basicTags}, Economic Characteristics, employment status, work status, worker, commuting, travel time, vehicles, transportation, occupation, industry, class of worker, income, earnings, health insurance, poverty",
            "Description": f"US Census American Community Survey (ACS) {year}, 5-year estimates of the key economic characteristics of multiple geographic levels (county; county subdivisions; cities; ZIP codes; congressional, state assembly and state senate districts; elementary, secondary and unified educational districts; urban areas, PUMA, census tracts and block groups) for Orange County, California. The data contains 397 fields for the variable groups E01: Employment status (universe: population 16 years and over, table X23, 7 fields); E02: Work status by age of worker (universe: population 16 years and over, table X23, 36 fields); E03: Commuting to work (universe: workers 16 years and over, table X8, 8 fields); E04: Travel time to work (universe: workers 16 years and over who did not work at home, table X8, 14 fields); E05: Number of vehicles available for workers (universe: workers 16 years and over in households, table X8, 8 fields); E06: Median age by means of transportation to work (universe: median age, workers 16 years and over, table X8, 7 fields); E07: Means of transportation to work by race (universe: workers 16 years and over, table X8, 64 fields); E08: Occupation (universe: civilian employed population 16 years and over, table X24, 53 fields); E09: Industry (universe: civilian employed population 16 years and over, table X24, 43 fields); E10: Class of worker (universe: civilian employed population 16 years and over, table X24, 19 fields); E11: Household income and earnings in the past 12 months (universe: total households, table X19, 37 fields); E12: Income and earnings in dollars (universe: inflation-adjusted dollars, tables X19-X20, 31 fields); E13: Family income in dollars (universe: total families, table X19, 17 fields); E14: Health insurance coverage (universe: total families, table X19, 17 fields); E15: Ratio of income to Poverty level (universe: total population for whom Poverty level is determined, table X17,  8 fields); E16: Poverty in population in the past 12 months (universe: total population for whom Poverty level is determined, table X17, 7 fields); E17: Poverty in households in the past 12 months (universe: total households, table X17, 9 fields); E18: Percentage of families and people whose income in the past 12 months is below the poverty level (universe: families, population, table X17, 8 fields), and; X19: Poverty and income deficit (dollars) in the past 12 months for families (universe: families with income below Poverty level in the past 12 months, table X17, 4 fields). The US Census geodemographic data are based on the {year} TigerLines across multiple geographies. The spatial geographies were merged with ACS data tables. See full documentation at the OCACS project GitHub page (<a href='https://github.com/ktalexan/OCACS-Geodemographics' target='blank'>https://github.com/ktalexan/OCACS-Geodemographics</a>).",
            "Thumbnail": "https://github.com/ktalexan/OCACS-Geodemographics/blob/main/Images/OCEconomicCharacteristics.jpg?raw=true",
            "Fields": "The data contains 397 fields for the variable groups E01: Employment status (universe: population 16 years and over, table X23, 7 fields); E02: Work status by age of worker (universe: population 16 years and over, table X23, 36 fields); E03: Commuting to work (universe: workers 16 years and over, table X8, 8 fields); E04: Travel time to work (universe: workers 16 years and over who did not work at home, table X8, 14 fields); E05: Number of vehicles available for workers (universe: workers 16 years and over in households, table X8, 8 fields); E06: Median age by means of transportation to work (universe: median age, workers 16 years and over, table X8, 7 fields); E07: Means of transportation to work by race (universe: workers 16 years and over, table X8, 64 fields); E08: Occupation (universe: civilian employed population 16 years and over, table X24, 53 fields); E09: Industry (universe: civilian employed population 16 years and over, table X24, 43 fields); E10: Class of worker (universe: civilian employed population 16 years and over, table X24, 19 fields); E11: Household income and earnings in the past 12 months (universe: total households, table X19, 37 fields); E12: Income and earnings in dollars (universe: inflation-adjusted dollars, tables X19-X20, 31 fields); E13: Family income in dollars (universe: total families, table X19, 17 fields); E14: Health insurance coverage (universe: total families, table X19, 17 fields); E15: Ratio of income to Poverty level (universe: total population for whom Poverty level is determined, table X17, 8 fields); E16: Poverty in population in the past 12 months (universe: total population for whom Poverty level is determined, table X17, 7 fields); E17: Poverty in households in the past 12 months (universe: total households, table X17, 9 fields); E18: Percentage of families and people whose income in the past 12 months is below the poverty level (universe: families, population, table X17, 8 fields), and; X19: Poverty and income deficit (dollars) in the past 12 months for families (universe: families with income below Poverty level in the past 12 months, table X17, 4 fields)."
        },
        "H": {
            "Name": "Housing Characteristics",
            "Tags": f"{basicTags}, Housing Characteristics, housing occupancy, units, tenure, year built, rooms, bedrooms, vacancy status, vehicles, heating fuel, kitchen, plumbing, occupants, housing value, price asked, mortgage status, owner costs, rent value, gross rent",
            "Description": f"US Census American Community Survey (ACS) {year}, 5-year estimates of the key housing characteristics of multiple geographic levels (county; county subdivisions; cities; ZIP codes; congressional, state assembly and state senate districts; elementary, secondary and unified educational districts; urban areas, PUMA, census tracts and block groups) for Orange County, California. The data contains 406 fields for the variable groups H01: Housing occupancy (universe: total housing units, table X25, 3 fields); H02: Units in structure (universe: total housing units, table X25, 11 fields); H03: Population in occupied housing units by tenure by units in structure (universe: total population in occupied housing units, table X25, 13 fields); H04: Year structure built (universe: total housing units, table X25, 15 fields); H05: Rooms (universe: total housing units, table X25, 18 fields); H06: Bedrooms (universe: total housing units, table X25, 21 fields); H07: Housing tenure by race of householder (universe: occupied housing units, table X25, 51 fields); H08: Total population in occupied housing units by tenure (universe: total population in occupied housing units, table X25, 3 fields); H09: Vacancy status (universe: vacant housing units, table X25, 8 fields); H10: Occupied housing units by race of householder (universe: occupied housing units, table X25, 8 fields); H11: Year householder moved into unit (universe: occupied housing units, table X25, 18 fields); H12: Vehicles available (universe: occupied housing units, table X25, 18 fields); H13: Housing heating fuel (universe: occupied housing units, table X25, 10 fields); H14: Selected housing characteristics (universe: occupied housing units, table X25, 9 fields); H15: Occupants per room (universe: occupied housing units, table X25, 13 fields); H16: Housing value (universe: owner-occupied units, table X25, 32 fields); H17: Price asked for vacant for sale only, and sold not occupied housing units (universe: vacant for sale only, and sold not occupied housing units, table X25, 28 fields); H18: Mortgage status (universe: owner-occupied units, table X25, 10 fields); H19: Selected monthly owner costs, SMOC (universe: owner-occupied housing units with or without a mortgage, table X25, 45 fields); H20: Selected monthly owner costs as a percentage of household income, SMOCAPI (universe: owner-occupied housing units with or without a mortgage, table X25, 26 fields); H21: Contract rent distribution and rent asked distribution in dollars (universe: renter-occupied housing units paying cash rent and vacant, for rent, and rented not occupied housing units, table X25, 7 fields); H22: Gross rent (universe: occupied units paying rent, table X25, 28 fields), and; X23: Gross rent as percentage of household income (universe: occupied units paying rent, table X25, 11 fields). The US Census geodemographic data are based on the {year} TigerLines across multiple geographies. The spatial geographies were merged with ACS data tables. See full documentation at the OCACS project GitHub page (<a href='https://github.com/ktalexan/OCACS-Geodemographics' target='blank'>https://github.com/ktalexan/OCACS-Geodemographics</a>).",
            "Thumbnail": "https://github.com/ktalexan/OCACS-Geodemographics/blob/main/Images/OCHousingCharacteristics.jpg?raw=true",
            "Fields": "The data contains 406 fields for the variable groups H01: Housing occupancy (universe: total housing units, table X25, 3 fields); H02: Units in structure (universe: total housing units, table X25, 11 fields); H03: Population in occupied housing units by tenure by units in structure (universe: total population in occupied housing units, table X25, 13 fields); H04: Year structure built (universe: total housing units, table X25, 15 fields); H05: Rooms (universe: total housing units, table X25, 18 fields); H06: Bedrooms (universe: total housing units, table X25, 21 fields); H07: Housing tenure by race of householder (universe: occupied housing units, table X25, 51 fields); H08: Total population in occupied housing units by tenure (universe: total population in occupied housing units, table X25, 3 fields); H09: Vacancy status (universe: vacant housing units, table X25, 8 fields); H10: Occupied housing units by race of householder (universe: occupied housing units, table X25, 8 fields); H11: Year householder moved into unit (universe: occupied housing units, table X25, 18 fields); H12: Vehicles available (universe: occupied housing units, table X25, 18 fields); H13: Housing heating fuel (universe: occupied housing units, table X25, 10 fields); H14: Selected housing characteristics (universe: occupied housing units, table X25, 9 fields); H15: Occupants per room (universe: occupied housing units, table X25, 13 fields); H16: Housing value (universe: owner-occupied units, table X25, 32 fields); H17: Price asked for vacant for sale only, and sold not occupied housing units (universe: vacant for sale only, and sold not occupied housing units, table X25, 28 fields); H18: Mortgage status (universe: owner-occupied units, table X25, 10 fields); H19: Selected monthly owner costs, SMOC (universe: owner-occupied housing units with or without a mortgage, table X25, 45 fields); H20: Selected monthly owner costs as a percentage of household income, SMOCAPI (universe: owner-occupied housing units with or without a mortgage, table X25, 26 fields); H21: Contract rent distribution and rent asked distribution in dollars (universe: renter-occupied housing units paying cash rent and vacant, for rent, and rented not occupied housing units, table X25, 7 fields); H22: Gross rent (universe: occupied units paying rent, table X25, 28 fields), and; X23: Gross rent as percentage of household income (universe: occupied units paying rent, table X25, 11 fields)."
        }
    }
    
    # Geography dictionary
    gDictionary = {
        "CO": "Orange County",
        "CS": "County Subdivisions",
        "PL": "Cities",
        "ZC": "ZIP Code Tabulation Areas",
        "CD": f"Congressional Districts, {cdn}th US Congress",
        "LL": "State Assembly Legislative Districts",
        "UL": "State Senate Legislative Districts",
        "ED": "Elementary School Districts",
        "SD": "Secondary School Districts",
        "UD": "Unified School Districts",
        "UA": "Urban Areas",
        "PU": "Public Use Microdata Areas",
        "BG": "Block Groups",
        "TR": "Census Tracts"
    }
    
    print("\tFormatting metadata strings...")
    # Format the metadata from the template
    metadataList = {}
    for w in workspaces:
        print(f"\t\tProcessing workspace: {w}...")
        f = os.path.split(w)[1]
        c = f.split('.gdb')[0].split(f"OCACS{year}")[1]
        cName = cDictionary[c]["Name"]
        cTag = cDictionary[c]["Tags"]
        cDescription = cDictionary[c]["Description"]
        metadataList[c] = {}
        metadataList[c]["Path"] = w
        metadataList[c]["File"] = f.split(".gdb")[0]
        metadataList[c]["Year"] = year
        metadataList[c]["Name"] = cDictionary[c]["Name"]
        metadataList[c]["Title"] = f"OCACS {year} Geodatabase Selected {cName}"
        metadataList[c]["Tags"] = cTag
        metadataList[c]["Summary"] = f"Key {cName} of the {year} American Community Survey (ACS), 5-year estimates for multiple geography levels in Orange County, California."
        metadataList[c]["Description"] = cDescription
        metadataList[c]["Credits"] = "Original datasets from US Census TigerLine Geography (<a href='https://www.census.gov/geo/maps-data/data/tiger-line.html' target='_blank'>https://www.census.gov/geo/maps-data/data/tiger-line.html</a>), and American FactFinder (<a href='https://factfinder.census.gov/' target='_blank'>https://factfinder.census.gov/</a>) for the selected tables of the American Community Survey (ACS, {year}). Linking and merging geographic with demographic tables along with final production of the merged spatial geodatabase and online datasets are performed by Orange County Public Works, OC Survey Geospatial Services, <a href='https://www.linkedin.com/in/ktalexan/' target='_blank'>Dr. Kostas Alexandridis, GISP.</a>"
        metadataList[c]["Thumbnail"] = cDictionary[c]["Thumbnail"]
        metadataList[c]["Geographies"] = {}
        arcpy.env.workspace = w
        features = arcpy.ListFeatureClasses()
        featuresPath = [os.path.join(arcpy.env.workspace, f) for f in features]
        for g in gDictionary:
            print(f"\t\t\tProcessing geography: {gDictionary[g]}...")
            gName = gDictionary[g]
            cField = cDictionary[c]["Fields"]
            gDescription = f"US Census American Community Survey (ACS) {year}, 5-year estimates of the key {cName} of {gName} geographic level in Orange County, California. {cField}. The US Census geodemographic data are based on the {year} TigerLines across multiple geographies. The spatial geographies were merged with ACS data tables. See full documentation at the OCACS project GitHub page (<a href='https://github.com/ktalexan/OCACS-Geodemographics' target='blank'>https://github.com/ktalexan/OCACS-Geodemographics</a>)."
            metadataList[c]["Geographies"][g] = {}
            metadataList[c]["Geographies"][g]["Path"] = os.path.join(w, f"OCACS{year}{g}{c}")
            metadataList[c]["Geographies"][g]["Layer"] = f"OCACS{year}{g}{c}"
            metadataList[c]["Geographies"][g]["Year"] = year
            metadataList[c]["Geographies"][g]["Name"] = gName
            metadataList[c]["Geographies"][g]["Title"] = f"OCACS {year} {cName} for {gName}"
            metadataList[c]["Geographies"][g]["Tags"] = f"{cTag}, {gName}"
            metadataList[c]["Geographies"][g]["Summary"] = f"Key {cName} of the {year} American Community Survey (ACS), 5-year estimates for {gName} in Orange County, California"
            metadataList[c]["Geographies"][g]["Description"] = gDescription
            metadataList[c]["Geographies"][g]["Credits"] = metadataList[c]["Credits"]
            metadataList[c]["Geographies"][g]["Thumbnail"] = metadataList[c]["Thumbnail"]
    
    print("\tAssigning metadata to feature layers...")
    # Assign metadata
    for key in metadataList:
        print(f"\t\tApplying metadata for {metadataList[key]['Name']}...")
        cMetadata = md.Metadata()
        cMetadata.title = metadataList[key]["Title"]
        cMetadata.tags = metadataList[key]["Tags"]
        cMetadata.summary = metadataList[key]["Summary"]
        cMetadata.description = metadataList[key]["Description"]
        cMetadata.credits = metadataList[key]["Credits"]
        cMetadata.accessConstraints = metadataList[key]["Credits"]
        cMetadata.thumbnailUri = metadataList[key]["Thumbnail"]
        cTarget = md.Metadata(metadataList[key]["Path"])
        if not cTarget.isReadOnly:
            cTarget.copy(cMetadata)
            cTarget.save()
        elif cTarget.isReadOnly:
            print(f"{metadataList[key]['Name']} is Read Only...")
        gList = metadataList[key]["Geographies"]
        for k in gList:
            print(f"\t\t\tApplying metadata to gegoraphy {gDictionary[k]}...")
            gMetadata = md.Metadata()
            gMetadata.title = gList[k]["Title"]
            gMetadata.tags = gList[k]["Tags"]
            gMetadata.summary = gList[k]["Summary"]
            gMetadata.description = gList[k]["Description"]
            gMetadata.credits = gList[k]["Credits"]
            gMetadata.accessConstraints = gList[k]["Credits"]
            gMetadata.thumbnailUri = gList[k]["Thumbnail"]
            gTarget = md.Metadata(gList[k]["Path"])
            if not gTarget.isReadOnly:
                gTarget.copy(gMetadata)
                gTarget.save()
            elif gTarget.isReadOnly:
                print(f"{gMetadata[k]['Name']} is Read Only...")
    
    print("\tCompleted processing...\n)
    