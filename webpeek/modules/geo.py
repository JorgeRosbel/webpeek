import requests


def get_geo(ip):
    try:
        r = requests.get(f"http://ip-api.com/json/{ip}?fields=status,country,city,isp,query", timeout=10)
        if r.json().get('status') == 'success':
            data = r.json()
            return f"{data.get('country', 'N/A')}, {data.get('city', 'N/A')} ({data.get('isp', 'N/A')})"
        return "N/A"
    except Exception as e:
        return f"Error: {str(e)[:40]}"
