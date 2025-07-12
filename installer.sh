#!/bin/sh
# installer.sh — QuickFetch installer (POSIX sh compatible)

# Must run as root
if [ "$(id -u)" != "0" ]; then
    echo "This script must be run as root. Please use sudo."
    exit 1
fi

# Detect architecture
ARCH=$(uname -m)
case "$ARCH" in
    aarch64|arm64)
        BINARY_NAME="quickfetch-arm64"
        ;;
    *)
        BINARY_NAME="quickfetch"
        ;;
esac

# Set URLs and paths
REPO_BASE="https://github.com/master2619/quickfetch/releases/download/release-3"
DOWNLOAD_URL="$REPO_BASE/$BINARY_NAME"
DEST_PATH="/usr/bin/quickfetch"
TMP_PATH="/tmp/quickfetch.download"

# Download the appropriate binary
echo "Detected architecture: $ARCH"
echo "Downloading $BINARY_NAME from $DOWNLOAD_URL..."
curl -fsSL "$DOWNLOAD_URL" -o "$TMP_PATH"
if [ $? -ne 0 ] || [ ! -s "$TMP_PATH" ]; then
    echo "Error: failed to download $DOWNLOAD_URL"
    exit 1
fi

# Install the binary
echo "Installing to $DEST_PATH..."
mv "$TMP_PATH" "$DEST_PATH" || {
    echo "Error: failed to move file to $DEST_PATH"
    exit 1
}
chmod +x "$DEST_PATH"

# Verify installation
if [ -x "$DEST_PATH" ]; then
    echo "✔ QuickFetch installed at $DEST_PATH"
    echo "Run it with: quickfetch"
    exit 0
else
    echo "✖ Installation failed."
    exit 1
fi
