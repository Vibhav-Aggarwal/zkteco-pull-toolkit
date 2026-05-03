#!/bin/bash
# macOS double-clickable .command file — runs door unlock from Finder.
# Place in your Desktop or Applications folder.
# Prerequisites: pip3 install pyzk

cd "$(dirname "$0")"
export ZKTECO_IP="${ZKTECO_IP:-192.168.1.201}"
python3 simple_unlock.py
read -p "Press Enter to close..."
