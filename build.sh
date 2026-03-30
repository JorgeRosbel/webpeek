#!/bin/bash
set -e

echo "========================================"
echo "  Webpeek Package Builder"
echo "========================================"

VERSION=$(python3 -c "import re; print(re.search(r\"version='([^']+)'\", open('setup.py').read()).group(1))")

echo "Building webpeek version $VERSION"

echo "Cleaning previous builds..."
rm -rf debian/webpeek
rm -f webpeek_${VERSION}_all.deb
rm -rf /tmp/webpeek-install

echo "Installing Python dependencies..."
python3 -m pip install --target=/tmp/webpeek-install \
    click requests dnspython whois beautifulsoup4 lxml colorama \
    tldextract pwntools playwright pyee greenlet setuptools

echo "Creating package structure..."
mkdir -p debian/webpeek/DEBIAN
mkdir -p debian/webpeek/usr/lib/python3/dist-packages
mkdir -p debian/webpeek/usr/bin

echo "Copying dependencies..."
cp -r /tmp/webpeek-install/* debian/webpeek/usr/lib/python3/dist-packages/ 2>/dev/null || true

echo "Copying webpeek..."
cp -r webpeek debian/webpeek/usr/lib/python3/dist-packages/

echo "Creating launcher script..."
cat > debian/webpeek/usr/bin/webpeek << 'EOF'
#!/usr/bin/python3
import sys
from webpeek.cli import cli
if __name__ == '__main__':
    sys.exit(cli())
EOF
chmod +x debian/webpeek/usr/bin/webpeek

echo "Copying postinst..."
cp debian/postinst debian/webpeek/DEBIAN/
chmod +x debian/webpeek/DEBIAN/postinst

echo "Creating control file..."
cat > debian/webpeek/DEBIAN/control << EOF
Package: webpeek
Version: $VERSION
Section: utils
Priority: optional
Architecture: all
Depends: python3, python3-click, python3-requests, python3-dnspython, python3-whois, python3-bs4, python3-lxml, python3-colorama, python3-tldextract, python3-pwntools, python3-pyee, python3-greenlet
Maintainer: JorgeRosbel <jorge@rosbel.dev>
Description: OSINT CLI tool for web reconnaissance
 webpeek gathers both passive and active information about websites,
 including WHOIS, DNS, technologies, social networks, and more.
 Supports dynamic scanning with Playwright for JavaScript-rendered sites.
EOF

echo "Building .deb package..."
dpkg-deb --build debian/webpeek webpeek_${VERSION}_all.deb

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
