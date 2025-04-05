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

echo "📦 install requirements packges ..."
mv AutoDeskID-main/* $INSTALL_DIR 
cd $INSTALL_DIR
pip3  install -r requirements.txt --break-system-packages
rm $TMP_DIR -rf


sed -i "s|path/to/script/python/file|$INSTALL_DIR/src/main.py|g" systemd.service/autodeskid.service
sed -i "s|path/to/script/folder|$INSTALL_DIR|g" systemd.service/autodeskid.service

cp systemd.service/autodeskid.service /etc/systemd/system


sudo systemctl daemon-reload

sudo systemctl enable autodeskid.service

sudo systemctl start autodeskid.service

sudo systemctl status autodeskid.service


echo "✅ Installation complete!"
