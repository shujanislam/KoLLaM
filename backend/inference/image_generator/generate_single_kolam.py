#!/usr/bin/env python3
"""
Single Kolam Generator - Generate individual kolam patterns
"""

import os
from kolam_generator import KolamGenerator
from kolam_renderer import KolamRenderer, ColorPalettes

def generate_single_kolam(json_path: str, size: int, theme: str = 'classic',
                         output_filename: str = None, width: int = 800,
                         height: int = 800) -> str:
    """
    Generate a single kolam image

    Args:
        json_path: Path to kolamPatternsData.json
        size: Size of kolam (3-15)
        theme: Color theme name
        output_filename: Output filename (auto-generated if None)
        width: Image width in pixels
        height: Image height in pixels

    Returns:
        Path to generated image
    """
    generator = KolamGenerator(json_path)
    renderer = KolamRenderer()

    pattern = generator.generate_kolam(size)
    color_scheme = ColorPalettes.get_theme(theme)

    if not output_filename:
        output_filename = f"kolam_size{size}_{theme}.png"

    renderer.render_to_png(pattern, output_filename, color_scheme, width, height)

    return output_filename

def main():
    """Generate a single kolam with default parameters"""
    json_path = "kolamPatternsData.json"

    if not os.path.exists(json_path):
        return None

    output_dir = "renderedImage"
    os.makedirs(output_dir, exist_ok=True)

    output_path = os.path.join(output_dir, "single_kolam.png")
    generated_file = generate_single_kolam(json_path, 7, 'classic', output_path)

    return generated_file

if __name__ == "__main__":
    main()
