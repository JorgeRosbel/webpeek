import requests
import socket
import dns.resolver
import whois
import warnings
import subprocess
import re
import sys
from datetime import datetime
from bs4 import BeautifulSoup

warnings.filterwarnings('ignore', message='Unverified HTTPS request')


class Scanner:
    def __init__(self, target, verbose=False, use_color=True, use_dynamic=False):
        self.target = target
        self.verbose = verbose
        self.use_color = use_color
        self.use_dynamic = use_dynamic
        self.results = {}
        self.ip = None
        self._html_cache = None
    
    def _log(self, message):
        print(f"[*] {message}")
    
    def _get_html(self):
        if self._html_cache is not None:
            return self._html_cache
        
        if self.use_dynamic:
            from webpeek.modules.tech import get_html_dynamic
            content = get_html_dynamic(self.target)
            self._html_cache = content["html"] if content else None
        else:
            from webpeek.modules.tech import get_html
            content = get_html(self.target)
            self._html_cache = content["html"] if content else None
        
        return self._html_cache

    def get_ip(self):
        if self.ip:
            return self.ip
        try:
            self.ip = socket.gethostbyname(self.target)
            return self.ip
        except:
            return None

    def scan_passive(self, modules):
        self._log(f"Starting scan on {self.target}")
        
        if 'whois' in modules:
            self._log("Checking WHOIS...")
            self.results['WHOIS'] = self.whois_lookup()
        
        if 'dns' in modules:
            self._log("Resolving DNS...")
            self.results['DNS'] = self.dns_lookup()
        
        if 'mx' in modules:
            self._log("Checking MX records...")
            self.results['MX'] = self.mx_lookup()
        
        if 'txt' in modules:
            self._log("Checking TXT records...")
            self.results['TXT'] = self.txt_lookup()
        
        if 'subdomains' in modules:
            self._log("Finding subdomains...")
            from webpeek.modules import subdomains
            subs = subdomains.get_subdomains(self.target)
            if subs:
                self.results['Subdomains'] = subs
        
        return self.results

    def scan_active(self, modules):
        ip = self.get_ip()
        if ip:
            self.results['IP'] = ip
        
        if 'geo' in modules:
            self._log("Getting geolocation...")
            from webpeek.modules import geo
            self.results['Geo'] = geo.get_geo(ip) if ip else None
        
        if 'emails' in modules:
            self._log("Extracting emails...")
            from webpeek.modules import emails
            html = self._get_html()
            ems = emails.get_emails(html)
            if ems:
                self.results['Emails'] = ems
        
        if 'phones' in modules:
            self._log("Extracting phone numbers...")
            from webpeek.modules import emails
            html = self._get_html()
            phs = emails.get_phones(html)
            if phs:
                self.results['Phones'] = phs
        
        if 'os' in modules:
            self._log("Detecting OS (TTL)...")
            self.results['OS'] = self.os_detection()
        
        if 'headers' in modules:
            self._log("Fetching HTTP headers...")
            from webpeek.modules import headers as h
            self.results['Headers'] = h.get_headers(self.target)
        
        if 'security' in modules:
            self._log("Auditing security headers...")
            from webpeek.modules import security_headers
            self.results['Security Headers'] = security_headers.get_security_headers(self.target)
        
        if 'tech' in modules:
            self._log("Detecting technologies...")
            from webpeek.modules import tech
            result = tech.get_technologies(self.target, self.use_dynamic)
            self.results['Technologies'] = result
        
        if 'wplugins' in modules:
            self._log("Detecting WordPress plugins...")
            from webpeek.modules import tech
            result = tech.get_wplugins(self.target, self.use_dynamic)
            if result:
                self.results['WordPress Plugins'] = result
        
        if 'ssl' in modules:
            self._log("Checking SSL certificate...")
            from webpeek.modules import ssl_info
            self.results['SSL'] = ssl_info.get_ssl_info(self.target)
        
        if 'title' in modules:
            self._log("Getting page title...")
            self.results['Title'] = self.get_title()
        
        if 'description' in modules:
            self._log("Getting meta description...")
            self.results['Description'] = self.get_description()
        
        if 'sitemap' in modules:
            self._log("Fetching sitemap...")
            from webpeek.modules import sitemap
            urls = sitemap.get_sitemap(self.target)
            if urls:
                self.results['Sitemap'] = urls
        
        if 'robots' in modules:
            self._log("Fetching robots.txt...")
            from webpeek.modules import robots
            robots_data = robots.get_robots(self.target)
            if robots_data:
                self.results['Robots'] = robots_data
        
        if 'social' in modules:
            self._log("Extracting social networks...")
            from webpeek.modules import social
            html = self._get_html()
            social_data = social.get_social(html)
            if social_data:
                self.results['Social'] = social_data
        
        return self.results

    def whois_lookup(self):
        try:
            w = whois.query(self.target)
            if w:
                parts = []
                if hasattr(w, 'registrar') and w.registrar:
                    parts.append(f"Registrar: {w.registrar}")
                created = getattr(w, 'creation_date', None)
                if isinstance(created, list):
                    created = created[0]
                if created:
                    parts.append(f"Created: {created.strftime('%Y-%m-%d')}")
                if hasattr(w, 'expiration_date') and w.expiration_date:
                    exp = w.expiration_date
                    if isinstance(exp, list):
                        exp = exp[0]
                    parts.append(f"Expires: {exp.strftime('%Y-%m-%d')}")
                return " | ".join(parts) if parts else "No data"
            return "Available"
        except Exception as e:
            return f"Error: {str(e)[:60]}"

    def dns_lookup(self):
        try:
            resolver = dns.resolver.Resolver()
            answers = resolver.resolve(self.target, 'A')
            return ", ".join([rdata.to_text() for rdata in answers])
        except:
            return "No A records found"

    def mx_lookup(self):
        try:
            resolver = dns.resolver.Resolver()
            answers = resolver.resolve(self.target, 'MX')
            mx_records = []
            for rdata in answers:
                exchange = str(rdata)
                mx_records.append(exchange)
            return sorted(mx_records)
        except:
            return []

    def txt_lookup(self):
        try:
            resolver = dns.resolver.Resolver()
            answers = resolver.resolve(self.target, 'TXT')
            txt_records = []
            spf_found = False
            dkim_found = False
            
            for rdata in answers:
                txt = rdata.to_text().strip('"')
                txt_records.append(txt)
                if txt.startswith('v=spf1'):
                    spf_found = True
                if 'dkim' in txt.lower():
                    dkim_found = True
            
            result = []
            if spf_found:
                result.append("SPF: Found")
            if dkim_found:
                result.append("DKIM: Found")
            result.extend(txt_records[:5])
            return result
        except:
            return []

    def os_detection(self):
        try:
            hostname = self.target.split(':')[0] if ':' in self.target else self.target
            result = subprocess.run(['ping', '-c', '1', '-W', '2', hostname], 
                                  capture_output=True, text=True, timeout=5)
            output = result.stdout
            
            ttl_match = re.search(r'ttl=(\d+)', output, re.IGNORECASE)
            if ttl_match:
                ttl = int(ttl_match.group(1))
                if ttl <= 64:
                    return "Linux/macOS/FreeBSD (TTL ~64)"
                elif ttl <= 128:
                    return "Windows (TTL ~128)"
                else:
                    return "Network Device (TTL ~255)"
            return "Unknown"
        except:
            return "Unable to determine"

    def get_title(self):
        try:
            html = self._get_html()
            if html:
                soup = BeautifulSoup(html, 'lxml')
                title = soup.title.string if soup.title else None
                return title.strip() if title else None
            return None
        except:
            return None

    def get_description(self):
        try:
            html = self._get_html()
            if html:
                soup = BeautifulSoup(html, 'lxml')
                meta = soup.find('meta', attrs={'name': 'description'})
                return meta.get('content', None) if meta else None
            return None
        except:
            return None
