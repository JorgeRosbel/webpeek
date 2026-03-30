from webpeek.utils.colors import format_output, Colors


def format_list_value(value):
    if isinstance(value, dict):
        return value
    
    if not isinstance(value, list):
        return str(value)
    
    if not value:
        return ""
    
    if isinstance(value[0], dict):
        if 'name' in value[0] and 'version' in value[0]:
            return "\n".join(f"  • {v['name']} ({v['version']})" for v in value)
        return "\n".join(f"  • {v}" for v in value)
    
    return "\n".join(f"  • {v}" for v in value)


def print_results(target, results, use_color=True, is_custom=False):
    clean_results = {}
    for key, value in results.items():
        if key == 'IP' and is_custom:
            continue
        if value and (isinstance(value, dict) or str(value).strip()):
            if isinstance(value, dict):
                clean_results[key] = value
            else:
                formatted = format_list_value(value)
                clean_results[key] = formatted[:200]

    if not clean_results:
        if use_color:
            print(f"{Colors.warning('No results found')}")
        else:
            print("No results found")
        return

    output = format_output(target, clean_results, use_color, is_custom)
    print(output)


def save_to_file(filename, content):
    try:
        with open(filename, 'w') as f:
            f.write(content)
        return True
    except Exception as e:
        return False
