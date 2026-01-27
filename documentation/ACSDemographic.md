<img align="left" src="OCDC.jpg" width="300" hspace=25 vspace=15>

# Orange County ACS 5-Year Geodemographics Documentation <br> **Demographic Characteristics**

*Orange County American Community Survey (ACS) Geodemographic Repository <br> Dr. Kostas Alexandridis, GISP. OC Public Works, OC Survey/Geospatial Services, 2019 - 2025.*

[<div align="right"><< Back to ReadMe.md</div>](../README.md)


<br/>

## Geodemographic Tables by group

For each of the 14 geographies described in the previous section four categories of geodemographic characteristics are linked:

1. **Demographic characteristics (7 groups, 108 fields)**, _(this document)_
2. [Social characteristics (19 groups, 500 fields)](ACSSocial.md)
3. [Economic characteristics (19 groups, 397 fields)](ACSEconomic.md)
4. [Housing characteristics (23 groups, 406 fields)](ACSHousing.md)

Each of the geographies is represented by a separate geodatabase structure. Within of each of the geographic level geodatabases, each of the four characteristics is represented by a _feature class_ respectively. In order to easily identify each of the sub-groups within each category, the name of the original census table field was adjusted by prepending to it the subgroup identification code. For example, the original field B01001e1 would become D01_B01001e1 in the new feature class for the demographic characteristics.

A more detailed description of each sub-group within each of the four feature classes representing the ACS table characteristics is provided below. The table's columns represent: the subgroup's code; its descriptive name;the universe (summative) level of the reference; the ACS cenus table in which the original fields are located; the fields/variables of the data, and; how many fields are included in the subgroup.

## 📚 D: Demographic Characteristics (7 groups, 108 variables)

The demographic characteristics selected for spatial representation can be found in ACS data tables X1-X5. They are devided in 7 subgroups: total population, sex and age, median age by sex and race, race, race alone or in combination with other races, hispanic or latino, and citizen voting age population.

