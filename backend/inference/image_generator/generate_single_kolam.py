#!/usr/bin/env python3
"""
Setup script for Kolam Generator
Sets up the kolamPatternsData.json file from your existing data.
"""
import os
import sys

# Add the current directory to Python path for imports
sys.path.insert(0, os.path.dirname(__file__))

BASE_DIR = os.path.dirname(__file__)  # folder of generate_single_kolam.py
JSON_PATH = os.path.join(BASE_DIR, "kolamPatternsData.json")
output_dir = os.path.join(os.path.dirname(__file__), "renderedImage")
os.makedirs(output_dir, exist_ok=True)

def test_setup(size):
    try:
        # Import modules (removed relative imports)
        from kolam_generator import KolamGenerator
        from kolam_renderer import KolamRenderer
        import json
        
        # Check if JSON file exists
        if not os.path.exists(JSON_PATH):
            print(f"❌ Pattern data file not found: {JSON_PATH}")
            return None
            
        # Check if JSON file exists
        if not os.path.exists(JSON_PATH):
            print(f"❌ Pattern data file not found: {JSON_PATH}")
            return None
        
        # Generate pattern - pass the JSON file path, not the data
        generator = KolamGenerator(JSON_PATH)
        pattern = generator.generate_kolam(size)
        
        # Debug: Check what type of object we get
        print(f"Pattern type: {type(pattern)}")
        print(f"Pattern content: {pattern if not isinstance(pattern, list) or len(pattern) < 10 else 'Large pattern data...'}")
        
        # If generator returns a list of patterns, pick first
        if isinstance(pattern, list) and len(pattern) > 0:
            # Check if it's a list of pattern objects or a list of coordinates
            if hasattr(pattern[0], '__dict__') or isinstance(pattern[0], dict):
                pattern = pattern[0]
            # If it's already coordinate data, keep as is
        elif isinstance(pattern, list) and len(pattern) == 0:
            print("❌ Generator returned empty pattern list")
            return None
            
        # Render to PNG
        renderer = KolamRenderer()
        output_path = os.path.join(output_dir, "ayan.png")
        
        # Make sure output directory exists
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        # Define a default color scheme (matching KolamRenderer expectations)
        default_color_scheme = {
            'bg': '#FFFFFF',      # White background
            'dots': '#000000',    # Black dots
            'lines': '#FF0000'    # Red lines/curves
        }
        
        # Render the pattern
        renderer.render_to_png(pattern, output_path, default_color_scheme, width=size * 128, height=size * 128)
        
        # Verify file was created
        if os.path.exists(output_path):
            print(f"✅ Kolam generated successfully: {output_path}")
            return output_path
        else:
            print("❌ File was not created after rendering")
            return None
            
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Please ensure all modules are in the correct location")
        return None
    except FileNotFoundError as e:
        print(f"❌ File not found: {e}")
        return None
    except Exception as e:
        print(f"❌ Setup test failed: {e}")
        print("Please check that all required dependencies are installed: pip install matplotlib numpy")
        import traceback
        traceback.print_exc()
        return None

def main():
    print("Testing Kolam setup...")
    result = test_setup(16)
    if result:
        print(f"Setup successful! Output: {result}")
    else:
        print("Setup failed!")
        
if __name__ == "__main__":
    main()
