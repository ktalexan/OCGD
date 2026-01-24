#!/usr/bin/env python3
"""Generate acs_variables_master.json from documentation/acs_variables.md.

This script follows the project instructions (.github/instructions/acs_vars_master.instructions.md)
to parse first-level headings as categories, second-level headings as group categories,
and variable definition lines as variable entries. It writes a JSON file to
`codebook/acs_variables_master.json`.

Usage: python .github/scripts/generate_acs_vars_master.py
"""
from __future__ import annotations

import json
import os
import re
from typing import Dict, Any


def normalize_category_heading(line: str) -> str:
    # Expect format like '# D: Demographic Characteristics'
    if ":" in line:
        return line.split(":", 1)[1].strip()
    return line.lstrip("# ").strip()


def parse_group_heading(line: str) -> tuple[str, int]:
    # Expect format like '## D01: Sex And Age (49 variables)'
    # Return (group_category, group_count)
    text = line.lstrip("# ").strip()
    # split by ':' to remove code
    if ":" in text:
        after_code = text.split(":", 1)[1].strip()
    else:
        after_code = text
    # group_count inside parentheses at end
    m = re.search(r"\(([^)]*?(\d+)[^)]*?)\)\s*$", after_code)
    if m:
        # extract number
        count_match = re.search(r"(\d+)", m.group(1))
        group_count = int(count_match.group(1)) if count_match else 0
        # group name is text before the parentheses
        group_name = re.sub(r"\([^)]*\)\s*$", "", after_code).strip()
        return group_name, group_count
    return after_code, 0


def replace_e_suffix(name: str) -> str:
    # Replace trailing 'e' + 1-3 digits with '_###E' padded to 3 digits.
    m = re.search(r"e(\d{1,3})$", name)
    if m:
        num = int(m.group(1))
        return re.sub(r"e\d{1,3}$", f"_{num:03d}E", name)
    return name


def ensure_dir(path: str) -> None:
    os.makedirs(path, exist_ok=True)


def main() -> None:
    base = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    md_path = os.path.join(base, "documentation", "acs_variables.md")
    out_dir = os.path.join(base, "codebook")
    out_path = os.path.join(out_dir, "acs_variables_master.json")

    if not os.path.exists(md_path):
        raise FileNotFoundError(f"Markdown file not found: {md_path}")

    with open(md_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    result: Dict[str, Dict[str, Any]] = {}

    current_category = None
    current_group = None
    current_group_count = 0
    # id counters reset per category
    category_id_counters: Dict[str, int] = {}

    for raw in lines:
        line = raw.strip()
        if not line:
            continue
        if line.startswith("# ") and not line.startswith("##"):
            # first-level heading -> new category
            current_category = normalize_category_heading(line)
            result.setdefault(current_category, {})
            category_id_counters[current_category] = 0
            continue
        if line.startswith("## "):
            # second-level heading
            group_name, group_count = parse_group_heading(line)
            current_group = group_name
            current_group_count = group_count
            continue
        # otherwise treat as variable definition line which may contain many entries
        # split at semicolons
        parts = [p.strip() for p in re.split(r";\s*", line) if p.strip()]
        for part in parts:
            # each part expected like: 'B01001e1 (Total population)'
            if "(" not in part:
                continue
            first_paren = part.find("(")
            last_paren = part.rfind(")")
            if first_paren == -1 or last_paren == -1 or last_paren < first_paren:
                continue
            var_key = part[:first_paren].strip()
            alias = part[first_paren + 1 : last_paren].strip()

            if current_category is None:
                # skip entries before first category
                continue

            category_id_counters[current_category] += 1
            vid = category_id_counters[current_category]

            name_replaced = replace_e_suffix(var_key)
            group = name_replaced.split("_")[0]

            entry = {
                "id": vid,
                "name": name_replaced,
                "alias": alias,
                "description": "",
                "label": "",
                "type": "",
                "category": current_category,
                "group_category": current_group or "",
                "group_count": current_group_count,
                "group": group,
                "group_code": "",
                "limit": "",
                "attributes": "",
            }

            # Use the converted variable name as the dictionary key per instructions
            result[current_category][name_replaced] = entry

    ensure_dir(out_dir)
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

    print(f"Wrote {out_path}")


if __name__ == "__main__":
    main()
