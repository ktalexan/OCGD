# General <REPO_NAME> Repository Notes

This document contains general notes and guidelines for the <REPO_NAME> repository. It is intended to help contributors understand the structure, conventions, and best practices for working within this repository.

## Repository Desccription

<REPO_DESCRIPTION>

## Basic Repository Structure

The repository is organized into the following main directories:
- [admin](./): Administrative scripts and tools.
- [analysis](../analysis): Data analysis scripts and notebooks.
- [codebook](../codebook): Documentation of variables and data sources.
- [data](../data): Raw and processed data files.
- [documentation](../documentation): Documentation files and guides.
- [gis (optional)](../gis): Geographic Information System (GIS) data and scripts.
- [graphics](../graphics): Visualization scripts and output images.
- [metadata](../metadata): Metadata files describing datasets.
- [notebooks](../notebooks): Jupyter notebooks for exploration and analysis.
- [scripts](../scripts): Reusable scripts and functions.
- [tests](../tests): Unit tests and test data.


## Useful Links

- [Adding repository custom instructions for GitHub Copilot](https://docs.github.com/en/copilot/how-tos/configure-custom-instructions/add-repository-instructions?tool=vscode)

## Notes and ToDo's:

### Integrating US Census Community Resilience Estimates (CRE) Data for OC

- [Census CRE Page](https://www.census.gov/programs-surveys/community-resilience-estimates.html)
- [CRE Datasets](https://www.census.gov/programs-surveys/community-resilience-estimates/data/datasets.html)
- [Available Census APIs](https://www.census.gov/data/developers/data-sets.html)
- [Community Resilience Estimates (CRE) Census API Page](https://www.census.gov/data/developers/data-sets/community-resilience-estimates.html)
- [API Settings](https://api.census.gov/data/2024/cre.html)
- CRE Years: 2019-2024
- Example API Call: https://api.census.gov/data/2024/cre?get=SUMLEVEL,GEOCOMP,GEO_ID,NAME,POPUNI,PRED0_E,PRED12_E,PRED3_E,PRED0_PE,PRED12_PE,PRED3_PE,PRED0_M,PRED12_M,PRED3_M,PRED0_PM,PRED12_PM,PRED3_PM&for=tract:*&in=state:06&in=county:059
- The only useful geography for OC is Census Tract.

CRE Variables:

| Type | Variable | Description |
| :---- | :---- | :---- |
| Geography | SUMLEVEL | Summary Level code |
| Geography | GEOCOMP | GEO_ID Component |
| Geography | GEO_ID | Geographic Identifier |
| Geography | NAME | Full name of the component |
| Population | POPUNI | Population Universe |
| Estimate | PRED0_E | Estimate, 0 components of social vulnerability |
| Estimate | PRED12_E | Estimate, 1-2 components of social vulnerability |
| Estimate | PRED3_E | Estimate, 3+ components of social vulnerability |
| Percent | PRED0_PE | Percent, 0 components of social vulnerability |
| Percent | PRED12_PE | Percent, 1-2 components of social vulnerability |
| Percent | PRED3_PE | ercent, 3+ components of social vulnerability |
| Margin of Error | PRED0_M | Margin of error, 0 components of social vulnerability |
| Margin of Error | PRED12_M | Margin of error, 1-2 components of social vulnerability |
| Margin of Error | PRED3_M& | Margin of error, 3+ components of social vulnerability |
| Percent Margin of Error | PRED0_PM | Percent Margin of error, 0 components of social vulnerability |
| Percent Margin of Error | PRED12_PM | Percent Margin of error, 1-2 components of social vulnerability |
| Percent Margin of Error | PRED3_PM | Percent Margin of error, 3+ components of social vulnerability |
| Automatic | state | State |
| Automatic | county | County |
| Automatic | tract | Census Tract |

- Completed the CRE codebook function of the class. It now obtains and exports the CRE census variable codebook for a given year into a JSON dictionary (also saves it to the codebook directory) - 2/1/2026 5:35 AM

- Completed the CRE table query function of the class. It now obtains the data table of the CRE estimates for a given year (so it can joined based on geoid with the Tiger/Line geographies) - 2/1/2026 5:36 AM

