import requests


HEADERS_TO_CHECK = [
    'Strict-Transport-Security',
    'Content-Security-Policy',
    'X-Frame-Options',
    'X-Content-Type-Options',
    'Referrer-Policy',
    'Permissions-Policy'
]

REQUIRED_HEADERS = {
    'Strict-Transport-Security': 'HSTS - Enforces HTTPS',
    'Content-Security-Policy': 'CSP - Prevents XSS attacks',
    'X-Frame-Options': 'Prevents clickjacking',
    'X-Content-Type-Options': 'Prevents MIME sniffing',
    'Referrer-Policy': 'Controls referrer information',
    'Permissions-Policy': 'Controls browser features'
}


def get_security_headers(target):
    try:
        url = f"https://{target}" if not target.startswith('http') else target
        response = requests.head(url, timeout=10, verify=False, allow_redirects=True)
        headers = dict(response.headers)
        
        results = []
        missing = []
        
        for header in HEADERS_TO_CHECK:
            value = headers.get(header)
            if value:
                results.append(f"[PASS] {header}")
            else:
                results.append(f"[FAIL] {header}")
                missing.append(header)
        
        return results
    except Exception as e:
        return [f"Error: {str(e)[:50]}"]
