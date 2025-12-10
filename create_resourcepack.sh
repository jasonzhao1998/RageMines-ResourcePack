#!/bin/bash
set -e  # Exit on error

# Configuration
OUTPUT_NAME="${1:-RageMinesResourcePack}"

echo "=========================================="
echo "RageMines Resource Pack Builder"
echo "=========================================="
echo ""

# Remove existing output folder if it exists
if [ -d "$OUTPUT_NAME" ]; then
    echo "⚠️  Output folder '$OUTPUT_NAME' already exists"
    read -p "Remove and recreate? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        rm -rf "$OUTPUT_NAME"
        echo "✓ Removed existing folder"
    else
        echo "Cancelled"
        exit 0
    fi
fi

echo "Creating resource pack folder: $OUTPUT_NAME"
echo "=" * 60

# Create output directory
mkdir -p "$OUTPUT_NAME"

# Copy pack.mcmeta if it exists
if [ -f "pack.mcmeta" ]; then
    cp pack.mcmeta "$OUTPUT_NAME/"
    echo "✓ Copied: pack.mcmeta"
else
    echo "⚠️  Warning: pack.mcmeta not found"
fi

# Copy pack.png if it exists (resource pack icon)
if [ -f "pack.png" ]; then
    cp pack.png "$OUTPUT_NAME/"
    echo "✓ Copied: pack.png"
fi

# Copy assets directory if it exists
if [ -d "assets" ]; then
    echo "Copying assets directory..."

    # Use rsync to copy, excluding unwanted files
    rsync -av --progress \
        --exclude='.DS_Store' \
        --exclude='__pycache__' \
        --exclude='*.pyc' \
        assets/ "$OUTPUT_NAME/assets/"

    # Count files
    file_count=$(find "$OUTPUT_NAME/assets" -type f | wc -l | tr -d ' ')
    echo "✓ Copied: assets/ ($file_count files)"
else
    echo "⚠️  Warning: assets/ directory not found"
fi

# Calculate folder size
folder_size=$(du -sh "$OUTPUT_NAME" | awk '{print $1}')

echo ""
echo "=========================================="
echo "✓ Resource pack folder created!"
echo "=========================================="
echo ""
echo "📁 Location: ./$OUTPUT_NAME"
echo "📊 Size: $folder_size"
echo ""
echo "📝 Contents:"
ls -lh "$OUTPUT_NAME"
echo ""
echo "To use this pack:"
echo "  1. Copy the '$OUTPUT_NAME' folder to your Minecraft resourcepacks folder"
echo "  2. Or zip it: zip -r $OUTPUT_NAME.zip $OUTPUT_NAME"
echo "  3. Enable it in Minecraft: Options > Resource Packs"
echo ""
