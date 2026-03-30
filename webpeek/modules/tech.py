import requests
import re


def get_html(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
        "Accept-Language": "es-ES,es;q=0.9,en;q=0.8",
    }
    
    try:
        full_url = url if url.startswith(('http://', 'https://')) else f"https://{url}"
        response = requests.get(full_url, headers=headers, timeout=10, verify=False)
        
        headers_found = {}
        for header in ['Server', 'X-Powered-By', 'Content-Type']:
            headers_found[header] = response.headers.get(header, "Not Found")
        
        return {"html": response.text, "headers": headers_found}
    except:
        return None


def get_wordpress_plugins(html):
    plugins = {}
    
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
                "version": version or "unknown",
            }
        elif version and plugins[name]["version"] == "unknown":
            plugins[name]["version"] = version
    
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
        r'<!--[^-]*?plugin[s]?\s*[:\-]?\s*([a-zA-Z0-9][a-zA-Z0-9_\- ]{2,40}?)(?:\s+v?([0-9][0-9a-zA-Z._-]*))?(?:\s+active|\s+enabled|-->)',
        re.IGNORECASE,
    )
    for match in pattern_comment.finditer(html):
        raw_name = match.group(1).strip()
        version = match.group(2)
        slug = raw_name.lower().replace(" ", "-")
        if slug and slug not in plugins:
            plugins[slug] = {
                "name": raw_name,
                "version": version or "unknown",
            }
    
    return list(plugins.values())[:20]


def get_technologies(url):
    content = get_html(url)
    if not content:
        return []
    
    html = content["html"]
    html_lower = html.lower()
    results = []
    
    if "_astro/" in html_lower:
        results.append("Astro")
    if "gtag" in html_lower or "google-analytics" in html_lower:
        results.append("Google Analytics")
    if "elementor-section" in html_lower:
        results.append("Elementor")
    if "https://www.googletagmanager.com" in html_lower:
        results.append("Google Tag Manager")
    if "text-" in html_lower or "bg-" in html_lower or "border-" in html_lower:
        results.append("Tailwind CSS")
    if any(x in html_lower for x in ["wp-content", "wp-includes", "elementor/", "ver-wp"]):
        results.append("WordPress")
    if any(x in html_lower for x in ["__next_f", "/_next/static", "next-hal-stack"]):
        results.append("Next.js")
    if "data-shopify" in html_lower or "cdn.shopify.com" in html_lower:
        results.append("Shopify")
    if any(x in html_lower for x in ["id='root'", 'id="root"', "react-dom", "__react", "data-reactroot"]):
        results.append("React")
    if "data-styled=" in html_lower or "data-styled-components" in html_lower:
        results.append("Styled Components")
    if "jquery" in html_lower:
        results.append("jQuery")
    if "bootstrap" in html_lower:
        results.append("Bootstrap")
    if "vue" in html_lower:
        results.append("Vue.js")
    
    return list(set(results)) if results else ["Unknown"]


def get_wplugins(url):
    content = get_html(url)
    if not content:
        return []
    
    return get_wordpress_plugins(content["html"])
