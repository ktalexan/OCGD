# scripts

This folder contains helper scripts for generating and maintaining
ACS variable JSON files.

- `generate_acs_vars_by_year.py` — generates `codebook/acs_variables_{year}.json`
  files for years 2010–2023 by copying `codebook/acs_variables_master.json`.
  If a `check_census_var.py` script is present in the repo, the generator
  will attempt to call it to validate and update variables for each year.

Usage:
```bash
python scripts/generate_acs_vars_by_year.py
```

If you have a `check_census_var.py` script, place it in the repo root or
in `scripts/` so the generator can find and use it.
# Scripts Folder

