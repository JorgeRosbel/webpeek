#!/bin/bash
set -e

echo "========================================"
echo "  Webpeek Package Builder (Minimal)"
echo "========================================"

VERSION=$(python3 -c "import re; print(re.search(r\"version='([^']+)'\", open('setup.py').read()).group(1))")

echo "Building webpeek version $VERSION"

echo "Cleaning previous builds..."
rm -rf debian/webpeek
rm -f webpeek_${VERSION}_all.deb

echo "Creating minimal package structure..."
mkdir -p debian/webpeek/DEBIAN
mkdir -p debian/webpeek/usr/bin
mkdir -p debian/webpeek/usr/share/webpeek

echo "Creating installer script..."
cat > debian/webpeek/usr/bin/webpeek-install << 'EOFINSTALL'
#!/bin/bash
set -e

echo "========================================"
echo "  Webpeek Installer"
echo "========================================"

echo "Installing pipx..."
python3 -m pip install --user pipx

export PATH="$HOME/.local/bin:$PATH"

echo "Ensuring pipx paths..."
pipx ensurepath

echo "Installing webpeek from PyPI..."
pipx install webpeek || pipx install --force webpeek

echo ""
echo "========================================"
echo "  webpeek installed successfully!"
echo "========================================"
echo ""
echo "Run 'webpeek --help' to get started."
EOFINSTALL
chmod +x debian/webpeek/usr/bin/webpeek-install

echo "Creating uninstall script..."
cat > debian/webpeek/usr/bin/webpeek-uninstall << 'EOFUNINSTALL'
#!/bin/bash
set -e

export PATH="$HOME/.local/bin:$PATH"

echo "Uninstalling webpeek..."
pipx uninstall webpeek 2>/dev/null || true

echo "webpeek uninstalled."
EOFUNINSTALL
chmod +x debian/webpeek/usr/bin/webpeek-uninstall

echo "Creating control file..."
cat > debian/webpeek/DEBIAN/control << EOF
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

echo "Creating maintainer scripts..."
cat > debian/webpeek/DEBIAN/postinst << 'EOFPOSTINST'
#!/bin/bash
set -e

echo "Running webpeek installer..."
/usr/bin/webpeek-install
EOFPOSTINST
chmod +x debian/webpeek/DEBIAN/postinst

cat > debian/webpeek/DEBIAN/prerm << 'EOFPRERM'
#!/bin/bash
set -e

/usr/bin/webpeek-uninstall
EOFPRERM
chmod +x debian/webpeek/DEBIAN/prerm

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
