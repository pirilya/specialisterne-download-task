#!/bin/sh
cd ..
echo "Setting up..."
python -m venv .venv
source .venv/bin/activate
pip install -q -r python/requirements.txt
echo "Setup complete! Press any key to close this window"
read -n 1 -s -r