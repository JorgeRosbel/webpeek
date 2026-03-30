import requests
import re
from bs4 import BeautifulSoup


SOCIAL_PATTERNS = {
    'facebook': [
        r'facebook\.com/[\w.-]+',
        r'fb\.com/[\w.-]+',
    ],
    'twitter': [
        r'twitter\.com/[\w.-]+',
        r'x\.com/[\w.-]+',
    ],
    'instagram': [
        r'instagram\.com/[\w.-]+',
    ],
    'linkedin': [
        r'linkedin\.com/(?:company|in|school)/[\w.-]+',
    ],
    'youtube': [
        r'youtube\.com/(?:channel|c|user|@)[\w.-]+',
        r'youtu\.be/[\w.-]+',
    ],
    'tiktok': [
        r'tiktok\.com/@[\w.-]+',
    ],
    'pinterest': [
        r'pinterest\.com/[\w.-]+',
    ],
    'reddit': [
        r'reddit\.com/(?:u|user)/[\w.-]+',
        r'reddit\.com/r/[\w.-]+',
    ],
    'github': [
        r'github\.com/[\w.-]+',
    ],
    'mastodon': [
        r'mastodon\.social/@[\w.-]+',
        r'[\w.-]+\.mastodon\..+/@[\w.-]+',
    ],
}


def extract_social_links(html):
    found = {}
    
    for platform, patterns in SOCIAL_PATTERNS.items():
        for pattern in patterns:
            matches = re.findall(r'https?://' + pattern, html, re.IGNORECASE)
            if matches:
                unique_matches = list(set(matches))
                if platform not in found:
                    found[platform] = unique_matches
                else:
                    found[platform].extend(unique_matches)
    
    soup = BeautifulSoup(html, 'lxml')
    
    social_meta = soup.find_all('meta', property=re.compile(r'^og:(?:url|type)'))
    for meta in social_meta:
        content = meta.get('content', '')
        if content and any(domain in content for domain in ['facebook.com', 'fb.com', 'instagram.com', 'linkedin.com', 'twitter.com', 'x.com', 'youtube.com', 'tiktok.com']):
            for platform in SOCIAL_PATTERNS:
                if any(p in content.lower() for p in [platform, platform.replace('linkedin', 'linkedin').replace('youtube', 'youtube')]):
                    if platform not in found:
                        found[platform] = [content]
                    elif content not in found[platform]:
                        found[platform].append(content)
    
    links = soup.find_all('a', href=True)
    for link in links:
        href = link.get('href', '')
        for platform, patterns in SOCIAL_PATTERNS.items():
            for pattern in patterns:
                if re.search(pattern, href, re.IGNORECASE):
                    full_url = href if href.startswith('http') else f"https://{href}"
                    if platform not in found:
                        found[platform] = [full_url]
                    elif full_url not in found[platform]:
                        found[platform].append(full_url)
    
    result = {}
    for platform, urls in found.items():
        unique_urls = list(set(urls))[:3]
        result[platform] = unique_urls
    
    return result if result else None


def get_social(html=None):
    try:
        if html:
            return extract_social_links(html)
        return None
    except Exception as e:
        return None
