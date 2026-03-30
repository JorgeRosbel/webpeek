#!/bin/bash
set -e

echo "========================================"
echo "  Webpeek Package Builder (Minimal)"
echo "========================================"

VERSION=$(python3 -c "import re; print(re.search(r\"version='([^']+)'\", open('setup.py').read()).group(1))")

echo "Building webpeek version $VERSION"

echo "Cleaning previous builds..."
rm -rf debian/webpeek-package
rm -f webpeek_${VERSION}_all.deb

echo "Creating minimal package structure..."
mkdir -p debian/webpeek-package/DEBIAN
mkdir -p debian/webpeek-package/usr/bin

echo "Creating installer script..."
cat > debian/webpeek-package/usr/bin/webpeek-install << 'EOFINSTALL'
#!/bin/bash
set -e

echo "========================================"
echo "  Webpeek Installer"
echo "========================================"

echo "Installing pipx..."
python3 -m pip install --break-system-packages --user pipx

export PATH="$HOME/.local/bin:$PATH"

echo "Ensuring pipx paths..."
pipx ensurepath || true

echo "Installing webpeek from GitHub..."
pipx install --system https://github.com/JorgeRosbel/webpeek/archive/refs/heads/main.zip || pipx install --system --force https://github.com/JorgeRosbel/webpeek/archive/refs/heads/main.zip

echo "Creating symlink in /usr/local/bin..."
pipx run webpeek --version >/dev/null 2>&1 || true

WEBPEEK_PATH=$(find ~/.local -name "webpeek" -type f -executable 2>/dev/null | head -1)
if [ -z "$WEBPEEK_PATH" ]; then
    WEBPEEK_PATH=$(find /root -name "webpeek" -type f -executable 2>/dev/null | head -1)
fi

if [ -n "$WEBPEEK_PATH" ]; then
    ln -sf "$WEBPEEK_PATH" /usr/local/bin/webpeek 2>/dev/null || sudo ln -sf "$WEBPEEK_PATH" /usr/local/bin/webpeek
    echo "Created symlink: /usr/local/bin/webpeek -> $WEBPEEK_PATH"
fi

echo ""
echo "========================================"
echo "  webpeek installed successfully!"
echo "========================================"
echo ""
echo "Run 'webpeek --help' to get started."
EOFINSTALL
chmod +x debian/webpeek-package/usr/bin/webpeek-install

echo "Creating uninstall script..."
cat > debian/webpeek-package/usr/bin/webpeek-uninstall << 'EOFUNINSTALL'
#!/bin/bash
set -e

export PATH="$HOME/.local/bin:$PATH"

echo "Uninstalling webpeek..."
pipx uninstall webpeek 2>/dev/null || true

echo "webpeek uninstalled."
EOFUNINSTALL
chmod +x debian/webpeek-package/usr/bin/webpeek-uninstall

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

echo "Creating maintainer scripts..."
cat > debian/webpeek-package/DEBIAN/postinst << 'EOFPOSTINST'
#!/bin/bash
set -e
/usr/bin/webpeek-install || true
EOFPOSTINST
chmod +x debian/webpeek-package/DEBIAN/postinst

cat > debian/webpeek-package/DEBIAN/prerm << 'EOFPRERM'
#!/bin/bash
set -e
export PATH="$HOME/.local/bin:$PATH"
pipx uninstall webpeek 2>/dev/null || true
EOFPRERM
chmod +x debian/webpeek-package/DEBIAN/prerm

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
