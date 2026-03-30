# Webpeek Agent Guidelines

This document provides guidelines for agents working on the webpeek codebase.

## Project Overview

Webpeek is an OSINT CLI tool for web reconnaissance that gathers both passive and active information about websites. It supports multiple scan modes (Active, Passive, Hybrid) and individual module flags.

## Build & Installation

```bash
# Install in development mode
cd /home/rosbel/personal/osint/webpeek
pip install -e .

# Run the CLI
webpeek <target> [options]

# Or run as Python module
python -m webpeek <target> [options]
```

## Development Commands

```bash
# Run a specific scan (test basic functionality)
python -m webpeek example.com --tech
python -m webpeek example.com --wplugins

# Full scan with all modules
python -m webpeek example.com -H

# Passive only scan
python -m webpeek example.com -P

# Active only scan  
python -m webpeek example.com -A

# Custom mode (specific modules only)
python -m webpeek example.com --whois --dns --ssl

# Save output to file
python -m webpeek example.com -H -oN output.txt

# Test WordPress detection (known WP sites)
python -m webpeek www.wpbeginner.com --wplugins --tech
python -m webpeek wordpress.org --wplugins
```

## Code Style Guidelines

### Imports

Organize imports in the following order:
1. Standard library imports
2. Third-party imports
3. Local application imports

```python
# Standard library
import re
import socket
import subprocess
from datetime import datetime

# Third-party
import requests
import dns.resolver
import whois
from bs4 import BeautifulSoup
from pwn import log

# Local
from webpeek.core.scanner import Scanner
from webpeek.utils.colors import Colors
```

### Naming Conventions

- **Classes**: `PascalCase` (e.g., `Scanner`, `Colors`)
- **Functions/methods**: `snake_case` (e.g., `get_ip()`, `whois_lookup()`)
- **Variables**: `snake_case` (e.g., `target`, `use_color`)
- **Constants**: `UPPER_SNAKE_CASE` (e.g., `ALL_ACTIVE_MODULES`)
- **Private methods**: prefix with `_` (e.g., `_log`)

### Functions

Keep functions focused and under 50 lines when possible. Each function should have a single responsibility.

```python
def get_ip(self):
    """Resolve domain to IP address."""
    if self.ip:
        return self.ip
    try:
        self.ip = socket.gethostbyname(self.target)
        return self.ip
    except socket.gaierror:
        return None
```

### Error Handling

- Use specific exception types instead of bare `except:`
- Return meaningful error messages or `None`/empty values
- Log errors when appropriate

```python
# Good
try:
    result = socket.gethostbyname(self.target)
    return result
except socket.gaierror:
    return None

# Avoid
try:
    result = socket.gethostbyname(self.target)
    return result
except:
    return None
```

### HTTP Requests

Always include User-Agent header and timeout:

```python
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
}
response = requests.get(url, headers=headers, timeout=10, verify=False)
```

### Return Values

- Use empty lists `[]` for no results (not `None`)
- Use meaningful strings for errors (e.g., `"Error: message"`)
- Return structured data (dicts, lists) for complex results

### CLI with Click

```python
@click.command()
@click.argument('target')
@click.option('-H', '--hybrid', 'hybrid_mode', is_flag=True)
@click.option('-A', '--active', is_flag=True)
@click.option('--module', is_flag=True, help='Module description')
def cli(target, hybrid_mode, active, module):
    # Implementation
    pass
```

### Output Formatting

When formatting lists in output:
- Use newlines with bullet points for lists: `"\n".join(f"  • {item}" for item in items)`
- Use dict format for versioned items: `f"{v['name']} ({v['version']})"`
- Truncate long values appropriately (see `output.py`)

### Type Hints (Optional but Recommended)

Add type hints for better code clarity:

```python
def get_ip(self) -> str | None:
    ...

def scan_passive(self, modules: list[str]) -> dict:
    ...
```

## File Structure

```
webpeek/
├── webpeek/
│   ├── cli.py              # CLI entry point
│   ├── core/
│   │   ├── scanner.py      # Main scanning logic
│   │   └── output.py      # Output formatting
│   ├── modules/
│   │   ├── tech.py        # Technology detection + WP plugins
│   │   ├── emails.py      # Email/phone extraction
│   │   ├── geo.py         # Geolocation
│   │   ├── headers.py     # HTTP headers
│   │   ├── security_headers.py
│   │   ├── ssl_info.py    # SSL certificate info
│   │   ├── subdomains.py  # Passive subdomain enumeration
│   │   ├── robots.py      # Robots.txt
│   │   ├── sitemap.py     # Sitemap extraction
│   │   └── wplugins.py    # WordPress plugins
│   └── utils/
│       └── colors.py      # Terminal colors
├── setup.py
└── README.md
```

## Testing

There are no formal tests. Test functionality manually:

1. Test with valid domains
2. Test edge cases (invalid domains, timeouts)
3. Test WordPress detection on known WP sites (wpbeginner.com, wordpress.org)
4. Test all CLI flags work correctly
5. Test output formatting with `-oN` flag

## Common Issues

- **SSL warnings**: Use `verify=False` and suppress warnings with `warnings.filterwarnings('ignore')`
- **Timeout handling**: Always set timeouts on network requests
- **Module imports**: Import modules inside functions when needed to avoid circular imports
