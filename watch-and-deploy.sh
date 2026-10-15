#!/bin/bash

# Watch mode: Compiles Tailwind and copies to cloud folder on changes

SOURCE_DIR="/Users/ekki/Library/CloudStorage/Dropbox/Programmator/RESOURCES/Portfolio/2023/tailwindcss"
TARGET_DIR="/Users/ekki/Library/CloudStorage/CloudMounter-Programmator/portfolio23"

echo "Starting watch mode..."
echo "Watching for changes in: $SOURCE_DIR"
echo "Deploying to: $TARGET_DIR"
echo "Press Ctrl+C to stop"
echo ""

# Initial build and copy
cd "$SOURCE_DIR"
npx tailwindcss -i ./src/input.css -o ./dist/output.css --minify
echo "Initial build complete. Copying files..."
./build-and-deploy.sh

# Watch for changes
npx tailwindcss -i ./src/input.css -o ./dist/output.css --watch &
TAILWIND_PID=$!

# Function to copy files
copy_files() {
    echo "Copying files to cloud folder..."
    cp -r *.html "$TARGET_DIR/" 2>/dev/null
    cp -r projects "$TARGET_DIR/" 2>/dev/null || true
    cp -r menu.html "$TARGET_DIR/" 2>/dev/null || true
    cp -r privacy.html "$TARGET_DIR/" 2>/dev/null || true
    cp -r dist "$TARGET_DIR/" 2>/dev/null || true
    cp -r customStyle.css "$TARGET_DIR/" 2>/dev/null || true
    echo "Files copied!"
}

# Watch for file changes (HTML and CSS source)
fswatch -o "$SOURCE_DIR" --include="\.html$" --include="src/input\.css$" | while read; do
    copy_files
done &
FSWATCH_PID=$!

# Cleanup on exit
trap "kill $TAILWIND_PID $FSWATCH_PID 2>/dev/null; exit" INT TERM

wait
