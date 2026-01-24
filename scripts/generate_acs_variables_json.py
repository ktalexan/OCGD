import re
import json
from pathlib import Path


MD_PATH = Path("documentation/acs_variables.md")
OUT_PATH = Path("codebook/acs_variables.json")


def normalize_e_suffix(name: str) -> str:
    m = re.search(r'e(\d{1,3})$', name)
    if m:
        num = int(m.group(1))
        return re.sub(r'e(\d{1,3})$', f'_{num:03d}E', name)
    return name


def parse_markdown(text: str):
    lines = text.splitlines()
    data = {}
    current_category = None
    id_counters = {}

    i = 0
    while i < len(lines):
        line = lines[i].strip()
        # First-level heading (category)
        if line.startswith('# '):
            m = re.match(r'^#\s*[^:]+:\s*(.+)$', line)
            if m:
                current_category = m.group(1).strip()
                data.setdefault(current_category, {})
                id_counters[current_category] = 1
            i += 1
            continue

        # Second-level heading (group)
        if line.startswith('## '):
            mg = re.match(r'^##\s*[^:]+:\s*(.+?)\s*\((\d+)', line)
            if mg and current_category is not None:
                group_category = mg.group(1).strip()
                group_count = int(mg.group(2))

                # collect following paragraph lines until next heading or EOF
                j = i + 1
                block = []
                while j < len(lines) and not lines[j].startswith('## ') and not lines[j].startswith('# '):
                    if lines[j].strip():
                        block.append(lines[j].strip())
                    j += 1
                paragraph = ' '.join(block)

                # extract variable tuples: name and alias
                tuples = re.findall(r'([A-Za-z0-9]+)\s*\(([^)]+)\)', paragraph)
                for varname, alias in tuples:
                    newname = normalize_e_suffix(varname)
                    group = newname.split('_')[0] if '_' in newname else newname

                    entry = {
                        "id": id_counters[current_category],
                        "name": newname,
                        "alias": alias.strip(),
                        "description": "",
                        "type": "",
                        "category": current_category,
                        "group_category": group_category,
                        "group_count": group_count,
                        "group": group,
                        "group_code": "",
                    }

                    data[current_category][newname] = entry
                    id_counters[current_category] += 1

                i = j
                continue
        i += 1

    return data


def main():
    if not MD_PATH.exists():
        raise FileNotFoundError(f"{MD_PATH} not found")

    text = MD_PATH.read_text(encoding='utf-8')
    data = parse_markdown(text)
    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUT_PATH.write_text(json.dumps(data, indent=2, ensure_ascii=False))
    print(f"Wrote {OUT_PATH}")


if __name__ == '__main__':
    main()
