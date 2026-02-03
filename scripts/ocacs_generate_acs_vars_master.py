#!/usr/bin/env python3
"""Generate acs_variables_master.json from documentation/acs_variables.md.

This implements the transformation rules in .github/instructions/acs_vars_master.instructions.md
"""
import json
import re
from pathlib import Path


def normalize_e_suffix(var: str) -> str:
    """Replace trailing e### with _###E (pad to 3 digits).

    Examples:
      B01001e1 -> B01001_001E
      B01002Ae12 -> B01002A_012E
    """
    m = re.search(r'e(\d{1,})$', var)
    if not m:
        return var
    num = int(m.group(1))
    return re.sub(r'e(\d{1,})$', f'_{num:03d}E', var)


def parse_markdown(md_text: str):
    lines = md_text.splitlines()
    data = {}
    counters = {}
    current_category = None
    group_name = ""
    group_code = ""
    group_count = 0

    for line in lines:
        line = line.strip()
        if not line:
            continue

        # First-level heading: "# CODE: Category Name" (match single '#')
        m = re.match(r"^#\s+[^:]+:\s*(.+)$", line)
        if m:
            current_category = m.group(1).strip()
            data.setdefault(current_category, {})
            counters[current_category] = 1
            continue

        # Second-level heading: "## CODE: Group Name (N variables)"
        m2 = re.match(r"^##\s+([^:]+):\s*(.+?)\s*\((\d+)[^)]*\)", line)
        if m2:
            group_code = m2.group(1).strip()
            group_name = m2.group(2).strip()
            try:
                group_count = int(m2.group(3))
            except Exception:
                group_count = 0
            continue

        # Extract variable definitions like: B01001e1 (Total population);
        entries = re.findall(r'([A-Za-z0-9]+)\s*\(([^)]*)\)', line)
        for var, alias in entries:
            if current_category is None:
                continue
            id_val = counters[current_category]
            counters[current_category] += 1

            name_replaced = normalize_e_suffix(var)
            group = name_replaced.split("_")[0] if "_" in name_replaced else name_replaced

            entry = {
                "id": id_val,
                "name": name_replaced,
                "alias": alias.strip(),
                "description": "",
                "label": "",
                "type": "",
                "category": current_category,
                "group_category": group_name,
                "group_count": group_count,
                "group": group,
                "group_code": group_code,
                "limit": "",
                "attributes": "",
            }

            # Use the normalized name (with _###E) as the JSON key per instructions
            data[current_category][name_replaced] = entry

    return data


def main():
    repo_root = Path(__file__).resolve().parents[1]
    md_path = repo_root / "documentation" / "acs_variables.md"
    out_path = repo_root / "codebook" / "acs_variables_master.json"

    text = md_path.read_text(encoding="utf-8")
    result = parse_markdown(text)

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Wrote {out_path}")


if __name__ == "__main__":
    main()
