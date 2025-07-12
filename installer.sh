#!/bin/sh

# Ensure root
if [ "$(id -u)" -ne 0 ]; then
    echo "This script must be run as root. Please use sudo."
    exit 1
fi

# Detect architecture and set binary
ARCH=`uname -m`
BINARY_NAME="quickfetch"

if [ "$ARCH" = "aarch64" ] || [ "$ARCH" = "arm64" ]; then
    BINARY_NAME="quickfetch-arm64"
fi

# Set paths
REPO_URL="https://github.com/master2619/quickfetch/releases/download/release-3"
DOWNLOAD_URL="$REPO_URL/$BINARY_NAME"
DEST_PATH="/usr/bin/quickfetch"

# Download binary
echo "Downloading $BINARY_NAME from $DOWNLOAD_URL..."
curl -fsSL "$DOWNLOAD_URL" -o /tmp/quickfetch.tmp

if [ $? -ne 0 ] || [ ! -s /tmp/quickfetch.tmp ]; then
    echo "Download failed. Please check the URL or network connection."
    exit 1
fi

# Move to /usr/bin and rename
mv /tmp/quickfetch.tmp "$DEST_PATH"
chmod +x "$DEST_PATH"

# Verify install
if [ -x "$DEST_PATH" ]; then
    echo "QuickFetch installed successfully at $DEST_PATH"
    echo "You can run it by typing: quickfetch"
    exit 0
else
    echo "Installation failed."
    exit 1
fi
