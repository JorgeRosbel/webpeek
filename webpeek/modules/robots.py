import requests
import re
from bs4 import BeautifulSoup


COMMON_SITEMAPS = [
    "/sitemap.xml",
    "/sitemap_index.xml",
    "/sitemap-index.xml",
    "/sitemap-0.xml",
    "/sitemap1.xml",
    "/sitemap2.xml",
    "/wp-sitemap.xml",
    "/wp-sitemap-posts-post-1.xml",
    "/wp-sitemap-posts-page-1.xml",
    "/sitemap_products.xml",
    "/sitemap_categories.xml",
    "/sitemap_pages.xml",
    "/sitemap_posts.xml",
    "/news-sitemap.xml",
    "/video-sitemap.xml",
    "/image-sitemap.xml",
]


def fetcher(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
    }
    try:
        response = requests.get(f"https://{url}", headers=headers, timeout=10, verify=False)
        return response.text
    except:
        return None


def find_robots(url):
    try:
        return fetcher(f'{url}/robots.txt')
    except:
        return None


def extract_sitemap_list(url):
    robots = find_robots(url)
    
    if not robots:
        return None
    
    pattern = r'\S*sitemap\S*'
    matches = re.findall(pattern, robots)
    
    if matches:
        sitemaps_list = [f"/{item.split('/')[3]}" for item in list(set(matches))]
        return sitemaps_list
    else:
        return None


def extract_urls_from_sitemap(sitemap_content):
    urls = []
    if sitemap_content:
        soup = BeautifulSoup(sitemap_content, "xml")
        for loc in soup.find_all("loc"):
            urls.append(loc.text)
    return urls


def get_sitemap(url):
    sitemaps_names = extract_sitemap_list(url)
    
    if not sitemaps_names:
        return "Not found"
    
    urls = []
    for sitemap in sitemaps_names:
        try:
            fetcher_response = fetcher(f'{url}{sitemap}')
            if fetcher_response:
                urls.extend(extract_urls_from_sitemap(fetcher_response))
        except:
            pass
    
    if urls:
        return list(set(urls))[:50]
    
    return "Not found"


def get_robots(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
    }
    try:
        response = requests.get(f"https://{url}/robots.txt", headers=headers, timeout=10, verify=False)
        
        if response.status_code == 404:
            return "Not found"
        
        if response.status_code != 200:
            return f"Error: HTTP {response.status_code}"
        
        content = response.text
        if content and not content.strip().startswith('<!DOCTYPE') and not content.strip().startswith('<html'):
            lines = content.split('\n')
            
            disallow_list = []
            allow_list = []
            
            for line in lines:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                
                match_disallow = re.match(r'^Disallow:\s*(.*)$', line, re.IGNORECASE)
                match_allow = re.match(r'^Allow:\s*(.*)$', line, re.IGNORECASE)
                
                if match_disallow:
                    path = match_disallow.group(1).strip()
                    if path:
                        disallow_list.append(path)
                elif match_allow:
                    path = match_allow.group(1).strip()
                    if path:
                        allow_list.append(path)
            
            if disallow_list or allow_list:
                return {
                    'disallow': disallow_list[:15],
                    'allow': allow_list[:10]
                }
            
            return "Empty (no rules defined)"
        
        return "Not found (HTML returned)"
    except Exception as e:
        return "Not found"

