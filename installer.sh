#!/bin/bash

# Ensure the script is run as root
if [ "$(id -u)" -ne 0 ]; then
    echo "This script must be run as root. Please use sudo."
    exit 1
fi

# Detect architecture
ARCH="$(uname -m)"
if [ "$ARCH" = "aarch64" ] || [ "$ARCH" = "arm64" ]; then
    BINARY_NAME="quickfetch-arm64"
else
    BINARY_NAME="quickfetch"
fi

# Set variables
REPO_BASE="https://github.com/master2619/quickfetch/releases/download/release-3"
DOWNLOAD_URL="$REPO_BASE/$BINARY_NAME"
DEST_PATH="/usr/bin/quickfetch"
TMP_PATH="/tmp/quickfetch.download"

# Download the appropriate binary
echo "Detected architecture: $ARCH"
echo "Downloading $BINARY_NAME from $DOWNLOAD_URL..."
curl -fsSL -o "$TMP_PATH" "$DOWNLOAD_URL"

# Check if the download was successful
if [ $? -ne 0 ] || [ ! -s "$TMP_PATH" ]; then
    echo "Error downloading the file. Please check the URL and try again."
    exit 1
fi

# Move the downloaded file to the destination, renaming it to 'quickfetch'
echo "Installing to $DEST_PATH..."
mv "$TMP_PATH" "$DEST_PATH"

# Make the binary executable
chmod +x "$DEST_PATH"

# Verify installation
if [ -f "$DEST_PATH" ]; then
    echo "QuickFetch has been successfully installed to $DEST_PATH."
else
    echo "Installation failed. Please check permissions and try again."
    exit 1
fi

echo "Installation complete. You can run QuickFetch by typing 'quickfetch' in the terminal."
exit 0
