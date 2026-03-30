#!/bin/bash
set -e

echo "========================================"
echo "  Webpeek Package Builder"
echo "========================================"

VERSION=$(python3 -c "import re; print(re.search(r\"version='([^']+)'\", open('setup.py').read()).group(1))")

echo "Building webpeek version $VERSION"

echo "Cleaning previous builds..."
rm -rf debian/webpeek-package
rm -f webpeek_${VERSION}_all.deb

echo "Creating package structure..."
mkdir -p debian/webpeek-package/DEBIAN
mkdir -p debian/webpeek-package/usr/local/bin
mkdir -p debian/webpeek-package/usr/share/webpeek

echo "Creating installer script..."
cat > debian/webpeek-package/usr/local/bin/webpeek << 'EOFINSTALL'
#!/bin/bash

REPO_URL="https://github.com/JorgeRosbel/webpeek"
INSTALL_DIR="/usr/share/webpeek"
BIN_LINK="/usr/local/bin/webpeek"

echo "========================================"
echo "  Webpeek Installer"
echo "========================================"

# Check if already installed
if [ -f "$BIN_LINK" ] && [ -d "$INSTALL_DIR" ]; then
    echo "webpeek is already installed!"
    exec "$BIN_LINK" "$@"
fi

# Create install directory
mkdir -p "$INSTALL_DIR"

# Clone or download repository
echo "Downloading webpeek..."
if command -v git &> /dev/null; then
    if [ -d "$INSTALL_DIR/.git" ]; then
        cd "$INSTALL_DIR" && git pull
    else
        git clone --depth 1 "$REPO_URL" "$INSTALL_DIR"
    fi
else
    # Fallback: download as zip
    curl -sL "$REPO_URL/archive/refs/heads/main.zip" -o /tmp/webpeek.zip
    unzip -q /tmp/webpeek.zip -d /tmp/
    mv /tmp/webpeek-main/* "$INSTALL_DIR/"
    rm -rf /tmp/webpeek.zip /tmp/webpeek-main
fi

# Install dependencies
echo "Installing dependencies..."
pip3 install --break-system-packages click requests dnspython whois beautifulsoup4 lxml colorama tldextract pwntools playwright pyee greenlet 2>/dev/null || \
pip3 install click requests dnspython whois beautifulsoup4 lxml colorama tldextract pwntools playwright pyee greenlet

# Create launcher
cat > "$BIN_LINK" << 'EOFLAUNCHER'
#!/bin/bash
/usr/bin/python3 -c "
import sys
sys.path.insert(0, '/usr/share/webpeek')
from webpeek.cli import cli
sys.exit(cli())
"
EOFLAUNCHER

chmod +x "$BIN_LINK"

# Install Playwright browser
echo "Installing Playwright browser..."
playwright install chromium --with-deps 2>/dev/null || true

echo ""
echo "========================================"
echo "  webpeek installed successfully!"
echo "========================================"
echo ""
echo "Run 'webpeek --help' to get started."
EOFINSTALL
chmod +x debian/webpeek-package/usr/local/bin/webpeek

echo "Creating control file..."
cat > debian/webpeek-package/DEBIAN/control << EOF
Package: webpeek
Version: $VERSION
Section: utils
Priority: optional
Architecture: all
Depends: python3, python3-pip
Maintainer: JorgeRosbel <jorge@rosbel.dev>
Description: OSINT CLI tool for web reconnaissance
 webpeek gathers both passive and active information about websites,
 including WHOIS, DNS, technologies, social networks, and more.
 Supports dynamic scanning with Playwright for JavaScript-rendered sites.
EOF

echo "Building .deb package..."
dpkg-deb --build --root-owner-group debian/webpeek-package webpeek_${VERSION}_all.deb

echo ""
echo "========================================"
echo "  Package built successfully!"
echo "========================================"
echo ""
echo "Output: webpeek_${VERSION}_all.deb"
echo "Size: $(du -h webpeek_${VERSION}_all.deb | cut -f1)"
echo ""
echo "To install:"
echo "  sudo apt install ./webpeek_${VERSION}_all.deb"
echo ""
