<img align="left" src="OCHC.jpg" width="300" hspace=25 vspace=15>

# OCACS Geodemographics Documentation <br> Housing Characteristics

*Orange County American Community Survey (ACS) Geodemographic Repository <br> Dr. Kostas Alexandridis, GISP. OC Public Works, OC Survey/Geospatial Services, 2019 - 2022.*

[<div align="right"><< Back to ReadMe.md</div>](../README.md)

## Geodemographic Tables by group

For each of the 14 geographies described in the previous section four categories of geodemographic characteristics are linked:

1. [Demographic characteristics (6 groups, 105 fields)](ACSDemographic.md)
2. [Social characteristics (19 groups, 500 fields)](ACSSocial.md)
3. [Economic characteristics (19 groups, 397 fields)](ACSEconomic.md)
4. **Housing characteristics (23 groups, 406 fields)** _(this document)_

Each of the geographies is represented by a separate geodatabase structure. Within of each of the geographic level geodatabases, each of the four characteristics is represented by a _feature class_ respectively. In order to easily identify each of the sub-groups within each category, the name of the original census table field was adjusted by prepending to it the subgroup identification code. For example, the original field B01001e1 would become D01_B01001e1 in the new feature class for the demographic characteristics.

A more detailed description of each sub-group within each of the four feature classes representing the ACS table characteristics is provided below. The table's columns represent: the subgroup's code; its descriptive name;the universe (summative) level of the reference; the ACS cenus table in which the original fields are located; the fields/variables of the data, and; how many fields are included in the subgroup.

#### H: Housing Characteristics (23 groups, 406 fields)

The housing characteristics selected for spatial representation can by found in ACS data table X25. They are divided into 23 subgroups: housing occupancy, units in struture, housing tenure for population, year built, rooms, bedrooms, tenure by race, tenure by occupancy, vacancy status, occupancy by householder race, other selected housing characteristics, occupants per room, housing value, price asked for housing unit, mortgage status, monthly owner costs (in dollars and as % of income), contract rent and rent asked, gross rent costs (in dollaras and as % of income) estimates.

