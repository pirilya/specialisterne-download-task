#!/bin/sh
cd ..
source .venv/bin/activate
python -u download_files.py #without this -u, print statements happen all together at the end of execution
echo ""
echo "The script is done! Press any key to close this window"
read -n 1 -s -r