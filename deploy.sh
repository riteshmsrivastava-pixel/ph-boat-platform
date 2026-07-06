#!/bin/bash
# Rebuilds pages from the source pack (if present) and publishes to GitHub Pages.
set -e
cd ~/ph-boat-platform
git add -A
git commit -q -m "${1:-update}" || { echo "Nothing to deploy."; exit 0; }
git push -q
echo "Deployed → https://riteshmsrivastava-pixel.github.io/ph-boat-platform/"
