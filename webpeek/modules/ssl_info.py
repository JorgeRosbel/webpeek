import socket
import ssl
from datetime import datetime


def get_ssl_info(target):
    try:
        hostname = target.split(':')[0] if ':' in target else target
        port = 443
        context = ssl.create_default_context()
        with socket.create_connection((hostname, port), timeout=10) as sock:
            with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                cert = ssock.getpeercert()
                issuer = dict(x[0] for x in cert['issuer'])
                common_name = dict(x[0] for x in cert['subject']).get('commonName', '')
                not_after = datetime.strptime(cert['notAfter'], '%b %d %H:%M:%S %Y %Z')
                days_left = (not_after - datetime.now()).days
                return f"{common_name} (expires in {days_left} days)"
    except Exception as e:
        return f"No SSL or error: {str(e)[:40]}"
