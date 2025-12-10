#!/usr/bin/env python3
"""
Generate a Minecraft resource pack zip file from the current directory.
Only includes relevant files: assets/ directory and pack.mcmeta
"""

import os
import zipfile
from datetime import datetime
from pathlib import Path

def create_resource_pack(output_name=None):
    """
    Create a resource pack zip file containing only assets/ and pack.mcmeta

    Args:
        output_name: Optional custom name for the output zip file
    """
    # Get the current directory name for the pack name
    current_dir = Path.cwd()
    pack_name = current_dir.name

    # Generate output filename with timestamp if not provided
    if output_name is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_name = f"{pack_name}_{timestamp}.zip"

    # Ensure .zip extension
    if not output_name.endswith('.zip'):
        output_name += '.zip'

    print(f"Creating resource pack: {output_name}")
    print("=" * 60)

    # Files and directories to include
    required_files = ['pack.mcmeta']
    required_dirs = ['assets']

    # Check for required files
    missing_files = []
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)

    if missing_files:
        print(f"⚠️  Warning: Missing files: {', '.join(missing_files)}")
        print("The resource pack may not work correctly without these files.")
        response = input("Continue anyway? (y/n): ")
        if response.lower() != 'y':
            print("Cancelled.")
            return

    # Files and directories to exclude
    exclude_patterns = [
        '__pycache__',
        '.git',
        '.gitignore',
        'venv',
        '.venv',
        'env',
        '.env',
        '.DS_Store',
        '*.pyc',
        '*.py',  # Exclude Python scripts
        '*.zip',  # Exclude existing zip files
        '.idea',
        '.vscode',
        'node_modules'
    ]

    def should_exclude(path):
        """Check if a path should be excluded"""
        path_str = str(path)
        for pattern in exclude_patterns:
            if pattern.startswith('*'):
                # Wildcard pattern
                if path_str.endswith(pattern[1:]):
                    return True
            elif pattern in path_str:
                return True
        return False

    # Create the zip file
    files_added = 0
    with zipfile.ZipFile(output_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
        # Add pack.mcmeta if it exists
        if os.path.exists('pack.mcmeta'):
            zipf.write('pack.mcmeta', 'pack.mcmeta')
            print(f"✓ Added: pack.mcmeta")
            files_added += 1

        # Add pack.png if it exists (resource pack icon)
        if os.path.exists('pack.png'):
            zipf.write('pack.png', 'pack.png')
            print(f"✓ Added: pack.png")
            files_added += 1

        # Add all files in assets/ directory
        if os.path.exists('assets'):
            for root, dirs, files in os.walk('assets'):
                # Remove excluded directories from dirs list to prevent walking into them
                dirs[:] = [d for d in dirs if not should_exclude(os.path.join(root, d))]

                for file in files:
                    file_path = os.path.join(root, file)

                    # Skip excluded files
                    if should_exclude(file_path):
                        continue

                    # Add to zip with relative path
                    zipf.write(file_path, file_path)
                    files_added += 1

            print(f"✓ Added: assets/ directory ({files_added - 1} files)")
        else:
            print("⚠️  Warning: assets/ directory not found")

    # Get the size of the created zip file
    file_size = os.path.getsize(output_name)
    size_mb = file_size / (1024 * 1024)

    print("=" * 60)
    print(f"✓ Resource pack created successfully!")
    print(f"  File: {output_name}")
    print(f"  Size: {size_mb:.2f} MB ({file_size:,} bytes)")
    print(f"  Files: {files_added} files included")
    print(f"\nTo use this pack:")
    print(f"  1. Copy {output_name} to your Minecraft resourcepacks folder")
    print(f"  2. Enable it in Minecraft: Options > Resource Packs")

if __name__ == "__main__":
    import sys

    # Allow custom output name as command line argument
    if len(sys.argv) > 1:
        output_name = sys.argv[1]
    else:
        output_name = None

    create_resource_pack(output_name)
