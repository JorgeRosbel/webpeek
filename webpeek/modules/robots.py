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


EXPOSED_PATHS = [
    '/.env', '/.env.local', '/.env.prod', '/.env.dev', '/.env.bak',
    '/.aws/credentials', '/.vscode/sftp.json', '/.ssh/id_rsa',
    '/.git/config', '/.git/index', '/.gitignore', '/.svn/entries',
    '/wp-config.php.bak', '/wp-config.php.old', '/wp-config.php.save', '/wp-config.php~',
    '/wp-content/debug.log', '/wp-content/uploads/debug.log',
    '/wp-json/wp/v2/users', '/wp-links-opml.php', '/xmlrpc.php',
    '/backup.sql', '/db.sql', '/db_backup.sql', '/database.sql', '/dump.sql',
    '/db.zip', '/backup.zip', '/site.zip', '/www.zip', '/old.zip',
    '/latest.tar.gz', '/site.tar.gz', '/backup.tar.gz', '/full.sql',
    '/phpinfo.php', '/info.php', '/status', '/server-status',
    '/error_log', '/error.log', '/access.log', '/debug.log',
    '/.htaccess.bak', '/.htpasswd', '/web.config',
    '/package.json', '/composer.json', '/composer.lock',
    '/.npmrc', '/yarn.lock', '/docker-compose.yml',
    '/backup/', '/backups/', '/css/', '/js/', '/images/', '/uploads/',
    '/sql/', '/temp/', '/tmp/', '/old/',
    '/admin', '/wp-admin', '/phpmyadmin', '/administrator', '/login',
    '/wp-login.php', '/readme.html', '/readme.txt', '/license.txt',
    '/install.php', '/test/', '/api/',
]


def check_path(url, path):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
    }
    try:
        full_url = f"https://{url}{path}"
        response = requests.get(full_url, headers=headers, timeout=5, verify=False, allow_redirects=False)
        return f"{path} [{response.status_code}]"
    except:
        return None


def check_exposed(url):
    exposed = []
    for path in EXPOSED_PATHS:
        result = check_path(url, path)
        if result:
            exposed.append(result)
    return exposed[:25]