Code|Name|Universe|Table|Fields|Count
---|---|---|---|---|---:
[D01](#️-d01-total-population-1-variable) | Total Population | X1 | B01001 | 1
[D02](#d02-sex-and-age-49-variables) | Sex and Age | X1 | B01001 | 49
[D03](#d03-median-age-by-sex-and-race-12-variables) | Median age by sex and race | X1 | B01002 | 12
[D04](#️-d04-race-8-variables) | Race | X1 | B02001 | 8
[D05](#️-d05-race-alone-or-in-combination-with-other-races-7-variables) | Race alone or in combination with other races | X1 | B02008 | 7
[D06](#️-d06-hispanic-or-latino-21-variables) | Hispanic or Latino | X1 | B03003 | 21
[D07](#️-d07-citizen-voting-age-population-10-variables) | Citizen voting age population | X1 | B05003 | 10


The following fields are included for each of the demographic groups:

### 🏷️ D01: Total Population (1 variable)

>🆔 B01003_001E: Total Population
<br/>
[<div align="right"><< Back to List</div>](#geodemographic-tables-by-group)

### 🏷️ D02: Sex and Age (49 variables)

>🆔 B01001_001E: Total (Sex and Age)
🆔 B01001_002E: Male
🆔 B01001_026E: Female
🆔 B01001_003E: Male: Under 5 years
🆔 B01001_004E: Male: 5 to 9 years
🆔 B01001_005E: Male: 10 to 14 years
🆔 B01001_006E: Male: 15 to 17 years
🆔 B01001_007E: Male: 18 and 19 years
🆔 B01001_008E: Male: 20 years
🆔 B01001_009E: Male: 21 years
🆔 B01001_010E: Male: 22 to 24 years
🆔 B01001_011E: Male: 25 to 29 years
🆔 B01001_012E: Male: 30 to 34 years
🆔 B01001_013E: Male: 35 to 39 years
🆔 B01001_014E: Male: 40 to 44 years
🆔 B01001_015E: Male: 45 to 49 years
🆔 B01001_016E: Male: 50 to 54 years
🆔 B01001_017E: Male: 55 to 59 years
🆔 B01001_018E: Male: 60 and 61 years
🆔 B01001_019E: Male: 62 to 64 years
🆔 B01001_020E: Male: 65 and 66 years
🆔 B01001_021E: Male: 67 to 69 years
🆔 B01001_022E: Male: 70 to 74 years
🆔 B01001_023E: Male: 75 to 79 years
🆔 B01001_024E: Male: 80 to 84 years
🆔 B01001_025E: Male: 85 years and over
🆔 B01001_027E: Female: Under 5 years
🆔 B01001_028E: Female: 5 to 9 years
🆔 B01001_029E: Female: 10 to 14 years
🆔 B01001_030E: Female: 15 to 17 years
🆔 B01001_031E: Female: 18 and 19 years
🆔 B01001_032E: Female: 20 years
🆔 B01001_033E: Female: 21 years
🆔 B01001_034E: Female: 22 to 24 years
🆔 B01001_035E: Female: 25 to 29 years
🆔 B01001_036E: Female: 30 to 34 years
🆔 B01001_037E: Female: 35 to 39 years
🆔 B01001_038E: Female: 40 to 44 years
🆔 B01001_039E: Female: 45 to 49 years
🆔 B01001_040E: Female: 50 to 54 years
🆔 B01001_041E: Female: 55 to 59 years
🆔 B01001_042E: Female: 60 and 61 years
🆔 B01001_043E: Female: 62 to 64 years
🆔 B01001_044E: Female: 65 and 66 years
🆔 B01001_045E: Female: 67 to 69 years
🆔 B01001_046E: Female: 70 to 74 years
🆔 B01001_047E: Female: 75 to 79 years
🆔 B01001_048E: Female: 80 to 84 years
🆔 B01001_049E: Female: 85 years and over
<br/>
[<div align="right"><< Back to List</div>](#geodemographic-tables-by-group)

### 🏷️ D03: Median Age by Sex and Race (12 variables)

>🆔 B01002_001E: Median age: Total
🆔 B01002_002E: Median age: Male
🆔 B01002_003E: Median age: Female
🆔 B01002A_001E: Median age: White Alone
🆔 B01002B_001E: Median age: Black or African American Alone
🆔 B01002C_001E: Median age: American Indian and Alaska Native Alone
🆔 B01002D_001E: Median age: Asian Alone
🆔 B01002E_001E: Median age: Native Hawaiian and Other Pacific Islander Alone
🆔 B01002F_001E: Median age: Some Other Race Alone
🆔 B01002G_001E: Median age: Two or More Races
🆔 B01002H_001E: Median age: White Alone, not Hispanic or Latino
🆔 B01002I_001E: Median age: Hispanic or Latino
<br>
[<div align="right"><< Back to List</div>](#geodemographic-tables-by-group)

### 🏷️ D04: Race (8 variables)

>🆔 B02001_001E: Race: Total
🆔 B02001_002E: Race: White alone
🆔 B02001_003E: Race: Black or African American alone
🆔 B02001_004E: Race: American Indian and Alaska Native alone
🆔 B02001_005E: Race: Asian alone
🆔 B02001_006E: Race: Native Hawaiian and Other Pacific Islander alone
🆔 B02001_007E: Race: Some Other Race alone
🆔 B02001_008E: Race: Two or More Races
<br>
[<div align="right"><< Back to List</div>](#geodemographic-tables-by-group)

### 🏷️ D05: Race Alone or in Combination with Other Races (7 variables)

>🆔 B02008_001E: White
🆔 B02009_001E: Black or African American
🆔 B02010_001E: American Indian and Alaska Native
🆔 B02011_001E: Asian
🆔 B02012_001E: Native Hawaiian and Other Pacific Islander
🆔 B02013_001E: Some Other Race
🆔 B02014_001E: Two or More Races
<br>
[<div align="right"><< Back to List</div>](#geodemographic-tables-by-group)

### 🏷️ D06: Hispanic or Latino (21 variables)

>🆔 B03003_001E: Total (Hispanic or Latino)
🆔 B03003_002E: Not Hispanic or Latino
🆔 B03003_003E: Hispanic or Latino
🆔 B03002_003E: Not Hispanic or Latino: White alone
🆔 B03002_004E: Not Hispanic or Latino: Black or African American alone
🆔 B03002_005E: Not Hispanic or Latino: American Indian and Alaska Native alone
🆔 B03002_006E: Not Hispanic or Latino: Asian alone
🆔 B03002_007E: Not Hispanic or Latino: Native Hawaiian and Other Pacific Islander alone
🆔 B03002_008E: Not Hispanic or Latino: Some other race alone
🆔 B03002_009E: Not Hispanic or Latino: Two or more races
🆔 B03002_010E: Not Hispanic or Latino: Two or more races: Two races including Some other race
🆔 B03002_011E: Not Hispanic or Latino: Two or more races: Two races excluding Some other race, and three or more races
🆔 B03002_013E: Hispanic or Latino: White alone
🆔 B03002_014E: Hispanic or Latino: Black or African American alone
🆔 B03002_015E: Hispanic or Latino: American Indian and Alaska Native alone
🆔 B03002_016E: Hispanic or Latino: Asian alone
🆔 B03002_017E: Hispanic or Latino: Native Hawaiian and Other Pacific Islander alone
🆔 B03002_018E: Hispanic or Latino: Some other race alone
🆔 B03002_019E: Hispanic or Latino: Two or more races
🆔 B03002_020E: Hispanic or Latino: Two or more races: Two races including Some other race
🆔 B03002_021E: Hispanic or Latino: Two or more races: Two races excluding Some other race, and three or more races
<br>
[<div align="right"><< Back to List</div>](#geodemographic-tables-by-group)

### 🏷️ D07: Citizen Voting Age Population (10 variables)

>🆔 B05003_008E: Male: 18 years and over
🆔 B05003_009E: Male: 18 years and over: Native
🆔 B05003_010E: Male: 18 years and over: Foreign-born
🆔 B05003_011E: Male: 18 years and over: Foreign-born: Naturalized US citizen
🆔 B05003_012E: Male: 18 years and over: Foreign-born: Not a US citizen
🆔 B05003_019E: Female: 18 years and over
🆔 B05003_020E: Female: 18 years and over: Native
🆔 B05003_021E: Female: 18 years and over: Foreign-born
🆔 B05003_022E: Female: 18 years and over: Foreign-born: Naturalized US citizen
🆔 B05003_023E: Female: 18 years and over: Foreign-born: Not a US citizen
<br>
[<div align="right"><< Back to List</div>](#geodemographic-tables-by-group)


[<div align="right"><< Back to ReadMe.md</div>](../README.md)
