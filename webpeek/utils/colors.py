from colorama import Fore, Style, init
from webpeek import __version__

init(autoreset=True)

C = Fore
S = Style

RESET = S.RESET_ALL
BOLD = S.BRIGHT


class Colors:
    CYAN = C.CYAN
    GREEN = C.GREEN
    YELLOW = C.YELLOW
    RED = C.RED
    BLUE = C.BLUE
    MAGENTA = C.MAGENTA
    WHITE = C.WHITE
    GREY = C.LIGHTBLACK_EX

    @staticmethod
    def section(title):
        return f"{BOLD}{Colors.CYAN}{title}{RESET}"

    @staticmethod
    def label(text):
        return f"{BOLD}{Colors.WHITE}{text}{RESET}"

    @staticmethod
    def value(text):
        return f"{Colors.GREEN}{text}{RESET}"

    @staticmethod
    def warning(text):
        return f"{Colors.YELLOW}{text}{RESET}"

    @staticmethod
    def error(text):
        return f"{Colors.RED}{text}{RESET}"

    @staticmethod
    def pass_(text):
        return f"{Colors.GREEN}[PASS] {text}{RESET}"

    @staticmethod
    def fail(text):
        return f"{Colors.RED}[FAIL] {text}{RESET}"

    @staticmethod
    def progress(text):
        return f"{Colors.GREY}[?] {text}...{RESET}"

    @staticmethod
    def progress_done(text):
        return f"{Colors.GREY}[?] {text}... {Colors.GREEN}✓{RESET}"

    @staticmethod
    def progress_skip(text):
        return f"{Colors.GREY}[?] {text}... {Colors.YELLOW}SKIP{RESET}"


def format_output(target, data, use_color=True, is_custom=False):
    if not use_color:
        return format_plain(target, data)

    sections = {
        'PASSIVE': [],
        'ACTIVE': []
    }

    passive_keys = ['WHOIS', 'Registrar', 'Expiration', 'Creation', 'DNS', 'MX', 'TXT', 'SPF', 'DKIM', 'DMARC', 'Subdomains']
    active_keys = ['IP', 'OS', 'Geo', 'Country', 'City', 'ISP', 'Headers', 'Security Headers', 'Technologies', 'WordPress Plugins', 'SSL', 'Title', 'Description', 'Sitemap', 'Robots', 'Social']

    for key, value in data.items():
        if value is None:
            continue
        if isinstance(value, str) and not value:
            continue
        if isinstance(value, list) and len(value) == 0:
            continue
        if isinstance(value, dict) and len(value) == 0:
            continue
        section = 'PASSIVE' if any(k in key for k in passive_keys) else 'ACTIVE'
        sections[section].append((key, value))

    output = []
    
    output.append(f"{BOLD}{Colors.CYAN}╔{'═'*56}╗{RESET}")
    output.append(f"{BOLD}{Colors.CYAN}║{RESET}  🌐 {BOLD}{Colors.WHITE}WEBPEEK{RESET} v{__version__} - {Colors.GREEN}{target}{RESET}" + " " * (23 - len(target)) + f"{BOLD}{Colors.CYAN}║{RESET}")
    output.append(f"{BOLD}{Colors.CYAN}╚{'═'*56}╝{RESET}")
    output.append("")

    if sections['PASSIVE']:
        mode_name = "CUSTOM MODE" if is_custom else "PASSIVE MODE"
        mode_icon = "🎯" if is_custom else "📡"
        output.append(f"{BOLD}{Colors.MAGENTA}  {mode_icon} {mode_name}{RESET}")
        output.append(f"{BOLD}{Colors.MAGENTA}  {'─'*20}{RESET}")
        for key, value in sections['PASSIVE']:
            output.append(f"  {Colors.label('◉ ' + key + ':')}")
            if isinstance(value, list):
                for v in value[:8]:
                    output.append(f"      {Colors.value('└─ ' + str(v))}")
                if len(value) > 8:
                    output.append(f"      {Colors.warning('└─ ... and ' + str(len(value) - 8) + ' more')}")
            elif '\n' in str(value):
                for line in str(value).split('\n'):
                    output.append(f"      {Colors.value(line)}")
            else:
                output.append(f"      {Colors.value(str(value))}")
            output.append("")
        output.append(f"{Colors.GREY}  {'─'*20}{RESET}")
        output.append("")

    if sections['ACTIVE']:
        mode_name = "CUSTOM MODE" if is_custom else "ACTIVE MODE"
        mode_icon = "⚡" if not is_custom else "🎯"
        output.append(f"{BOLD}{Colors.BLUE}  {mode_icon} {mode_name}{RESET}")
        output.append(f"{BOLD}{Colors.BLUE}  {'─'*20}{RESET}")
        for key, value in sections['ACTIVE']:
            output.append(f"  {Colors.label('◉ ' + key + ':')}")
            
            if key == 'Robots' and isinstance(value, dict):
                if value.get('disallow'):
                    output.append(f"      {Colors.error('[🔒] Private (Disallow):')}")
                    for v in value['disallow'][:8]:
                        output.append(f"          {Colors.warning('└─ ' + v)}")
                if value.get('allow'):
                    output.append(f"      {Colors.GREEN}[🔓] Allowed:{RESET}")
                    for v in value['allow'][:5]:
                        output.append(f"          {Colors.value('└─ ' + v)}")
                if not value.get('disallow') and not value.get('allow'):
                    output.append(f"      {Colors.warning('Not found')}")
            elif key == 'Exposed Files':
                for v in value[:15]:
                    output.append(f"      {Colors.value(str(v))}")
            elif isinstance(value, dict):
                for k, v in value.items():
                    if isinstance(v, list):
                        urls = ', '.join(v[:2])
                        output.append(f"      {Colors.label('• ' + k + ':')} {Colors.value(urls)}")
                    else:
                        output.append(f"      {Colors.label('• ' + k + ':')} {Colors.value(str(v))}")
            elif isinstance(value, list):
                for v in value[:8]:
                    output.append(f"      {Colors.value('└─ ' + str(v))}")
                if len(value) > 8:
                    output.append(f"      {Colors.warning('└─ ... and ' + str(len(value) - 8) + ' more')}")
            elif '\n' in str(value):
                for line in str(value).split('\n'):
                    output.append(f"      {Colors.value(line)}")
            else:
                output.append(f"      {Colors.value(str(value))}")
            output.append("")

    output.append(f"{BOLD}{Colors.CYAN}╔{'═'*56}╗{RESET}")
    output.append(f"{BOLD}{Colors.CYAN}║{RESET}  {Colors.GREEN}Scan complete!{RESET}" + " " * 35 + f"{BOLD}{Colors.CYAN}║{RESET}")
    output.append(f"{BOLD}{Colors.CYAN}╚{'═'*56}╝{RESET}")

    return "\n".join(output)


