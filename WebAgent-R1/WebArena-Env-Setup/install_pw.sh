#!/bin/bash

# === Playwright on AWS DLAMI Ubuntu 24 (g5.48xlarge) ===
set -euo pipefail

# 0) (Recommended) run inside tmux so the session survives SSH hiccups
# sudo apt-get update -y && sudo apt-get install -y tmux && tmux new -s pw

# 1) Basic OS tools
sudo apt-get update -y
sudo apt-get install -y curl git build-essential

# 2) Create an isolated conda env (DLAMI ships with conda)
#source ~/anaconda3/etc/profile.d/conda.sh || source ~/miniconda3/etc/profile.d/conda.sh ||
conda create -y -n pw python=3.11
conda activate pw
python -V

# 3) Install Playwright + browsers
python -m pip install --upgrade pip
pip install playwright

# Install Chromium (fastest) – or use "python -m playwright install" for all (chromium, firefox, webkit)
python -m playwright install chromium

# 4) Install required OS libraries (Playwright helper for Ubuntu 24 works fine)
# IMPORTANT: use the *same python* that has playwright installed
PYBIN="$(command -v python)"
sudo "$PYBIN" -m playwright install-deps || true

# Fallback (only if you still see missing-lib errors):
# sudo apt-get install -y libgbm1 libxshmfence1 libasound2 libatk-bridge2.0-0 \
#   libgtk-3-0 libnss3 libx11-xcb1 libxcomposite1 libxdamage1 libxrandr2 \
#   libxkbcommon0 libcups2 libpangocairo-1.0-0

# 5) Quick sanity test (headless)
cat > test_pw.py << 'PY'
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(
        headless=True,
        args=[
            "--no-sandbox",             # EC2/CI friendly
            "--disable-dev-shm-usage",  # avoid small /dev/shm issues
            "--use-gl=egl",             # fine on NVIDIA driver stacks
        ],
    )
    page = browser.new_page(viewport={"width": 1280, "height": 800})
    page.goto("https://example.com", timeout=60_000)
    page.screenshot(path="example.png")
    print("Title:", page.title())
    browser.close()
PY

python test_pw.py
ls -lh example.png
echo "✅ Playwright is working on DLAMI Ubuntu 24."
