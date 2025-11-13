#!/bin/bash

# Make sure 'universe' is enabled (usually is on DLAMI)
sudo apt-get update -y
sudo apt-get install -y software-properties-common
sudo add-apt-repository -y universe
sudo apt-get update -y

# Core runtime libs Chromium/WebKit need on Noble
sudo apt-get install -y \
  libnss3 libnspr4 libx11-xcb1 libxcomposite1 libxdamage1 libxrandr2 \
  libxkbcommon0 libxshmfence1 libasound2t64 libgbm1 libcups2 \
  libatk-bridge2.0-0 libgtk-3-0 libpangocairo-1.0-0 \
  libx11-6 libxext6 libxi6 libxfixes3 libglib2.0-0 libdrm2 libxcb1 \
  libxrender1 ca-certificates fonts-liberation libicu74 libffi8 ffmpeg

# Optional: if some sites need x264 explicitly on your build
sudo apt-get install -y libx264-164 || true
