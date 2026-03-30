# webpeek

OSINT CLI tool for web reconnaissance - gather passive and active information about websites.

## Installation

### From PyPI (recommended when published)
```bash
pip install webpeek
```

### From GitHub
```bash
pip install git+https://github.com/JorgeRosbel/webpeek.git
```

### Local development
```bash
git clone https://github.com/JorgeRosbel/webpeek.git
cd webpeek
pip install -e .
```

## Usage

```bash
# Basic scan
webpeek example.com

# Hybrid mode (active + passive)
webpeek example.com -H

# Passive only
webpeek example.com -P

# Active only
webpeek example.com -A

# Dynamic mode (for JavaScript sites)
webpeek example.com -H -y

# Specific modules
webpeek example.com -T -l -e -p

# Save to file
webpeek example.com -H -oN result.txt

# Without colors
webpeek example.com -C

# Help
webpeek --help
```

## Options

| Short | Flag | Description |
|-------|------|-------------|
| `-H` | `--hybrid` | Run both active and passive modules |
| `-A` | `--active` | Run all active modules |
| `-P` | `--passive` | Run all passive modules |
| `-y` | `--dynamic` | Use headless browser (Playwright) |
| `-oN` | `--output` | Save output to file |
| `-C` | `--no-color` | Disable colors |
| `-v` | `--verbose` | Verbose output |

---

## Passive Modules

Gather information from public sources without connecting directly to the target.

| Short | Flag | Description |
|-------|------|-------------|
| `-w` | `--whois` | Domain registration info |
| `-d` | `--dns` | DNS A records |
| `-m` | `--mx` | MX records |
| `-t` | `--txt` | TXT records (SPF, DKIM) |
| `-S` | `--subdomains` | Find subdomains |

---

## Active Modules

Gather information by connecting directly to the target.

| Short | Flag | Description |
|-------|------|-------------|
| `-h` | `--headers` | HTTP headers |
| `-c` | `--security` | Security headers |
| `-T` | `--tech` | Detect technologies |
| `-W` | `--wplugins` | WordPress plugins |
| `-s` | `--ssl` | SSL certificate info |
| `-g` | `--geo` | Geolocation |
| `-O` | `--os` | OS detection |
| `-i` | `--title` | Page title |
| `-D` | `--description` | Meta description |
| `-e` | `--emails` | Extract emails |
| `-p` | `--phones` | Extract phone numbers |
| `-M` | `--sitemap` | Sitemap URLs |
| `-r` | `--robots` | Robots.txt |
| `-l` | `--social` | Social networks |

---

## Dynamic Mode

Use `-y` for JavaScript-rendered sites (React, Vue, Angular, etc.):

```bash
webpeek example.com -T -y
```

First time using dynamic mode will download Chromium (~150MB).

---

## Example Output

```
╔════════════════════════════════════════════════════════╗
║  🌐 WEBPEEK v1.3.0 - example.com                  ║
╚════════════════════════════════════════════════════════╝

  📡 PASSIVE MODE
  ─────────────────────
  ◉ WHOIS:
      └─ Registrar: NameCheap, Inc.
      └─ Created: 2025-12-14
      └─ Expires: 2026-12-14

  ◉ DNS:
      └─ 93.184.216.34

  ⚡ ACTIVE MODE
  ─────────────────────
  ◉ IP:
      └─ 93.184.216.34

  ◉ Geo:
      └─ US, California (Cloudflare, Inc.)

  ◉ Technologies:
      └─ Cloudflare
      └─ Nginx

  ◉ SSL:
      └─ example.com (expires in 90 days)

╔════════════════════════════════════════════════════════╗
║  Scan complete!                                  ║
╚════════════════════════════════════════════════════════╝
```

---

## Uninstall

```bash
pip uninstall webpeek
```

## License

MIT