def format_plain(target, data):
    lines = []
    lines.append(f"{'='*60}")
    lines.append(f"WEBPEEK REPORT - {target}")
    lines.append(f"{'='*60}")
    lines.append("")

    passive_keys = ['WHOIS', 'Registrar', 'Expiration', 'Creation', 'DNS', 'MX', 'TXT', 'SPF', 'DKIM', 'DMARC', 'Subdomains']

    lines.append("[PASSIVE MODE]")
    for key, value in data.items():
        if value and any(k in key for k in passive_keys):
            if isinstance(value, dict):
                for k, v in value.items():
                    if isinstance(v, list):
                        lines.append(f"  {k}:")
                        for item in v:
                            lines.append(f"    - {item}")
                    else:
                        lines.append(f"  {k}: {v}")
            elif isinstance(value, list):
                lines.append(f"  {key}:")
                for v in value:
                    lines.append(f"    - {v}")
            else:
                lines.append(f"  {key}: {value}")

    lines.append("")
    lines.append("[ACTIVE MODE]")
    for key, value in data.items():
        if value and not any(k in key for k in passive_keys):
            if isinstance(value, dict):
                if key == 'Robots':
                    if value.get('disallow'):
                        lines.append(f"  {key}:")
                        lines.append(f"    [Private (Disallow)]:")
                        for item in value['disallow']:
                            lines.append(f"      - {item}")
                    if value.get('allow'):
                        lines.append(f"    [Allowed]:")
                        for item in value['allow']:
                            lines.append(f"      - {item}")
                else:
                    lines.append(f"  {key}:")
                    for k, v in value.items():
                        if isinstance(v, list):
                            urls = ', '.join(v[:2])
                            lines.append(f"    - {k}: {urls}")
                        else:
                            lines.append(f"    - {k}: {v}")
            elif isinstance(value, list):
                lines.append(f"  {key}:")
                for v in value:
                    lines.append(f"    - {v}")
            else:
                lines.append(f"  {key}: {value}")

    lines.append(f"{'='*60}")
    return "\n".join(lines)


def print_progress(message):
    print(f"{Colors.progress(message)}", end='\r')


def print_progress_done(message):
    print(f"{Colors.progress_done(message)}")


def print_progress_skip(message):
    print(f"{Colors.progress_skip(message)}")
