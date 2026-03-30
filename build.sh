#!/bin/bash
set -e

echo "========================================"
echo "  Webpeek Package Builder (pipx)"
echo "========================================"

VERSION=$(python3 -c "import re; print(re.search(r\"version='([^']+)'\", open('setup.py').read()).group(1))")

echo "Building webpeek version $VERSION"

echo "Cleaning previous builds..."
rm -rf debian/webpeek
rm -f webpeek_${VERSION}_all.deb
rm -rf /tmp/webpeek-pipx

echo "Creating pipx package structure..."
mkdir -p debian/webpeek/DEBIAN
mkdir -p debian/webpeek/usr/bin
mkdir -p debian/webpeek/usr/share/webpeek

echo "Creating installation script..."
cat > debian/webpeek/usr/share/webpeek/install.sh << 'EOFINSTALL'
#!/bin/bash
set -e

echo "Installing webpeek with pipx..."

# Install pipx if not present
if ! command -v pipx &> /dev/null; then
    echo "Installing pipx..."
    python3 -m pip install --user pipx
    export PATH="$HOME/.local/bin:$PATH"
    pipx ensurepath
fi

# Install webpeek using pipx
pipx install webpeek || pipx install --force webpeek

echo ""
echo "========================================"
echo "  webpeek installed successfully!"
echo "========================================"
echo ""
echo "Run 'webpeek --help' to get started."
EOFINSTALL
chmod +x debian/webpeek/usr/share/webpeek/install.sh

echo "Creating uninstall script..."
cat > debian/webpeek/usr/share/webpeek/uninstall.sh << 'EOFUNINSTALL'
#!/bin/bash
set -e

echo "Uninstalling webpeek..."
pipx uninstall webpeek 2>/dev/null || true

echo "webpeek uninstalled."
EOFUNINSTALL
chmod +x debian/webpeek/usr/share/webpeek/uninstall.sh

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
Depends: python3, python3-pip, python3-venv
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
echo "The package will automatically install webpeek using pipx."
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
