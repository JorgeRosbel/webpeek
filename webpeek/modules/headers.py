import requests


def get_headers(target):
    try:
        r = requests.head(f"http://{target}", timeout=10, verify=False, allow_redirects=True)
        headers = dict(r.headers)
        important = ['Server', 'X-Powered-By', 'Content-Type', 'Content-Length', 'Set-Cookie', 'Cache-Control', 'ETag']
        result = []
        for key in important:
            if key in headers:
                result.append(f"{key}: {headers[key]}")
        return result if result else []
    except Exception as e:
        return []
