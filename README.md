
<h1 align = "center">🗄️ Orange County Geodemographics Repository (OCGD)</h1>
<div align = "center">

<h3>🔖 Orange County Geodemographics Repository (OCGD) Codebook and Metadata</h3>

**👤 Kostas Alexandridis, PhD, GISP** | *🏷️ v. 2026.1, Januuary 2026*

![Static Badge](https://img.shields.io/badge/OCGD%2dOCGD-GitHub?style=plastic&logo=github&logoSize=auto&labe=GitHub&labelColor=navy) 
![GitHub License](https://img.shields.io/github/license/ktalexan/OCGD%2dOCGD?style=plastic&labelcolor=black) 
![Shield Badge: Language-Python](https://img.shields.io/static/v1?style=plastic&label=language&message=Python&logo=python&color=forestgreen&logoColor=blue&labelColor=black)

</div>

----
  
This repository contains basic code for processing, customizing and displaying geodatabases containing the spatially-explicit data of the US Census American Community Survey (ACS), 5-year estimates for the Orange County, California.




Below, the main project folder structure is provided and described. The project is organized into several folders, each containing specific types of files related to the analysis.

## 🗃️ Folder Structure 

- 📁 [**admin**](admin): Contains the administrative files, notes and settings for the project.
- 📁 [**analysis**](analysis): Contains the analysis files, including documents, notes and analysis presentation content.
- 📁 [**data**](data): Contains the project data (raw and processed).
  - 📂 [**raw**](data/raw): Raw and unprocessed data for the project.
  - 📂 [**processed**](data/processed): Processed and scripted data for the project.
  - 📁 [**archived**](data/archived): Archived project data.
- 📁 [**documentation**](documentation): Contains the documentation files for the project.
- 📁 [**gis**](gis): Contains the GIS and ArcGIS project files.
- 📁 [**graphics**](graphics): Contains the graphics files used in the analysis.
- 📁 [**metadata**](metadata): Contains the metadata files for the project.
- 📁 [**notebooks**](notebooks): Contains the Jupyter notebooks used in the analysis.
- 📁 [**scripts**](scripts): Contains the scripts used in the analysis including Python, and other scripts.
  - 📂 [**archived**](scripts/archived): Archived project scripts.

</br>

# 🔰 Getting Started

## Census Data

The original data are downloaded from the US Census TIGER/Line dataset with linked ACS demographic tables.
*Data source:* [US Census TIGER/Line with Selected Demographic and Economic Data](https://www.census.gov/geographies/mapping-files/time-series/geo/tiger-data.html).

## Years Included

The dataset include the following *Orange County American Community Survey (OCACS)* geodatabases for the last 9 years (2013-2021)<sup>1</sup>:

| Year | Demographic | Social | Economic | Housing | Date Added |
| :--- | :--- | :--- | :--- | :--- | ---: | 
| [2013](Documentation/ACSMetadata2013.md) | OCACS2013D | OCACS2013S | OCACS2013E | OCACS2013H | March 2019 |
| [2014](Documentation/ACSMetadata2014.md) | OCACS2014D | OCACS2014S | OCACS2014E | OCACS2014H | March 2019 |
| [2015](Documentation/ACSMetadata2015.md) | OCACS2015D | OCACS2015S | OCACS2015E | OCACS2015H | March 2019 |
| [2016](Documentation/ACSMetadata2016.md) | OCACS2016D | OCACS2016S | OCACS2016E | OCACS2016H | March 2019 |
| [2017](Documentation/ACSMetadata2017.md) | OCACS | OCACS2017S | OCACS2017E | OCACS2017H | March 2019 |
| [2018](Documentation/ACSMetadata2018.md) | OCACS2018D | OCACS2018S | OCACS2018E | OCACS2018H | April 2020 |
| [2019](Documentation/ACSMetadata2019.md) | OCACS2019D | OCACS2019S | OCACS2019E | OCACS2019H | June 2022 |
| [2020](Documentation/ACSMetadata2020.md) | OCACS2020D | OCACS2020S | OCACS2020E | OCACS2020H | May 2023 |
| [2021](Documentation/ACSMetadata2021.md) | OCACS2021D | OCACS2021S | OCACS2021E | OCACS2021H | May 2023 |
| 2022 |||||TBD 2024|

*<sup>(1)</sup> Last Update: May 2023*



## Geographies Included

The dataset include 14 separate geographies, and 25 data tables per geography (total 14 x 25 = 350 geographic feature datasets) in each year's geodatabases. Specifically, the included geographies are:

| Category | Level | Abbrev | Description |
|:---|:---|:---:|:---|
| Administrative | County | CO | County of Orange |
|| County Subdivisions | CS | Orange County Subdivisions |
|| Cities/Places | PL | Orange County Cities |
|| ZIP Codes | ZC | ZIP Code Tabulation Areas for Orange County |
| Political | Congressional Districts | CD | Congressional Districts, 113th-116th US Congress for Orange County |
|| State Assembly | LL | State Assembly Legislative Districts (Lower) for Orange County |
|| State Senate | UL | State Senate Legislative Districts (Upper) for Orange County |
| Education | Elementary | ED | Elementary School Districts for Orange County |
|| Secondary | SD | Secondary School Districts for Orange County |
|| Unified | UD | Unified School Districts for Orange County |
| Census | Urban Areas | UA | Urban Areas for Orange and Los Angeles Counties |
|| Public Use Microdata Areas | PU | Census Public Use Microdata Areas (PUMA) for Orange County |
|| Block Groups | BG | Census Block Groups for Orange County |
|| Census Tracts | TR | Census Tracts for Orange County |


## Geodatabase Feature Class Metadata Description

Tabulation of level abbreviations by geography and ACS category characteristics. The 3-letter abbreviation consists of:

* First and second letter: *Geography level* (14-levels)
* Third letter: *ACS category characteristics* (4-levels)

*Total abbreviations: 14 georaphies x 4 characteristics = 56 feature class levels (four in each geodatabase).*

| Geography | Demographic (D) | Social (S) | Economic (E) | Housing (H) |
| :--- | :---: | :---: | :---: | :---: |
| 1. County (CO) | COD | COS | COE | COH |
| 2. County Subdivision (CS) | CSD | CSS | CSE | CSH |
| 3. Cities/Places (PL) | PLD | PLS | PLE | PLH |
| 4. ZIP Code Tabulation Areas (ZC) | ZCD | ZCS | ZCE | ZCH |
| 5. Congressional Districts (CD) | CDD | CDS | CDE | CDH |
| 6. State Assembly Legislative Districts (LL) | LLD | LLS | LLE | LLH |
| 7. State Senate Legislative Districts (UL) | ULD | ULS | ULE | ULH |
| 8. Elementary School Districts (ED) | EDD | EDS | EDE | EDH |
| 9. Secondary School Districts (SD) | SDD | SDS | SDE | SDH |
| 10. Unified School Districts (UD) | UDD | UDS | UDE | UDH |
| 11. Urban Areas (UA) | UAD | UAS | UAE | UAH |
| 12. Public Use Microdata Areas (PU) | PUD | PUS | PUE | PUH |
| 13. Block Groups (BG) | BGD | BGS | BGE | BGH |
| 14. Census Tracts (TR) | TRD | TRS | TRE | TRH |

For complete geodatabase metadata information and description, please <a href="Documentation/GeodatabaseMetadata.md" target="_blank">follow this link to the full metadata document.</a>


## Geodemographic Tables by group

For each of the 14 geographies described in the previous section four categories of geodemographic characteristics are linked:

1. [Demographic Characteristics (6 groups, 105 fields)](Documentation/ACSDemographic.md)
2. [Social Characteristics (19 groups, 500 fields)](Documentation/ACSSocial.md)
3. [Economic Characteristics (19 groups, 397 fields)](Documentation/ACSEconomic.md)
4. [Housing Characteristics (19 groups, 406 fields)](Documentation/ACSHousing.md)

Each of the geographies is represented by a separate geodatabase structure. Within of each of the geographic level geodatabases, each of the four characteristics is represented by a *feature class* respectively. In order to easily identify each of the sub-groups within each category, the name of the original census table field was adjusted by prepending to it the subgroup identification code. For example, the original field B01001e1 would become D01_B01001e1 in the new feature class for the demographic characteristics.

A more detailed description of each sub-group within each of the four feature classes representing the ACS table characteristics is provided in each of the sections above (opens the documentation markdown file). The table's columns represent: the subgroup's code; its descriptive name;the universe (summative) level of the reference; the ACS cenus table in which the original fields are located; the fields/variables of the data, and; how many fields are included in the subgroup.


#### Summary of Data Table Levels by Geodemographic Characteristic

The tabulation summaries below provide an overview of the data tables by each of the four geodemographic characteristics (Demographic, Social, Economic and Housing). For more details on the specific table lists, see the detailed page links above by geodemographic characteristic.

| Demographic (D) | Social (S) | Economic (E) | Housing (H) |
| :--- | :--- | :--- | :--- |
| D01: Sex and Age | S01: Households Type | E01: Employment Status | H01: Housing Occupancy |
| D02: Median Age by Sex and Race | S02: Relationships | E02: Work Status | H02: Units in Structure |
| D03: Race | S03: Marital Status | E03: Commuting | H03: Population by Housing Occupancy |
| D04: Race Combinations | S04: Fertility | E04: Travel Time to Work | H04: Year Structure Built |
| D05: Hispanic or Latino Race | S05: Grandparents | E05: Vehicles Available to Workers | H05: Rooms |
| D06: Citizen Voting Age | S06: School Enrollment | E06: Median Age by Transportation Means | H06: Bedrooms |
|| S07: Education Attainment | E07: Transportation Means by Race | H07: Housing Tenure by Race and Age |
|| S08: Veteran Status | E08: Occupation | H08: Population by Tenure |
|| S09: Disability Status by Sex and Race | E09: Industry | H09: Vacancy Status |
|| S10: Disability by Age and Health Insurance | E10: Class of Worker | H10: Householder Race |
|| S11: Residence Status | E11: Household Income and Earnings | H11: Year Moved into Unit |
|| S12: Place of Birth | E12: Earnings Income in Dollars | H12: Vehicles Available |
|| S13: Citizenship Status | E13: Family Income | H13: House Heating and Fuel |
|| S14: Year of Entry | E14: Health Insurance | H14: Selected Characteristics |
|| S15: Birth Region | E15: Income to Poverty Ratio | H15: Occupants per Room |
|| S16: Language Spoken in Households | E16: Population Below Poverty Level | H16: Housing Value |
|| S17: Language Spoken at Home | E17: Households Below Poverty Level | H17: Housing Price Asked |
|| S18: Ancestry | E18: Families Below Povertry Level | H18: Mortgage Status |
|| S19: Computers and Internet Use | E19: Income Deficit Below Poverty Level | H19: Selected Monthly Owner Costs |
|||| H20: Selected Monthly Owner costs as a Percent of Household Income|
|||| H21: Rent Contract Asked |
|||| H22: Gross Rent |
|||| H23: Gross Rent as Percentage of Income |

