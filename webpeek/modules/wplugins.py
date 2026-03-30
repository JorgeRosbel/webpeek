import requests
import re


def fetcher(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
    }
    try:
        full_url = url if url.startswith(('http://', 'https://')) else f"https://{url}"
        response = requests.get(full_url, headers=headers, timeout=10, verify=False)
        return response.text
    except:
        return None


def get_wordpress_plugins(url):
    html = fetcher(url)
    if not html:
        return []
    
    plugins = {}
    html_lower = html.lower()

    if 'wp-content' not in html_lower and 'wp-includes' not in html_lower:
        return []

    pattern_path = re.compile(
        r'/wp-content/plugins/([a-zA-Z0-9_-]+)(?:/[^"\'>\s]*)?'
        r'(?:["\'\s].*?(?:ver|version)[=\s]+["\']?([0-9][0-9a-zA-Z._-]*))?',
        re.IGNORECASE,
    )

    for match in pattern_path.finditer(html):
        name = match.group(1)
        version = match.group(2)
        if name not in plugins:
            plugins[name] = {
                "name": name,
                "version": version or "unknown"
            }

    pattern_ver = re.compile(
        r'/wp-content/plugins/([a-zA-Z0-9_-]+)/[^"\'>\s]*\?(?:[^"\'>\s]*&)?ver=([0-9][0-9a-zA-Z._-]*)',
        re.IGNORECASE,
    )
    for match in pattern_ver.finditer(html):
        name = match.group(1)
        version = match.group(2)
        if name in plugins and plugins[name]["version"] == "unknown":
            plugins[name]["version"] = version

    pattern_comment = re.compile(
        r'<!--[^-]*?plugin[s]?\s*[:\-]?\s*([a-zA-Z0-9][a-zA-Z0-9_\- ]{2,40}?)(?:\s+v?([0-9][0-9a-zA-Z._-]*))?',
        re.IGNORECASE,
    )
    for match in pattern_comment.finditer(html):
        raw_name = match.group(1).strip()
        version = match.group(2)
        slug = raw_name.lower().replace(" ", "-")
        if slug and slug not in plugins:
            plugins[slug] = {
                "name": raw_name,
                "version": version or "unknown"
            }

    return list(plugins.values())[:20]
