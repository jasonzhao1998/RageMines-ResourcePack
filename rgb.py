#!/usr/bin/env python3
import sys

def decimal_to_rgb(decimal):
    """Convert decimal color to RGB tuple"""
    red = (decimal >> 16) & 0xFF
    green = (decimal >> 8) & 0xFF
    blue = decimal & 0xFF
    return (red, green, blue)

def rgb_to_hex(r, g, b):
    """Convert RGB to hex color code"""
    return f"#{r:02X}{g:02X}{b:02X}"

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python rgb.py <decimal_color>")
        print("Example: python rgb.py 6306848")
        sys.exit(1)

    try:
        decimal = int(sys.argv[1])
        r, g, b = decimal_to_rgb(decimal)
        hex_code = rgb_to_hex(r, g, b)
        print(f"RGB({r} {g} {b}) → {hex_code}")
    except ValueError:
        print(f"Error: '{sys.argv[1]}' is not a valid number")
        sys.exit(1)
