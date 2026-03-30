import click
import tldextract
import socket
import re
from pwn import log
from webpeek.core.scanner import Scanner
from webpeek.core.output import print_results, save_to_file
from webpeek.utils.colors import Colors, RESET


def is_valid_domain(domain):
    pattern = r'^(?:[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,}$'
    return bool(re.match(pattern, domain))


def validate_target(target):
    ext = tldextract.extract(target)
    if not ext.domain or not ext.suffix:
        return None
    
    domain = f"{ext.domain}.{ext.suffix}"
    
    if not is_valid_domain(domain):
        return None
    
    try:
        socket.gethostbyname(domain)
        return domain
    except socket.gaierror:
        return None


ALL_ACTIVE_MODULES = ['headers', 'tech', 'ssl', 'geo', 'title', 'description', 'security', 'wplugins', 'sitemap', 'robots', 'social', 'os', 'emails', 'phones']
ALL_PASSIVE_MODULES = ['whois', 'dns', 'mx', 'txt', 'subdomains']


@click.command()
@click.argument('target')
@click.option('-H', '--hybrid', 'hybrid_mode', is_flag=True, help='Run both active and passive modules')
@click.option('-A', '--active', is_flag=True, help='Run all active modules')
@click.option('-P', '--passive', is_flag=True, help='Run all passive modules')
@click.option('-w', '--whois', is_flag=True, help='WHOIS lookup')
@click.option('-d', '--dns', is_flag=True, help='DNS lookup')
@click.option('-m', '--mx', is_flag=True, help='MX records')
@click.option('-t', '--txt', is_flag=True, help='TXT records (SPF, DKIM)')
@click.option('-h', '--headers', is_flag=True, help='HTTP headers')
@click.option('-T', '--tech', is_flag=True, help='Detect technologies')
@click.option('-s', '--ssl', is_flag=True, help='SSL certificate info')
@click.option('-g', '--geo', is_flag=True, help='Geolocation')
@click.option('-O', '--os', is_flag=True, help='OS detection via TTL')
@click.option('-i', '--title', is_flag=True, help='Page title')
@click.option('-D', '--description', 'desc', is_flag=True, help='Meta description')
@click.option('-e', '--emails', is_flag=True, help='Extract emails')
@click.option('-p', '--phones', is_flag=True, help='Extract phone numbers')
@click.option('-S', '--subdomains', is_flag=True, help='Find subdomains')
@click.option('-c', '--security', is_flag=True, help='Security headers audit')
@click.option('-W', '--wplugins', is_flag=True, help='WordPress plugins')
@click.option('-M', '--sitemap', is_flag=True, help='Extract URLs from sitemap')
@click.option('-r', '--robots', is_flag=True, help='Fetch robots.txt')
@click.option('-l', '--social', is_flag=True, help='Social networks')
@click.option('-y', '--dynamic', is_flag=True, help='Use headless browser (Playwright) for dynamic content')
@click.option('-oN', '--output', type=click.Path(), help='Save output to file')
@click.option('-C', '--no-color', is_flag=True, help='Disable colors')
@click.option('-v', '--verbose', is_flag=True, help='Verbose output')
def cli(target, hybrid_mode, active, passive, whois, dns, mx, txt, headers, tech, ssl, geo, os, title, desc, emails, phones, subdomains, security, wplugins, sitemap, robots, social, dynamic, output, no_color, verbose):
    use_color = not no_color
    
    domain = validate_target(target)
    if not domain:
        print(f"{Colors.error('[ERROR] Invalid domain: ' + target)}")
        return
    
    scanner = Scanner(domain, verbose, use_color, dynamic)
    
    active_modules = []
    passive_modules = []
    
    specific_flags = [whois, dns, mx, txt, subdomains, headers, tech, ssl, geo, os, title, desc, emails, phones, security, wplugins, sitemap, robots, social]
    is_custom = any(specific_flags) and not hybrid_mode and not active and not passive
    
    if hybrid_mode:
        active_modules = ALL_ACTIVE_MODULES.copy()
        passive_modules = ALL_PASSIVE_MODULES.copy()
    elif active:
        active_modules = ALL_ACTIVE_MODULES.copy()
    elif passive:
        passive_modules = ALL_PASSIVE_MODULES.copy()
    elif any(specific_flags):
        active_modules = []
        passive_modules = []
    else:
        active_modules = ALL_ACTIVE_MODULES.copy()
        passive_modules = ALL_PASSIVE_MODULES.copy()
    
    if whois: passive_modules.append('whois')
    if dns: passive_modules.append('dns')
    if mx: passive_modules.append('mx')
    if txt: passive_modules.append('txt')
    if subdomains: passive_modules.append('subdomains')
    if emails: active_modules.append('emails')
    if phones: active_modules.append('phones')
    if headers: active_modules.append('headers')
    if tech: active_modules.append('tech')
    if ssl: active_modules.append('ssl')
    if geo: active_modules.append('geo')
    if os: active_modules.append('os')
    if title: active_modules.append('title')
    if desc: active_modules.append('description')
    if security: active_modules.append('security')
    if wplugins: active_modules.append('wplugins')
    if sitemap: active_modules.append('sitemap')
    if robots: active_modules.append('robots')
    if social: active_modules.append('social')
    
    active_modules = list(set(active_modules))
    passive_modules = list(set(passive_modules))
    
    results = {}
    
    if passive_modules:
        results.update(scanner.scan_passive(passive_modules))
    
    if active_modules:
        results.update(scanner.scan_active(active_modules))
    
    print_results(domain, results, use_color, is_custom)
    
    if output:
        from webpeek.utils.colors import format_plain
        plain_output = format_plain(domain, results)
        
        if save_to_file(output, plain_output):
            if use_color:
                click.echo(f"{Colors.pass_('Results saved to ' + output)}")
            else:
                click.echo(f"Results saved to {output}")


if __name__ == '__main__':
    cli()
