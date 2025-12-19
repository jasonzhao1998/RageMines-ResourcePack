from PIL import Image
import numpy as np
import os

def recolor_sword_preserve_variation(input_path, output_path, bright_rgb, medium_rgb, dark_rgb):
    """
    Recolor sword while preserving color variation like vanilla Minecraft.
    Maps original brightness smoothly to new color range.
    """
    # Load the image
    img = Image.open(input_path)
    img = img.convert('RGBA')
    pixels = np.array(img.copy(), dtype=np.float32)

    for r in range(pixels.shape[0]):
        for c in range(pixels.shape[1]):
            pixel = pixels[r, c]

            if pixel[3] > 0:  # Not transparent
                # Check if this is a cyan/aqua pixel (sword blade)
                # Detects cyan/aqua colors (high blue & green, lower red)
                is_cyan = (pixel[2] > pixel[0]) and (pixel[1] > pixel[0])

                if is_cyan:
                    # Get the original brightness (0-255)
                    original_brightness = (pixel[0] + pixel[1] + pixel[2]) / 3

                    # Normalize to 0-1 range
                    brightness_norm = original_brightness / 255.0

                    # Create a smooth gradient between dark -> medium -> bright
                    # Based on the original pixel's brightness
                    if brightness_norm < 0.33:
                        # Dark range: interpolate between very dark edge and dark shade
                        t = brightness_norm / 0.33  # 0 to 1 in this range
                        # Very dark edges (almost black) to dark shade
                        edge_color = tuple(int(c * 0.15) for c in dark_rgb)
                        new_color = tuple(
                            edge_color[i] + t * (dark_rgb[i] - edge_color[i])
                            for i in range(3)
                        )
                    elif brightness_norm < 0.66:
                        # Medium range: interpolate between dark and medium
                        t = (brightness_norm - 0.33) / 0.33  # 0 to 1 in this range
                        new_color = tuple(
                            dark_rgb[i] + t * (medium_rgb[i] - dark_rgb[i])
                            for i in range(3)
                        )
                    else:
                        # Bright range: interpolate between medium and bright
                        t = (brightness_norm - 0.66) / 0.34  # 0 to 1 in this range
                        new_color = tuple(
                            medium_rgb[i] + t * (bright_rgb[i] - medium_rgb[i])
                            for i in range(3)
                        )

                    # Add slight random variation for texture (like vanilla)
                    # ±2 on each channel for subtle noise
                    variation = np.random.randint(-2, 3, 3)
                    new_color = tuple(
                        np.clip(int(new_color[i] + variation[i]), 0, 255)
                        for i in range(3)
                    )

                    pixels[r, c] = list(new_color) + [pixel[3]]

    # Convert back to uint8
    pixels = np.clip(pixels, 0, 255).astype(np.uint8)
    result = Image.fromarray(pixels, 'RGBA')
    result.save(output_path, 'PNG', optimize=True, compress_level=9)
    print(f"✓ Created: {os.path.basename(output_path)}")

def create_shades(base_rgb):
    """Create bright, medium, and dark shades from a base RGB color."""
    medium = base_rgb
    # Brighter highlights (1.7x)
    bright = tuple(min(255, int(c * 1.7)) for c in base_rgb)
    # Darker shadows (0.35x)
    dark = tuple(max(0, int(c * 0.35)) for c in base_rgb)
    return bright, medium, dark

# Input and output paths
input_file = "templates/swords/diamond_sword.png"
output_dir = "assets/minecraft/textures/item/swords"

# Ensure output directory exists
os.makedirs(output_dir, exist_ok=True)

# Define all swords with their base colors (same as pickaxes)
swords = [
    ("loam_soil_sword.png", (58, 43, 36)),
    ("peat_sword.png", (96, 60, 32)),
    ("dirt_sword.png", (134, 96, 67)),
    ("ryegrass_sword.png", (76, 83, 42)),
    ("lemon_grass_sword.png", (166, 182, 85)),
    ("oak_leaves_sword.png", (74, 110, 41)),
    ("silvergrass_sword.png", (110, 135, 65)),
    ("dripstone_sword.png", (143, 119, 99))
]

print("Generating sword textures with color variation...")
print("=" * 60)

# Set random seed for reproducibility
np.random.seed(42)

for filename, base_color in swords:
    output_path = os.path.join(output_dir, filename)
    bright, medium, dark = create_shades(base_color)
    recolor_sword_preserve_variation(input_file, output_path, bright, medium, dark)

print("=" * 60)
print(f"All {len(swords)} sword textures generated!")
print("Now with smooth color gradients and subtle variation like vanilla.")
