from PIL import Image
import numpy as np
import os

def get_color_palette(img_path):
    """Extract unique colors from an image's non-transparent pixels."""
    img = Image.open(img_path).convert('RGBA')
    pixels = np.array(img)

    # Get non-transparent pixels
    non_transparent = pixels[pixels[:, :, 3] > 0]

    # Get unique colors
    unique_colors = np.unique(non_transparent[:, :3], axis=0)
    return unique_colors

def map_handle_colors(input_path, output_path, source_handle_colors):
    """
    Recolor only the handle of a netherite sword by mapping handle pixels
    to colors from a source image (e.g., golden_sword, diamond_sword).
    """
    # Load the netherite sword
    img = Image.open(input_path).convert('RGBA')
    pixels = np.array(img, dtype=np.uint8)

    # Store original pixels for the blade
    original_pixels = pixels.copy()

    # Collect handle pixel colors and their brightness
    handle_pixels = []
    for r in range(pixels.shape[0]):
        for c in range(pixels.shape[1]):
            pixel = pixels[r, c]

            if pixel[3] > 0:  # Not transparent
                # Detect handle pixels (brown/tan colors in netherite sword)
                # Handle has more red than blue, and is not dark gray (blade)
                avg = (int(pixel[0]) + int(pixel[1]) + int(pixel[2])) / 3
                is_handle = (
                    pixel[0] > pixel[2] and  # More red than blue
                    avg > 40  # Not too dark (blade is very dark)
                )

                if is_handle:
                    brightness = avg
                    handle_pixels.append((r, c, brightness))

    if not handle_pixels:
        print(f"Warning: No handle pixels found!")
        return

    # Sort source colors by brightness
    source_colors_sorted = sorted(source_handle_colors, key=lambda c: (int(c[0]) + int(c[1]) + int(c[2])) / 3)

    # Map handle pixels to source colors based on brightness
    min_brightness = min(p[2] for p in handle_pixels)
    max_brightness = max(p[2] for p in handle_pixels)

    for r, c, brightness in handle_pixels:
        # Normalize brightness to 0-1
        if max_brightness > min_brightness:
            norm_brightness = (brightness - min_brightness) / (max_brightness - min_brightness)
        else:
            norm_brightness = 0.5

        # Map to source color palette
        color_index = int(norm_brightness * (len(source_colors_sorted) - 1))
        color_index = max(0, min(color_index, len(source_colors_sorted) - 1))

        new_color = source_colors_sorted[color_index]
        pixels[r, c, :3] = new_color

    # Save result
    result = Image.fromarray(pixels, 'RGBA')
    result.save(output_path, 'PNG', optimize=True, compress_level=9)
    print(f"✓ Created: {os.path.basename(output_path)}")

# Paths
input_file = "templates/swords/netherite_sword.png"
output_dir = "assets/minecraft/textures/item/swords"
os.makedirs(output_dir, exist_ok=True)

print("Extracting colors from vanilla Minecraft swords...")
print("=" * 60)

# Extract handle colors from golden sword
golden_sword_colors = get_color_palette("templates/swords/golden_sword.png")
# Filter to get only the gold/yellow handle colors (remove dark outline)
gold_handle_colors = [c for c in golden_sword_colors if (c[0] + c[1] + c[2]) / 3 > 50]

# Extract blade colors from diamond sword (cyan blade)
diamond_sword_colors = get_color_palette("templates/swords/diamond_sword.png")
# Filter to get only the cyan blade colors
diamond_colors = [c for c in diamond_sword_colors if c[2] > c[0] and c[1] > c[0]]

# For emerald, create a green palette similar to Minecraft emerald
# Minecraft emerald is a bright green: base ~(80, 210, 100)
emerald_base = np.array([
    [28, 73, 35],      # Dark
    [50, 130, 60],     # Medium-dark
    [80, 210, 100],    # Medium (base)
    [130, 245, 150],   # Bright
    [170, 255, 180]    # Very bright
], dtype=np.uint8)

print(f"Gold colors extracted: {len(gold_handle_colors)}")
print(f"Diamond colors extracted: {len(diamond_colors)}")
print(f"Emerald colors generated: {len(emerald_base)}")
print("=" * 60)

# Generate the three variants
print("\nGenerating netherite swords with colored handles...")
print("=" * 60)

map_handle_colors(input_file, os.path.join(output_dir, "netherite_gold_handle_sword.png"), gold_handle_colors)
map_handle_colors(input_file, os.path.join(output_dir, "netherite_emerald_handle_sword.png"), emerald_base)
map_handle_colors(input_file, os.path.join(output_dir, "netherite_diamond_handle_sword.png"), diamond_colors)

print("=" * 60)
print("All 3 netherite handle variants generated!")
print("Using exact Minecraft vanilla colors for gold and diamond handles.")
