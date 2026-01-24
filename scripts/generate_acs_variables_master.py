import re
import json
from pathlib import Path


def normalize_category(header_line: str) -> str:
    text = header_line.strip()
    if ':' in text:
        return text.split(':', 1)[1].strip()
    return text


def normalize_group(header_line: str) -> (str, int):
    text = header_line.strip()
    if ':' in text:
        text = text.split(':', 1)[1].strip()
    m = re.search(r"\((\d+)\)", text)
    count = int(m.group(1)) if m else 0
    group_cat = re.sub(r"\s*\(\d+\)", '', text).strip()
    return group_cat, count


def replace_e_digits(varname: str) -> str:
    def repl(m):
        num = m.group(1)
        return '_' + num.zfill(3) + 'E'
    return re.sub(r'e(\d{1,3})', repl, varname, flags=re.IGNORECASE)


def parse_markdown(md_text: str) -> dict:
    lines = md_text.splitlines()
    result = {}
    current_category = None
    current_group_category = ''
    current_group_count = 0
    id_counters = {}
    buffer = []

    def flush_buffer():
        nonlocal buffer, current_category, current_group_category, current_group_count
        if not buffer or not current_category:
            buffer = []
            return
        text = ' '.join(buffer)
        # find variable definitions like NAME (Alias);
        pattern = re.compile(r'([^\s(]+)\s*\(([^)]+)\)\s*[;\.]')
        matches = list(pattern.finditer(text))
        for m in matches:
            var_key = m.group(1).strip()
            alias = m.group(2).strip()
            if current_category not in id_counters:
                id_counters[current_category] = 1
            vid = id_counters[current_category]
            id_counters[current_category] += 1

            name_after = replace_e_digits(var_key)
            group_val = var_key.split('_', 1)[0] if '_' in var_key else var_key

            entry = {
                'id': vid,
                'name': name_after,
                'alias': alias,
                'description': '',
                'label': '',
                'type': '',
                'category': current_category,
                'group_category': current_group_category,
                'group_count': current_group_count,
                'group': group_val,
                'group_code': '',
                'limit': '',
                'attributes': ''
            }
            result.setdefault(current_category, {})[var_key] = entry

        buffer = []

    for line in lines:
        stripped = line.strip()
        if stripped.startswith('# '):
            # flush previous group
            flush_buffer()
            # set new category
            header = stripped[2:].strip()
            category = normalize_category(header)
            current_category = category
            current_group_category = ''
            current_group_count = 0
            continue
        if stripped.startswith('## '):
            # flush previous group's buffer
            flush_buffer()
            header2 = stripped[3:].strip()
            group_cat, count = normalize_group(header2)
            current_group_category = group_cat
            current_group_count = count
            continue
        if stripped == '':
            # ignore empty lines but keep them as separators
            continue
        # otherwise collect variable lines
        buffer.append(stripped)

    # final flush
    flush_buffer()
    return result


def main():
    repo_root = Path(__file__).resolve().parents[1]
    md_path = repo_root / 'documentation' / 'acs_variables.md'
    out_path = repo_root / 'codebook' / 'acs_variables_master.json'
    out_path.parent.mkdir(parents=True, exist_ok=True)

    md_text = md_path.read_text(encoding='utf-8')
    result = parse_markdown(md_text)

    out_path.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
    print(f'Wrote {out_path}')


if __name__ == '__main__':
    main()
