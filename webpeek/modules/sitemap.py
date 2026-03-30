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