Code|Name|Universe|Table|Fields|Count
---|---|---|---|---|---:
[H01](#h01-housing-occupancy-3-variables)|Housing occupancy|total housing units|X25|B25002|3
[H02](#h02-units-in-structure-11-variables)|Units in structure|total housing units|X25|B25024|11
[H03](#h03-population-in-occupied-housing-units-by-tenure-by-units-in-structure-13-variables)|Population in occupied housing units by tenure by units in structure|total population in occupied housing units|X25|B25033|13
[H04](#h04-year-structure-built-15-variables)|Year structure built|total housing units|X25|B25034-35, B25037|15
[H05](#h05-rooms-18-variables)|Rooms|total housing units|X25|B25017-19, B25021-22|18
[H06](#h06-bedrooms-21-variables)|Bedrooms|total housing units|X25|B25041-42|21
[H07](#h07-housing-tenure-by-race-of-householder-51-variables)|Housing tenure by race of householder|occupied housing units|X25|B25003, B25007, B25010|51
[H08](#h08-total-population-in-occupied-housing-units-by-tenure-3-variables)|Total population in occupied housing units by tenure|total population in occupied housing units|X25|B25008|3
[H09](#h09-vacancy-status-8-variables)|Vacancy status|vacant housing units|X25|B25004|8
[H10](#h10-occupied-housing-units-by-race-of-householder-8-variables)|Occupied housing units by race of householder|occupied housing units|X25|B25006|8
[H11](#h11-year-householder-moved-into-unit-18-variables)|Year householder moved into unit|occupied housing units|X25|B25038|18
[H12](#h12-vehicles-available-18-variables)|Vehicles available|occupied housing units|X25|B25044, B25046|18
[H13](#h13-house-heating-fuel-10-variables)|House heating fuel|occupied housing units|X25|B25040|10
[H14](#h14-selected-characteristics-9-variables)|Selected characteristics|occupied housing units|X25|B25016, B25043, B25053|9
[H15](#h15-occupants-per-room-13-variables)|Occupants per room|occupied housing units|X25|B25014|13
[H16](#h16-housing-value-32-variables)|Housing value|owner-occupied units|X25|B25075-79, B25083|32
[H17](#h17-price-ssked-for-vacant-for-sale-only-and-sold-not-occupied-housing-units-28-variables)|Price asked for vacant for-sale only, and sold, not occupied housing units|vacant for slae only, and sold, not occupied housing units|X25|B25085-86|28
[H18](#h18-mortgage-status-10-variables)|Mortgage status|owner-occupied units|X25|B25081-82|10
[H19](#h19-selected-monthly-owner-costs-smoc-45-variables)|Selected monthly owner costs (SMOC)|owner-occupied housing units with or without a mortgage|X25|B25087-89|45
[H20](#h20-selected-monthly-owner-costs-as-a-percentage-of-household-income-smocapi-26-variables)| Selected monthly owner costs as a percentage of household income (SMOCAPI)|owner-occupied housing units with or without a mortgage|X25|B25091-92|26
[H21](#h21-contract-rent-distribution-and-rent-asked-distribution-in-dollars-7-variables)|Contract rent distribution and rent asked distribution in dollars|renter-occupied housing units paying cash rent and vacant, for rent, and rented, not occupied housing units|X25|B25056-62|7
[H22](#h22-gross-rent-28-variables)|Gross rent|occupied units paying rent|X25|B25063-65|28
[H23](#h23-gross-rent-as-percentage-of-household-income-11-variables)|Gross rent as percentage of household income|occupied units paying rent|X25|B25070|11

The following fields are included for each of the housing groups:

#### H01: Housing occupancy (3 variables)

>B25002e1 (Total housing units); B25002e2 (Occupied housing units); B25002e3 (Vacant housing units).
[<div align="right"><< Back to List</div>](#h-housing-characteristics-23-groups-406-fields)

#### H02: Units in Structure (11 variables)

> B25024e1 (Total housing units); B25024e2 (1-unit, detatched); B25024e3 (1-unit, attached); B25024e4 (2-units); B25024e5 (3 or 4 units); B25024e6 (5 to 9 units); B25024e7 (10 to 19 units); B25024e8 (20 to 49 units); B25024e9 (50 or more units); B25024e10 (Mobile home); B25024e11 (Boat, RV, van, etc). 
[<div align="right"><< Back to List</div>](#h-housing-characteristics-23-groups-406-fields)

#### H03: Population in Occupied Housing Units by Tenure by Units in Structure (13 variables)

> B25033e1 (Total population in occupied housing units); B25033e2 (Population in owner-occupied housing units); B25033e3 (Population in owner-occupied 1 detached or attached housing units); B25033e4 (Population in owner-occupied 2 to 4 housing units); B25033e5 (Population in owner-occupied 5 or more housing units); B25033e6 (Population in owner-occupied mobile home); B25033e7 (Population in owner-occupied boat, RV, van, etc); B25033e8 (Population in renter-occupied housing units); B25033e9 (Population in renter-occupied 1 detached or attached housing units); B25033e10 (Population in renter-occupied 2 to 4 housing units); B25033e11 (Population in renter-occupied 5 or more housing units); B25033e12 (Population in renter-occupied mobile home); B25033e13 (Population in renter-occupied boat, RV, van, etc).
[<div align="right"><< Back to List</div>](#h-housing-characteristics-23-groups-406-fields)

#### H04: Year Structure Built (15 variables)

> B25034e1 (Total housing units); B25034e2 (Built 2014 or later); B25034e3 (Built 2010 to 2013); B25034e4 (Built 2000 to 2009); B25034e5 (Built 1990 to 1999); B25034e6 (Built 1980 to 1989); B25034e7 (Built 1970 to 1979); B25034e8 (Built 1960 to 1969); B25034e9 (Built 1950 to 1959); B25034e10 (Built 1940 to 1949); B25034e11 (Built 1939 or earlier); B25035e1 (Median year structure built); B25037e1 (Median year structure built, occupied housing units); B25037e2 (Median year structure built, owner-occupied housing units); B25037e3 (Median year structure built, renter-occupied housing units).
[<div align="right"><< Back to List</div>](#h-housing-characteristics-23-groups-406-fields)

#### H05: Rooms (18 variables)

> B25017e1 (Total housing units); B25017e2 (1 room); B25017e3 (2 rooms); B25017e4 (3 rooms); B25017e5 (4 rooms); B25017e6 (5 rooms); B25017e7 (6 rooms); B25017e8 (7 rooms); B25017e9 (8 rooms); B25017e10 (9 rooms or more); B25018e1 (Median number of rooms); B25019e1 (Aggregate number of rooms); B25021e1 (Median number of rooms in occupied housing units); B25021e2 (Median number of rooms in owner-occupied housing units); B25021e3 (Median number of rooms in renter-occupied housing units); B25022e1 (Aggregate number of rooms in occupied housing units); B25022e2 (Aggregate number of rooms in owner-occupied housing units); B25022e3 (Aggregate number of rooms in renter-occupied housing units).
[<div align="right"><< Back to List</div>](#h-housing-characteristics-23-groups-406-fields)

#### H06: Bedrooms (21 variables)

> B25041e1 (Total housing units); B25041e2 (No bedroom); B25041e3 (1 bedroom); B25041e4 (2 bedrooms); B25041e5 (3 bedrooms); B25041e6 (4 bedrooms); B25041e7 (5 or more bedrooms); B25042e (Owner-occupied housing units); B25042e3 (Owner-occupied, no bedroom); B25042e4 (Onwer-occupied, 1 bedroom); B25042e5 (Owner-occupied, 2 bedrooms); B25042e6 (Owner-occupied, 3 bedrooms); B25042e7 (Owner-occupied, 4 bedrooms); B25042e8 (Owner-occupied, 5 or more bedrooms); B25042e9 (Renter-occupied housing units); B25042e10 (Renter-occupied, no bedroom); B25042e11 (Onwer-occupied, 1 bedroom); B25042e12 (Renter-occupied, 2 bedrooms); B25042e13 (Renter-occupied, 3 bedrooms); B25042e14 (Renter-occupied, 4 bedrooms); B25042e15 (Renter-occupied, 5 or more bedrooms).
[<div align="right"><< Back to List</div>](#h-housing-characteristics-23-groups-406-fields)

#### H07: Housing Tenure by Race of Householder (51 variables)

> B25003e1 (Occupied houging units); B25003e2 (Owner-occupied); B25003e3 (Renter-occuped); B25003Ae1 (Occupied housing units with a householder who is White alone); B25003Ae2 (Owner-occupied housing units with a householder who is White alone); B25003Ae3 (Renter-occupied housing units with a householder who is White alone); B25003Be1 (Occupied housing units with a householder who is Black or African American alone); B25003Be2 (Owner-occupied housing units with a householder who is Black or African American alone); B25003Be3 (Renter-occupied housing units with a householder who is Black or African American alone); B25003Ce1 (Occupied housing units with a householder who is American Indian and Alaska Native alone); B25003Ce2 (Owner-occupied housing units with a householder who is American Indian and Alaska Native alone); B25003Ce3 (Renter-occupied housing units with a householder who is American Indian and Alaska Native alone); B25003De1 (Occupied housing units with a householder who is Asian alone); B25003De2 (Owner-occupied housing units with a householder who is Asian alone); B25003De3 (Renter-occupied housing units with a householder who is Asian alone); B25003Ee1 (Occupied housing units with a householder who is Native Hawaiian and Other Pacific Islander alone); B25003Ee2 (Owner-occupied housing units with a householder who is Native Hawaiian and Other Pacific Islander alone); B25003Ee3 (Renter-occupied housing units with a householder who is Native Hawaiian and Other Pacific Islander alone); B25003Fe1 (Occupied housing units with a householder who is other race alone); B25003Fe2 (Owner-occupied housing units with a householder who is other race alone); B25003Fe3 (Renter-occupied housing units with a householder who is other race alone); B25003Ge1 (Occupied housing units with a householder who is two or more races); B25003Ge2 (Owner-occupied housing units with a householder who is two or more races); B25003Ge3 (Renter-occupied housing units with a householder who is two or more races); B25003He1 (Occupied housing units with a householder who is White alone, not Hispanic or Latino); B25003He2 (Owner-occupied housing units with a householder who is White alone, not Hispanic or Latino); B25003He3 (Renter-occupied housing units with a householder who is White alone, not Hispanic or Latino); B25003Ie1 (Occupied housing units with a householder who is Hispanic or Latino); B25003Ie2 (Owner-occupied housing units with a householder who is Hispanic or Latino); B25003Ie3 (Renter-occupied housing units with a householder who is Hispanic or Latino); B25007e3 (Owner-occupied, householder 15 to 24 years); B25007e4 (Owner-occupied, householder 25 to 34 years); B25007e5 (Owner-occupied, householder 35 to 44 years); B25007e6 (Owner-occupied, householder 45 to 54 years); B25007e7 (Owner-occupied, householder 55 to 59 years); B25007e8 (Owner-occupied, householder 60 to 64 years); B25007e9 (Owner-occupied, householder 65 to 74 years); B25007e10 (Owner-occupied, householder 75 to 84 years); B25007e11 (Owner-occupied, householder 85 years and over); B25007e13 (Renter-occupied, householder 15 to 24 years); B25007e14 (Renter-occupied, householder 25 to 34 years); B25007e15 (Renter-occupied, householder 35 to 44 years); B25007e16 (Renter-occupied, householder 45 to 54 years); B25007e17 (Renter-occupied, householder 55 to 59 years); B25007e18 (Renter-occupied, householder 60 to 64 years); B25007e19 (Renter-occupied, householder 65 to 74 years); B25007e20 (Renter-occupied, householder 75 to 84 years); B25007e21 (Renter-occupied, householder 85 years and over); B25010e1 (Average household size of occupied housing units); B25010e2 (Average household size of owner-occupied housing units); B25010e3 (Average household size of renter-occupied houding units).
[<div align="right"><< Back to List</div>](#h-housing-characteristics-23-groups-406-fields)

#### H08: Total Population in Occupied Housing Units by Tenure (3 variables)

> B25008e1 (Total population in occupied housing units); B25008e2 (Population in owner-occupied housing units); B25008e3 (Population in renter-occupied housing units).
[<div align="right"><< Back to List</div>](#h-housing-characteristics-23-groups-406-fields)

#### H09: Vacancy Status (8 variables)

> B25004e1 (Total vacant housing units); B25004e2 (For rent); B25004e3 (Rented, not occupied); B25004e4 (For sale only); B25004e5 (Sold, not occupied); B25004e6 (For seasonal, recreational, or occassional use); B25004e7 (For migrant workers); B25004e8 (Other vacant units).
[<div align="right"><< Back to List</div>](#h-housing-characteristics-23-groups-406-fields)

#### H10: Occupied Housing Units by Race of Householder (8 variables)

> B25006e1 (Occupied housing units); B25006e2 (Units with White alone householder); B25006e3 (Units with Black or Afican American alone householder); B25006e4 (Units with American Indian and Alaska Native alone householder); B25006e5 (Units with Asian alone householder); B25006e6 (Units with Native Hawaiian and Other Pacific Islander alone householder); B25006e7 (Units with some other race alone householder); B25006e8 (Units with two or more races householder).
[<div align="right"><< Back to List</div>](#h-housing-characteristics-23-groups-406-fields)

#### H11: Year Householder Moved Into Unit (18 variables)

> B25038e1 (Occupied housing units); B25038e2 (Owner-occupied housing units); B25038e3 (Owner-occupied, moved in 2015 or later); B25038e4 (Owner-occupied, moved in 2010 to 2014); B25038e5 (Owner-occupied, moved in 2000 to 2009); B25038e6 (Owner-occupied, moved in 1990 to 1999); B25038e7 (Owner-occupied, moved in 1980 to 1989); B25038e8 (Owner-occupied, moved in 1979 or earlier); B25038e9 (Renter-occupied housing units); B25038e10 (Renter-occupied, moved in 2015 or later); B25038e11 (Renter-occupied, moved in 2010 to 2014); B25038e12 (Renter-occupied, moved in 2000 to 2009); B25038e13 (Renter-occupied, moved in 1990 to 1999); B25038e14 (Renter-occupied, moved in 1980 to 1989); B25038e15 (Renter-occupied, moved in 1979 or earlier); B25039e1 (Median year householder moved into occupied housing unit); B25039e2 (Median year householder moved into owner-occupied unit); B25039e3 (Median year householder moved into renter-occupied unit).
[<div align="right"><< Back to List</div>](#h-housing-characteristics-23-groups-406-fields)

#### H12: Vehicles Available (18 variables)

> B25044e1 (Occupied housing units); B25044e2 (Owner-occupied housing units); B25044e3 (Owner-occupied, no vehicles available); B25044e4 (Owner-occupied, 1 vehicle available); B25044e5 (Owner-occupied, 2 vehicles available); B25044e6 (Owner-occupied, 3 vehicles available); B25044e7 (Owner-occupied, 4 vehicles available); B25044e8 (Owner-occupied, 5 or more vehicles available); B25044e9 (Renter-occupied housing units); B25044e10 (Renter-occupied, no vehicles available); B25044e11 (Renter-occupied, 1 vehicle available); B25044e12 (Renter-occupied, 2 vehicles available); B25044e13 (Renter-occupied, 3 vehicles available); B25044e14 (Renter-occupied, 4 vehicles available); B25044e15 (Renter-occupied, 5 or more vehicles available); B25046e1 (Aggregate number of vehicles available in occupied housing units); B25046e2 (Aggregate number of vehicles available in owner-occupied housing units); B25046e3 (Aggregate number of vehicles available in renter-occupied housing units).
[<div align="right"><< Back to List</div>](#h-housing-characteristics-23-groups-406-fields)

#### H13: House Heating Fuel (10 variables)

> B25040e1 (Occupied housing units); B25040e2 (Utility gas); B25040e3 (Bottled, tank, or LP gas); B25040e4 (Electricity); B25040e5 (Fuel oil, kerosene, etc); B25040e6 (Coal or coke); B25040e7 (Wood); B25040e8 (Solar energy); B25040e9 (Other fuel); B25040e10 (No fuel used).
[<div align="right"><< Back to List</div>](#h-housing-characteristics-23-groups-406-fields)

#### H14: Selected Characteristics (9 variables)

> B25016e1 (Occupied housing units); B25016e2 (Onwer-occupied housing units); B25016e11 (Renter-occupied housing units); B25016e7 (Onwer-occupied, lacking complete plumbing facilities); B25016e16 (Renter-occupied, lacking complete plumbing facilities); B25043e7 (Owner-occupied, no telephone service available); B25043e16 (Renter-occupied, no telephone service available); B25053e4 (Owner-occupied, lacking complete kitchen facilities); B25053e7 (Renter-occupied, lacking complete kitchen facilities).
[<div align="right"><< Back to List</div>](#h-housing-characteristics-23-groups-406-fields)

#### H15: Occupants per Room (13 variables)

> B25014e1 (Occupied housing units); B25014e2 (Owner-occupied housing units); B25014e3 (Owner-occupied housing units, 0.5 or less occupants per room); B25014e4 (Owner-occupied housing units, 0.51 to 1.00 occupants per room); B25014e5 (Owner-occupied housing units, 1.01 to 1.50 occupants per room); B25014e6 (Owner-occupied housing units, 1.51 to 2.00 occupants per room); B25014e7 (Owner-occupied housing units, 2.01 or more occupants per room); B25014e8 (Renter-occupied housing units); B25014e9 (Renter-occupied housing units, 0.5 or less occupants per room); B25014e10 (Renter-occupied housing units, 0.51 to 1.00 occupants per room); B25014e11 (Renter-occupied housing units, 1.01 to 1.50 occupants per room); B25014e12 (Renter-occupied housing units, 1.51 to 2.00 occupants per room); B25014e13 (Renter-occupied housing units, 2.01 or more occupants per room).
[<div align="right"><< Back to List</div>](#h-housing-characteristics-23-groups-406-fields)

#### H16: Housing Value (32 variables)

> B25075e1 (Owner-occupied units); B25075e2 (Less than $10,000); B25075e3 ($10,000 to $14,999); B25075e4 ($15,000 to $19,999); B25075e5 ($20,000 to $24,999); B25075e6 ($25,000 to $29,999); B25075e7 ($30,000 to $34,999); B25075e8 ($35,000 to $39,999); B25075e9 ($40,000 to $49,999); B25075e10 ($50,000 to $59,999); B25075e11 ($60,000 to $69,999); B25075e12 ($70,000 to $79,999); B25075e13 ($80,000 to $89,999); B25075e14 ($90,000 to $99,999); B25075e15 ($100,000 to $124,999); B25075e16 ($125,000 to $149,999); B25075e17 ($150,000 to $174,999); B25075e18 ($175,000 to $199,999); B25075e19 ($200,000 to $249,999); B25075e20 ($250,000 to $299,999); B25075e21 ($300,000 to $399,999); B25075e22 ($400,000 to $499,999); B25075e23 ($500,000 to $749,999); B25075e24 ($750,000 to $999,999); B25075e25 ($1,000,000 to $1,499,999); B25075e26 ($1,500,000 to $1,999,999); B25075e27 ($2,000,000 or more); B25076e1 (Lower value quartile (dollars)); B25077e1 (Median value (dollars)); B25078e1 (Upper value quartile (dollars)); B25079e1 (Aggregate value (dollars)); B25083e1 (Median value (dollars) for mobile homes).
[<div align="right"><< Back to List</div>](#h-housing-characteristics-23-groups-406-fields)

#### H17: Price Ssked for Vacant For-Sale Only, and Sold, not Occupied Housing Units (28 variables)

> B25085e1 (Total vacant for-sale only and sold, not occupied housing units); B25085e2 (Less than $10,000); B25085e3 ($10,000 to $14,999); B25085e4 ($15,000 to $19,999); B25085e5 ($20,000 to $24,999); B25085e6 ($25,000 to $29,999); B25085e7 ($30,000 to $34,999); B25085e8 ($35,000 to $39,999); B25085e9 ($40,000 to $49,999); B25085e10 ($50,000 to $59,999); B25085e11 ($60,000 to $69,999); B25085e12 ($70,000 to $79,999); B25085e13 ($80,000 to $89,999); B25085e14 ($90,000 to $99,999); B25085e15 ($100,000 to $124,999); B25085e16 ($125,000 to $149,999); B25085e17 ($150,000 to $174,999); B25085e18 ($175,000 to $199,999); B25085e19 ($200,000 to $249,999); B25085e20 ($250,000 to $299,999); B25085e21 ($300,000 to $399,999); B25085e22 ($400,000 to $499,999); B25085e23 ($500,000 to $749,999); B25085e24 ($750,000 to $999,999); B25085e25 ($1,000,000 to $1,499,999); B25085e26 ($1,500,000 to $1,999,999); B25085e27 ($2,000,000 or more); B25086e1 (Aggregate price asked (dollars)).
[<div align="right"><< Back to List</div>](#h-housing-characteristics-23-groups-406-fields)

#### H18: Mortgage Status (10 variables)

> B25081e1 (Owner-occupied units); B25081e2 (Housing units with a mortgage); B25081e7 (Housing units with a mortgage only); B25081e4 (Housing units with a mortgage and a second mortgage); B25081e5 (Housing units with a mortgage and a home equity loan); B25081e6 (Housing units with a mortgage and both a second mortgage and a home equity loan); B25081e8 (Housing units without a mortgage); B25082e1 (Aggregate value (dollars) of owner-occupied units); B25082e2 (Aggregate value (dollars) of housing units with a mortgage); B25082e3 (Aggregate value (dollars) of housing units without a mortgage).
[<div align="right"><< Back to List</div>](#h-housing-characteristics-23-groups-406-fields)

#### H19: Selected Monthly Owner Costs (SMOC) (45 variables)

> B25087e1 (Total owner-occupied housing units); B25087e2 (Housing units with a mortgage); B25087e3 (With mortgage, less than $200); B25087e4 (With mortgage, $200 to $299); B25087e5 (With mortgage, $300 to $399); B25087e6 (With mortgage, $400 to $499); B25087e7 (With mortgage, $500 to $599); B25087e8 (With mortgage, $600 to $699); B25087e9 (With mortgage, $700 to $799); B25087e10 (With mortgage, $800 to $899); B25087e11 (With mortgage, $900 to $999); B25087e12 (With mortgage, $1,000 to $1,249); B25087e13 (With mortgage, $1,250 to $1,499); B25087e14 (With mortgage, $1,500 to $1,999); B25087e15 (With mortgage, $2,000 to $2,499); B25087e16 (With mortgage, $2,500 to $2,999); B25087e17 (With mortgage, $3,000 to $3,499); B25087e18 (With mortgage, $3,500 to $3,999); B25087e19 (With mortgage, $4,000 or more); B25087e20 (Housing units without a mortgage); B25087e21 (Without mortgage, less than $100); B25087e22 (Without mortgage, $100 to $149); B25087e23 (Without mortgage, $150 to $199); B25087e24 (Without mortgage, $200 to $249); B25087e25 (Without mortgage, $250 to $299); B25087e26 (Without mortgage, $300 to $349); B25087e27 (Without mortgage, $350 to $399); B25087e28 (Without mortgage, $400 to $499); B25087e29 (Without mortgage, $500 to $599); B25087e30 (Without mortgage, $600 to $699); B25087e31 (Without mortgage, $700 to $799); B25087e32 (Without mortgage, $800 to $899); B25087e33 (Without mortgage, $900 to $999); B25087e34 (Without mortgage, $1,000 to $1,099); B25087e35 (Without mortgage, $1,100 to $1,199); B25087e36 (Without mortgage, $1,200 to $1,299); B25087e37 (Without mortgage, $1,300 to $1,399); B25087e38 (Without mortgage, $1,400 to $1,499); B25087e39 (Without morrgage, $1,500 or more); B25088e1 (Median selected monthly owner costs (dollars) for all owner-occupied housing units); B25088e2 (Median selected monthly owner costs (dollars) for units with a mortgage); B25088e3 (Median selected monthly owner costs (dollars) for units without a mortgage); B25089e1 (Aggregate selected monthly owner costs (dollars) for all owner-occupied housing units); B25089e2 (Aggregate selected monthly owner costs (dollars) for units with a mortgage); B25089e3 (Aggregate selected monthly owner costs (dollars) for units without a mortgage).
[<div align="right"><< Back to List</div>](#h-housing-characteristics-23-groups-406-fields)

#### H20: Selected Monthly Owner Costs as a Percentage of Household Income (SMOCAPI) (26 variables)

> B25091e1 (Owner-occupied housing units); B25091e2 (Housing units with a mortgage); B25091e3 (With mortgage, less than 10.0 percent); B25091e4 (With mortgage, 10.0 to 14.9 percent); B25091e5 (With mortgage, 15.0 to 19.9 percent); B25091e6 (With mortgage, 20.0 to 24.9 percent); B25091e7 (With mortgage, 25.0 to 29.9 percent); B25091e8 (With mortgage, 30.0 to 34.9 percent); B25091e9 (With mortgage, 35.0 to 39.9 percent); B25091e10 (With mortgage, 40.0 to 49.9 percent); B25091e11 (With mortgage, 50.0 percent or more); B25091e12 (With mortgage, not computed); B25091e13 (Housing units without a mortgage); B25091e14 (Without mortgage, less than 10.0 percent); B25091e15 (Without mortgage, 10.0 to 14.9 percent); B25091e16 (Without mortgage, 15.0 to 19.9 percent); B25091e17 (Without mortgage, 20.0 to 24.9 percent); B25091e18 (Without mortgage, 25.0 to 29.9 percent); B25091e19 (Without mortgage, 30.0 to 34.9 percent); B25091e20 (Without mortgage, 35.0 to 39.9 percent); B25091e21 (Without mortgage, 40.0 to 49.9 percent); B25091e22 (Without mortgage, 50.0 percent or more); B25091e23 (Without mortgage, not computed); B25092e1 (Median selected monthly owner costs (dollars) as percentage of household income for all units); B25092e2 (Median selected monthly owner costs (dollars) as percentage of household income for units with a mortgage); B25092e3 (Median selected monthly owner costs (dollars) as percentage of household income for units without a mortgage).
[<div align="right"><< Back to List</div>](#h-housing-characteristics-23-groups-406-fields)

#### H21: Contract Rent Distribution and Rent Asked Distribution in Dollars (7 variables)

> B25056e2 (Renter-occupied housing units paying cash rent); B25057e1 (Lower contract rent quartile); B25058e1 (Median contract rent); B25059e1 (Upper contract rent quartile); B25060e1 (Aggregate contract rent); B25061e1 (Vacant for rent and rented, not occupied housing units); B25062e1 (Aggregate rent asked).
[<div align="right"><< Back to List</div>](#h-housing-characteristics-23-groups-406-fields)

#### H22: Gross Rent (28 variables)

> B25063e2 (Occupied units paying rent); B25063e3 (Less than $500); B25063e4 ($100 to $149); B25063e5 ($150 to $199); B25063e6 ($200 to $249); B25063e7 ($250 to $299); B25063e8 ($300 to $349); B25063e9 ($350 to $399); B25063e10 ($400 to $449); B25063e11 ($450 to $499); B25063e12 ($500 to $549); B25063e13 ($550 to $599); B25063e14 ($600 to #649); B25063e15 ($650 to $699); B25063e16 ($700 to $749); B25063e17 ($750 to $799); B25063e18 ($800 to $899); B25063e19 ($900 to $999); B25063e20 ($1,000 to $1,249); B25063e21 ($1,250 to $1,499); B25063e22 ($1,500 to $1,999); B25063e23 ($2,000 to $2,499); B25063e24 ($2,500 to $2,999); B25063e25 ($3,000 to $3,499); B25063e26 ($3,500 or more); B25063e27 (No cash rent); B25064e1 (Median gross rent (dollars)); B25065e1 (Aggregate gross rent (dollars)).
[<div align="right"><< Back to List</div>](#h-housing-characteristics-23-groups-406-fields)

#### H23: Gross Rent as Percentage of Household Income (11 variables)

> B25070e1 (Occupied units paying rent); B25070e2 (Less than 10.0 percent); B25070e3 (10.0 to 14.9 percent); B25070e4 (15.0 to 19.9 percent); B25070e5 (20.0 to 24.9 percent); B25070e6 (25.0 to 29.9 percent); B25070e7 (30.0 to 34.9 percent); B25070e8 (35.0 to 39.9 percent); B25070e9 (40.0 to 49.9 percent); B25070e10 (50.0 percent or more); B25070e11 (Not computed).
[<div align="right"><< Back to List</div>](#h-housing-characteristics-23-groups-406-fields)

[<div align="right"><< Back to ReadMe.md</div>](../README.md)
