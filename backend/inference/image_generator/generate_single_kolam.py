#!/usr/bin/env python3
"""
Setup script for Kolam Generator
Sets up the kolamPatternsData.json file from your existing data.
"""

def test_setup(size):
    try:
        from kolam_generator import KolamGenerator
        from kolam_renderer import KolamRenderer
        import json

        # Load pattern data
        with open('kolamPatternsData.json', 'r') as f:
            data = json.load(f)
            patterns_data = data['patterns']

        # Create generator and test
        generator = KolamGenerator(patterns_data)
        pattern = generator.generate_kolam(size)

        # Create renderer and test
        renderer = KolamRenderer()
        renderer.render_to_png(pattern, './renderedImage/output.png', width=size * 128, height=size * 128) #appropriate resolution for the respective size

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
