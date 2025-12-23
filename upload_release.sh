#!/bin/bash
set -e  # Exit on error

# Configuration
REPO="jasonzhao1998/RageMines-ResourcePack"
VERSION="v1.0.0"
ZIP_NAME="RageMinesResourcePack.zip"

echo "=========================================="
echo "RageMines Resource Pack Release Uploader"
echo "=========================================="
echo ""

# Step 1: Generate the resource pack folder
echo "Step 1: Generating resource pack folder..."
FOLDER_NAME="RageMinesResourcePack"
./create_resourcepack.sh "$FOLDER_NAME" <<< "y"

if [ ! -d "$FOLDER_NAME" ]; then
    echo "❌ Error: $FOLDER_NAME folder was not created"
    exit 1
fi

echo "✓ Resource pack folder created: $FOLDER_NAME"
echo ""

# Step 1.5: Create zip from folder
echo "Step 1.5: Creating zip file..."
rm -f "$ZIP_NAME"  # Remove if exists
(cd "$FOLDER_NAME" && zip -r "../$ZIP_NAME" . -q)

if [ ! -f "$ZIP_NAME" ]; then
    echo "❌ Error: $ZIP_NAME was not created"
    exit 1
fi

echo "✓ Zip file created: $ZIP_NAME"
echo ""

# Step 2: Calculate SHA-1 hash and generate UUID
echo "Step 2: Calculating SHA-1 hash and generating UUID..."
SHA1=$(shasum -a 1 "$ZIP_NAME" | awk '{print $1}')
UUID=$(python3 -c "import uuid; print(uuid.uuid4())")
echo "✓ SHA-1: $SHA1"
echo "✓ UUID: $UUID"
echo ""

# Step 3: Check if gh CLI is installed
if ! command -v gh &> /dev/null; then
    echo "❌ Error: GitHub CLI (gh) is not installed"
    echo "Install it with: brew install gh"
    echo ""
    echo "After installation, run: gh auth login"
    exit 1
fi

# Step 4: Check if authenticated
echo "Step 3: Checking GitHub authentication..."
if ! gh auth status &> /dev/null; then
    echo "❌ Error: Not authenticated with GitHub"
    echo "Run: gh auth login"
    exit 1
fi
echo "✓ Authenticated"
echo ""

# Step 5: Check if release exists
echo "Step 4: Checking if release $VERSION exists..."
if gh release view "$VERSION" --repo "$REPO" &> /dev/null; then
    echo "⚠️  Release $VERSION already exists"
    read -p "Delete existing release and create new one? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo "Deleting existing release..."
        gh release delete "$VERSION" --repo "$REPO" --yes
        echo "✓ Deleted"
    else
        echo "Cancelled"
        exit 0
    fi
fi
echo ""

# Step 6: Create release and upload
echo "Step 5: Creating release and uploading..."
gh release create "$VERSION" \
    "$ZIP_NAME" \
    --repo "$REPO" \
    --title "RageMines Resource Pack $VERSION" \
    --notes ""

echo ""
echo "=========================================="
echo "✓ Release uploaded successfully!"
echo "=========================================="
echo ""
echo "📦 Release URL:"
echo "   https://github.com/$REPO/releases/tag/$VERSION"
echo ""
echo "📥 Download URL:"
echo "   https://github.com/$REPO/releases/download/$VERSION/$ZIP_NAME"
echo ""
echo "🔐 SHA-1 Hash:"
echo "   $SHA1"
echo ""
echo "🆔 Resource Pack UUID:"
echo "   $UUID"
echo ""
echo "📝 Add to server.properties:"
echo "   resource-pack=https://github.com/$REPO/releases/download/$VERSION/$ZIP_NAME"
echo "   resource-pack-id=$UUID"
echo "   resource-pack-sha1=$SHA1"
echo ""
