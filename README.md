# webpeek

OSINT CLI tool for web reconnaissance - gather passive and active information about websites.

## Installation

### From source
```bash
git clone https://github.com/yourusername/webpeek.git
cd webpeek
pip install -e .
```

### Create .deb package
```bash
pip install stdeb
python setup.py sdist
python setup.py --command-packages=stdeb.command bdist_deb
sudo apt install ./deb_dist/webpeek_1.0.0_all.deb
```

## Usage

```bash
# Full scan (all passive + active) - DEFAULT
webpeek example.com

# Hybrid mode (both active and passive)
webpeek example.com -H

# Passive only
webpeek example.com -P

# Active only
webpeek example.com -A

# Specific modules
webpeek example.com --whois --dns --headers --ssl

# Save to file
webpeek example.com -oN result.txt

# Without colors
webpeek example.com --no-color

# Help
webpeek --help
```

---

## Passive Modules

Gather information from public sources without connecting directly to the target.

| Short | Flag | Description |
|-------|------|-------------|
| `-w` | `--whois` | Domain registration info (registrar, creation, expiration) |
| `-d` | `--dns` | DNS A records |
| `-m` | `--mx` | Mail exchange (MX) records |
| `-t` | `--txt` | TXT records (SPF, DKIM) |
| `-S` | `--subdomains` | Subdomains via crt.sh, HackerTarget, AlienVault |

---

## Active Modules

Gather information by connecting directly to the target.

| Short | Flag | Description |
|-------|------|-------------|
| `-h` | `--headers` | HTTP response headers |
| `-c` | `--security` | Security headers audit (HSTS, CSP, X-Frame-Options, etc.) |
| `-T` | `--tech` | Detect web technologies (Astro, WordPress, React, etc.) |
| `-W` | `--wplugins` | WordPress plugins detected |
| `-s` | `--ssl` | SSL certificate info and expiration |
| `-g` | `--geo` | Geolocation (country, city, ISP) |
| `-O` | `--os` | OS detection via TTL |
| `-i` | `--title` | Page title |
| `-D` | `--description` | Meta description |
| `-e` | `--emails` | Email addresses found on the site |
| `-p` | `--phones` | Phone numbers found on the site (with country detection) |
| `-M` | `--sitemap` | URLs from sitemap.xml |
| `-r` | `--robots` | robots.txt content |

---

## Options

| Short | Flag | Description |
|-------|------|-------------|
| `-H` | `--hybrid` | Run both active and passive modules |
| `-A` | `--active` | Run all active modules |
| `-P` | `--passive` | Run all passive modules |
| `-oN` | `--output` | Save output to file |
| `-C` | `--no-color` | Disable colors |
| `-v` | `--verbose` | Verbose output |

---

## Examples

```bash
# Full scan (all passive + active) - DEFAULT
webpeek example.com

# Using short flags
webpeek example.com -H
webpeek example.com -P
webpeek example.com -A

# Specific modules with short flags
webpeek example.com -w -d -h -s

# Mixed short and long flags
webpeek example.com --whois --dns -h --ssl

# Save output to file
webpeek example.com -H -oN result.txt

# Without colors
webpeek example.com -C

# Help
webpeek --help
```

---

## Example Output

```
╔════════════════════════════════════════════════════════╗
║  🌐 WEBPEEK - example.com                             ║
╚════════════════════════════════════════════════════════╝

  📡 PASSIVE MODE
  ─────────────────────
  ◉ WHOIS:
      └─ Registrar: NameCheap, Inc.
      └─ Created: 2025-12-14
      └─ Expires: 2026-12-14

  ◉ DNS:
      └─ 93.184.216.34

  ◉ MX:
      └─ 10 mx1.example.com.
      └─ 20 mx2.example.com.

  ◉ TXT:
      └─ SPF: Found
      └─ v=spf1 include:_spf.mail.example.com ~all

  ─────────────────────

  ⚡ ACTIVE MODE
  ─────────────────────
  ◉ IP:
      └─ 93.184.216.34

  ◉ Geo:
      └─ US, California (Cloudflare, Inc.)

  ◉ OS:
      └─ Linux/macOS/FreeBSD (TTL ~64)

  ◉ Headers:
      └─ Server: cloudflare

  ◉ Security Headers:
      └─ [PASS] Content-Security-Policy
      └─ [FAIL] Strict-Transport-Security
      └─ [FAIL] X-Frame-Options

  ◉ Technologies:
      └─ Cloudflare
      └─ Nginx

  ◉ SSL:
      └─ example.com (expires in 90 days)

  ◉ Title:
      └─ Example Domain

╔════════════════════════════════════════════════════════╗
║  Scan complete!                                       ║
╚════════════════════════════════════════════════════════╝
```

## License

MIT
