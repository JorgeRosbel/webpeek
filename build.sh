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

echo "Installing pipx for current user..."
python3 -m pip install --user pipx

export PATH="$HOME/.local/bin:$PATH"

echo "Ensuring pipx paths..."
pipx ensurepath || true

# Get the actual user who ran sudo
TARGET_USER=${SUDO_USER:-$(whoami)}
TARGET_HOME=$(getent passwd "$TARGET_USER" | cut -d: -f6)

echo "Installing webpeek for user: $TARGET_USER..."
su - "$TARGET_USER" -c "export PATH=\"\$HOME/.local/bin:\$PATH\" && pipx install https://github.com/JorgeRosbel/webpeek/archive/refs/heads/main.zip" || true

# Create symlink accessible to all users
if [ -f "$TARGET_HOME/.local/share/pipx/venvs/webpeek/bin/webpeek" ]; then
    ln -sf "$TARGET_HOME/.local/share/pipx/venvs/webpeek/bin/webpeek" /usr/local/bin/webpeek
    chmod +x "$TARGET_HOME/.local/share/pipx/venvs/webpeek/bin/webpeek"
    echo "Created symlink in /usr/local/bin/webpeek"
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
