#!/bin/sh

# Abort script on error
set -e

# Temp file
TMP_FILE="/tmp/quickfetch.bin.$$"

# Cleanup on exit
cleanup() {
    if [ -f "$TMP_FILE" ]; then
        rm -f "$TMP_FILE"
    fi
}
trap cleanup EXIT

# Function to check root
check_root() {
    USER_ID=`id -u`
    if [ "$USER_ID" -ne 0 ]; then
        echo "Error: This script must be run as root. Please use sudo." >&2
        exit 1
    fi
}

# Function to detect architecture
detect_arch() {
    ARCH_RAW=`uname -m`
    case "$ARCH_RAW" in
        aarch64|arm64)
            echo "arm64"
            ;;
        x86_64|amd64)
            echo "amd64"
            ;;
        i386|i686)
            echo "386"
            ;;
        *)
            echo "unknown"
            ;;
    esac
}

# Function to download binary
download_binary() {
    ARCH="$1"
    BASE_URL="https://github.com/master2619/quickfetch/releases/download/release-3"

    if [ "$ARCH" = "arm64" ]; then
        BINARY_URL="$BASE_URL/quickfetch-arm64"
    else
        BINARY_URL="$BASE_URL/quickfetch"
    fi

    echo "Downloading binary for architecture: $ARCH"
    echo "Source URL: $BINARY_URL"

    curl -fsSL "$BINARY_URL" -o "$TMP_FILE" || {
        echo "Download failed. Please check your internet connection or the release URL."
        exit 1
    }

    if [ ! -s "$TMP_FILE" ]; then
        echo "Downloaded file is empty. Aborting."
        exit 1
    fi
}

# Function to install binary
install_binary() {
    DEST="/usr/bin/quickfetch"

    echo "Installing QuickFetch to $DEST..."
    mv "$TMP_FILE" "$DEST"
    chmod +x "$DEST"

    if [ ! -x "$DEST" ]; then
        echo "Installation failed. File does not exist or is not executable."
        exit 1
    fi

    echo "QuickFetch installed successfully."
    echo "Run it using: quickfetch"
}

### MAIN EXECUTION FLOW ###
check_root

ARCH_DETECTED=`detect_arch`

if [ "$ARCH_DETECTED" = "unknown" ]; then
    echo "Unsupported architecture: `uname -m`"
    exit 1
fi

download_binary "$ARCH_DETECTED"
install_binary

exit 0
