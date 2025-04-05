#!/bin/bash

set -e

REPO_URL="https://github.com/alisharify7/AutoDeskID"
ZIP_URL="$REPO_URL/archive/refs/heads/main.zip"
TMP_DIR="/tmp/autodeskid"
INSTALL_DIR="$HOME/AutoDeskID"
SERVICE_DIR="/etc/systemd/system/"
SERVICE_NAME="autodeskid"

echo "🚀 Downloading AutoDeskID from GitHub..."
mkdir -p "$TMP_DIR"
mkdir -p "$INSTALL_DIR"
cd "$TMP_DIR"
curl -L "$ZIP_URL" -o autodeskid.zip

echo "📦 Extracting project..."
unzip -qo autodeskid.zip

echo "📦 Installing Python dependencies..."
mv AutoDeskID-main/* "$INSTALL_DIR"
cd "$INSTALL_DIR"
pip3 install -r requirements.txt --break-system-packages

echo "🧹 Cleaning up temporary files..."
rm -rf "$TMP_DIR"

echo "🛠️ Updating service file paths..."
sed -i "s|path/to/script/python/file|$INSTALL_DIR/src/main.py|g" systemd.service/autodeskid.service
sed -i "s|path/to/script/folder|$INSTALL_DIR|g" systemd.service/autodeskid.service

echo "📁 Copying service file to $SERVICE_DIR..."
sudo cp systemd.service/autodeskid.service "$SERVICE_DIR"

echo "🔄 Reloading systemd daemon..."
sudo systemctl daemon-reload

echo "📌 Enabling $SERVICE_NAME service..."
sudo systemctl enable "$SERVICE_NAME.service"

echo "▶️ Starting $SERVICE_NAME service..."
sudo systemctl start "$SERVICE_NAME.service"

echo "ℹ️ Checking service status..."
sudo systemctl status "$SERVICE_NAME.service"

echo "✅ Installation complete!"
