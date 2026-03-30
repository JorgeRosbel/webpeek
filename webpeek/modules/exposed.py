import requests


EXPOSED_PATHS = [
    '/.env', '/.env.local', '/.env.prod', '/.env.dev', '/.env.bak',
    '/.aws/credentials', '/.vscode/sftp.json', '/.ssh/id_rsa',
    '/.git/config', '/.git/index', '/.gitignore', '/.svn/entries',
    '/wp-config.php.bak', '/wp-config.php.old', '/wp-config.php.save', '/wp-config.php~',
    '/wp-content/debug.log', '/wp-content/uploads/debug.log',
    '/wp-json/wp/v2/users', '/wp-links-opml.php', '/xmlrpc.php',
    '/backup.sql', '/db.sql', '/db_backup.sql', '/database.sql', '/dump.sql',
    '/db.zip', '/backup.zip', '/site.zip', '/www.zip', '/old.zip',
    '/latest.tar.gz', '/site.tar.gz', '/backup.tar.gz', '/full.sql',
    '/phpinfo.php', '/info.php', '/status', '/server-status',
    '/error_log', '/error.log', '/access.log', '/debug.log',
    '/.htaccess.bak', '/.htpasswd', '/web.config',
    '/package.json', '/composer.json', '/composer.lock',
    '/.npmrc', '/yarn.lock', '/docker-compose.yml',
    '/backup/', '/backups/', '/css/', '/js/', '/images/', '/uploads/',
    '/sql/', '/temp/', '/tmp/', '/old/',
    '/admin', '/wp-admin', '/phpmyadmin', '/administrator', '/login',
    '/wp-login.php', '/readme.html', '/readme.txt', '/license.txt',
    '/install.php', '/test/', '/api/',
]


def get_status_color(status):
    if status == 200:
        return 'green'
    elif status in [201, 204]:
        return 'green'
    elif status in [301, 302, 307, 308]:
        return 'yellow'
    elif status == 403:
        return 'red'
    elif status == 401:
        return 'red'
    elif status == 404:
        return 'grey'
    elif status >= 500:
        return 'red'
    return 'white'


def check_path(url, path):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
    }
    try:
        full_url = f"https://{url}{path}" if not url.startswith('http') else f"{url}{path}"
        response = requests.get(full_url, headers=headers, timeout=5, verify=False, allow_redirects=False)
        return {
            'path': path,
            'status': response.status_code,
            'color': get_status_color(response.status_code)
        }
    except:
        return None


def check_exposed(url):
    exposed = []
    for path in EXPOSED_PATHS:
        result = check_path(url, path)
        if result:
            exposed.append(result)
    return exposed[:25]
