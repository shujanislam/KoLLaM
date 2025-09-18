#!/usr/bin/env python3
"""
Setup script for Kolam Generator
Sets up the kolamPatternsData.json file from your existing data.
"""
import os

BASE_DIR = os.path.dirname(__file__)  # folder of generate_single_kolam.py
JSON_PATH = os.path.join(BASE_DIR, "kolamPatternsData.json")

output_dir = os.path.join(os.path.dirname(__file__), "renderedImage")
os.makedirs(output_dir, exist_ok=True)

def test_setup(size):
    try:
        from .kolam_generator import KolamGenerator
        from .kolam_renderer import KolamRenderer
        import json

        # Load pattern data
        with open(JSON_PATH, 'r') as f:
            data = json.load(f)
            patterns_data = data['patterns']

        # Create generator and test
        generator = KolamGenerator(patterns_data)
        pattern = generator.generate_kolam(size)

        # Create renderer and test
        renderer = KolamRenderer()
        output_path = os.path.join(output_dir, "ayan.png")
        renderer.render_to_png(pattern, output_path, width=size * 128, height=size * 128) #appropriate resolution for the respective size

        return output_path

    except Exception as e:
        print(f"❌ Setup test failed: {e}")
        print("Please check that all required dependencies are installed:")
        print("  pip install matplotlib numpy")
        return False

    return True

def main():
    test_setup(16)

if __name__ == "__main__":
    main()
