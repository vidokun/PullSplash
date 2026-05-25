#!/bin/bash
set -e

cd "$(dirname "$0")/.."

echo "=== PullSplash Mac Build ==="
echo ""

# Ensure deps
pip3 install -r requirements.txt > /dev/null 2>&1

echo "Building PullSplash.app ..."
pyinstaller \
    --distpath ./dist \
    --workpath ./build \
    --clean \
    --noconfirm \
    packaging/pullsplash.spec

echo ""
echo "Done! Output: dist/PullSplash.app"
echo "Double-click dist/PullSplash.app to launch."
echo ""
echo "To distribute: zip the .app file."
echo "  cd dist && zip -r PullSplash-mac.zip PullSplash.app"
