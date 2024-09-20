#!/bin/sh
echo "==> Install common stuff missing from the slim base image..."   && \
apt-get update            && \
apt-get install -y --no-install-recommends \
    gnupg   \
    dirmngr \
    wget    \
    ca-certificates               && \
    rm -rf /var/lib/apt/lists/*

echo "==> Add Google repo for Chrome..."
wget -q -O- https://dl.google.com/linux/linux_signing_key.pub | apt-key add -  && \
  echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" | tee /etc/apt/sources.list.d/google.list

echo "==> Install prerequisite stuff..."   && \
apt-get update            && \
apt-get install -y --no-install-recommends \
    python3-dev              \
    python3-pip              \
    xvfb                     \
    libfontconfig            \
    libfreetype6             \
    xfonts-scalable          \
    fonts-liberation         \
    google-chrome-stable
