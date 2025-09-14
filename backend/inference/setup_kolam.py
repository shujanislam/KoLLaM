#!/usr/bin/env python3
"""
Setup script for Kolam Generator
Sets up the kolamPatternsData.json file from your existing data.
"""

import json
import sys
import shutil
from pathlib import Path
import numpy as np

def copy_existing_json():
    """Copy an existing kolamPatternsData.json file."""
    print("📁 Looking for existing kolamPatternsData.json file...")

    # Check if file already exists in current directory
    if Path('kolamPatternsData.json').exists():
        print("✅ Found kolamPatternsData.json in current directory")
        return validate_pattern_data('kolamPatternsData.json')

    # Ask user for file path
    print("\n💡 Please provide the path to your kolamPatternsData.json file:")
    print("   Examples:")
    print("   - ./kolamPatternsData.json")
    print("   - /path/to/your/kolamPatternsData.json")
    print("   - ../data/kolamPatternsData.json")

    while True:
        file_path = input("\nEnter file path (or 'quit' to exit): ").strip()

        if file_path.lower() == 'quit':
            print("Setup cancelled.")
            return False

        if not file_path:
            continue

        source_path = Path(file_path)

        if not source_path.exists():
            print(f"❌ File not found: {file_path}")
            continue

        try:
            # Copy the file
            shutil.copy2(source_path, 'kolamPatternsData.json')
            print(f"✅ Copied {file_path} to kolamPatternsData.json")
            return validate_pattern_data('kolamPatternsData.json')

        except Exception as e:
            print(f"❌ Error copying file: {e}")
            continue

def validate_pattern_data(filename):
    """Validate the pattern data file."""
    try:
        with open(filename, 'r') as f:
            data = json.load(f)

        # Check required structure
        if 'patterns' not in data:
            print("❌ Error: JSON file missing 'patterns' key")
            return False

        patterns = data['patterns']

        if not isinstance(patterns, list):
            print("❌ Error: 'patterns' should be a list")
            return False

        if len(patterns) == 0:
            print("❌ Error: No patterns found in file")
            return False

        print(f"📊 Validation Results:")
        print(f"   Total patterns: {len(patterns)}")

        # Check each pattern
        valid_patterns = 0
        for i, pattern in enumerate(patterns):
            if not isinstance(pattern, dict):
                print(f"   ⚠️  Pattern {i+1}: Not a dictionary")
                continue

            if 'id' not in pattern:
                print(f"   ⚠️  Pattern {i+1}: Missing 'id'")
                continue

            if 'points' not in pattern:
                print(f"   ⚠️  Pattern {i+1}: Missing 'points'")
                continue

            points = pattern['points']
            if not isinstance(points, list) or len(points) == 0:
                print(f"   ⚠️  Pattern {i+1}: Invalid or empty 'points'")
                continue

            # Check points structure
            valid_points = True
            for j, point in enumerate(points[:5]):  # Check first 5 points
                if not isinstance(point, dict) or 'x' not in point or 'y' not in point:
                    print(f"   ⚠️  Pattern {i+1}: Invalid point structure at index {j}")
                    valid_points = False
                    break

            if valid_points:
                valid_patterns += 1
                print(f"   ✅ Pattern {pattern['id']}: {len(points)} points")

        print(f"\n📈 Summary: {valid_patterns}/{len(patterns)} patterns are valid")

        if valid_patterns == 0:
            print("❌ No valid patterns found!")
            return False

        print("✅ Pattern data file is valid!")
        return True

    except json.JSONDecodeError as e:
        print(f"❌ Error: Invalid JSON format - {e}")
        return False
    except Exception as e:
        print(f"❌ Error validating file: {e}")
        return False

def create_minimal_test_data():
    """Create minimal test data if user doesn't have the file."""
    print("\n🔧 Creating minimal test data...")

    minimal_data = {
        "description": "Minimal kolam patterns for testing",
        "extractedAt": "2025-01-19T12:00:00.000Z",
        "totalPatterns": 4,
        "patterns": [
            {
                "id": 1,
                "points": [
                    {"x": 0.25, "y": 0}, {"x": 0.2495, "y": 0.0159}, {"x": 0.248, "y": 0.0316},
                    {"x": 0.2455, "y": 0.0473}, {"x": 0.242, "y": 0.0628}, {"x": 0.2375, "y": 0.078},
                    {"x": 0.2321, "y": 0.0929}, {"x": 0.2257, "y": 0.1074}, {"x": 0.2185, "y": 0.1215},
                    {"x": 0.2103, "y": 0.1352}, {"x": 0.2013, "y": 0.1482}, {"x": 0.1915, "y": 0.1607},
                    {"x": 0.1809, "y": 0.1725}, {"x": 0.1696, "y": 0.1836}, {"x": 0.1576, "y": 0.194},
                    {"x": 0.145, "y": 0.2036}, {"x": 0.1318, "y": 0.2124}, {"x": 0.1181, "y": 0.2204},
                    {"x": 0.1039, "y": 0.2274}, {"x": 0.0892, "y": 0.2335}, {"x": 0.0742, "y": 0.2387},
                    {"x": 0.0589, "y": 0.243}, {"x": 0.0434, "y": 0.2462}, {"x": 0.0277, "y": 0.2485},
                    {"x": 0.0119, "y": 0.2497}, {"x": -0.004, "y": 0.25}, {"x": -0.0198, "y": 0.2492},
                    {"x": -0.0356, "y": 0.2475}, {"x": -0.0512, "y": 0.2447}, {"x": -0.0666, "y": 0.241},
                    {"x": -0.0818, "y": 0.2363}, {"x": -0.0966, "y": 0.2306}, {"x": -0.111, "y": 0.224},
                    {"x": -0.125, "y": 0.2165}, {"x": -0.1385, "y": 0.2081}, {"x": -0.1514, "y": 0.1989},
                    {"x": -0.1637, "y": 0.1889}, {"x": -0.1754, "y": 0.1782}, {"x": -0.1863, "y": 0.1667},
                    {"x": -0.1965, "y": 0.1545}, {"x": -0.2059, "y": 0.1418}, {"x": -0.2145, "y": 0.1284},
                    {"x": -0.2222, "y": 0.1146}, {"x": -0.229, "y": 0.1002}, {"x": -0.2349, "y": 0.0855},
                    {"x": -0.2399, "y": 0.0704}, {"x": -0.2439, "y": 0.0551}, {"x": -0.2469, "y": 0.0395},
                    {"x": -0.2489, "y": 0.0238}, {"x": -0.2499, "y": 0.0079}, {"x": -0.2499, "y": -0.0079},
                    {"x": -0.2489, "y": -0.0238}, {"x": -0.2469, "y": -0.0395}, {"x": -0.2439, "y": -0.0551},
                    {"x": -0.2399, "y": -0.0704}, {"x": -0.2349, "y": -0.0855}, {"x": -0.229, "y": -0.1002},
                    {"x": -0.2222, "y": -0.1146}, {"x": -0.2145, "y": -0.1284}, {"x": -0.2059, "y": -0.1418},
                    {"x": -0.1965, "y": -0.1545}, {"x": -0.1863, "y": -0.1667}, {"x": -0.1754, "y": -0.1782},
                    {"x": -0.1637, "y": -0.1889}, {"x": -0.1514, "y": -0.1989}, {"x": -0.1385, "y": -0.2081},
                    {"x": -0.125, "y": -0.2165}, {"x": -0.111, "y": -0.224}, {"x": -0.0966, "y": -0.2306},
                    {"x": -0.0818, "y": -0.2363}, {"x": -0.0666, "y": -0.241}, {"x": -0.0512, "y": -0.2447},
                    {"x": -0.0356, "y": -0.2475}, {"x": -0.0198, "y": -0.2492}, {"x": -0.004, "y": -0.25},
                    {"x": 0.0119, "y": -0.2497}, {"x": 0.0277, "y": -0.2485}, {"x": 0.0434, "y": -0.2462},
                    {"x": 0.0589, "y": -0.243}, {"x": 0.0742, "y": -0.2387}, {"x": 0.0892, "y": -0.2335},
                    {"x": 0.1039, "y": -0.2274}, {"x": 0.1181, "y": -0.2204}, {"x": 0.1318, "y": -0.2124},
                    {"x": 0.145, "y": -0.2036}, {"x": 0.1576, "y": -0.194}, {"x": 0.1696, "y": -0.1836},
                    {"x": 0.1809, "y": -0.1725}, {"x": 0.1915, "y": -0.1607}, {"x": 0.2013, "y": -0.1482},
                    {"x": 0.2103, "y": -0.1352}, {"x": 0.2185, "y": -0.1215}, {"x": 0.2257, "y": -0.1074},
                    {"x": 0.2321, "y": -0.0929}, {"x": 0.2375, "y": -0.078}, {"x": 0.242, "y": -0.0628},
                    {"x": 0.2455, "y": -0.0473}, {"x": 0.248, "y": -0.0316}, {"x": 0.2495, "y": -0.0159},
                    {"x": 0.25, "y": 0}
                ],
                "hasDownConnection": False,
                "hasRightConnection": True
            },
            {
                "id": 2,
                "points": [
                    {"x": 0, "y": -0.5}, {"x": 0.1, "y": -0.4}, {"x": 0.2, "y": -0.2},
                    {"x": 0.25, "y": 0}, {"x": 0.2, "y": 0.2}, {"x": 0.1, "y": 0.4}, {"x": 0, "y": 0.5},
                    {"x": -0.1, "y": 0.4}, {"x": -0.2, "y": 0.2}, {"x": -0.25, "y": 0},
                    {"x": -0.2, "y": -0.2}, {"x": -0.1, "y": -0.4}, {"x": 0, "y": -0.5}
                ],
                "hasDownConnection": False,
                "hasRightConnection": False
            },
            {
                "id": 3,
                "points": [
                    {"x": 0.5, "y": 0}, {"x": 0.4, "y": 0.1}, {"x": 0.2, "y": 0.2},
                    {"x": 0, "y": 0.25}, {"x": -0.2, "y": 0.2}, {"x": -0.4, "y": 0.1}, {"x": -0.5, "y": 0},
                    {"x": -0.4, "y": -0.1}, {"x": -0.2, "y": -0.2}, {"x": 0, "y": -0.25},
                    {"x": 0.2, "y": -0.2}, {"x": 0.4, "y": -0.1}, {"x": 0.5, "y": 0}
                ],
                "hasDownConnection": False,
                "hasRightConnection": True
            },
            {
                "id": 4,
                "points": [
                    {"x": 0, "y": 0.5}, {"x": -0.1, "y": 0.4}, {"x": -0.2, "y": 0.2},
                    {"x": -0.25, "y": 0}, {"x": -0.2, "y": -0.2}, {"x": -0.1, "y": -0.4}, {"x": 0, "y": -0.5},
                    {"x": 0.1, "y": -0.4}, {"x": 0.2, "y": -0.2}, {"x": 0.25, "y": 0},
                    {"x": 0.2, "y": 0.2}, {"x": 0.1, "y": 0.4}, {"x": 0, "y": 0.5}
                ],
                "hasDownConnection": True,
                "hasRightConnection": False
            }
        ]
    }

    # Add 12 more simple patterns to make 16 total (required by algorithm)
    for i in range(5, 17):
        # Create simple geometric patterns
        angle_offset = (i - 5) * 30  # degrees
        points = []
        for j in range(8):
            angle = (j * 45 + angle_offset) * 3.14159 / 180
            x = 0.2 * np.cos(angle) if 'numpy' in sys.modules else 0.2 * (1 if j % 2 == 0 else -1) * (0.7 if j < 4 else 0.3)
            y = 0.2 * np.sin(angle) if 'numpy' in sys.modules else 0.2 * (1 if j % 4 < 2 else -1) * (0.7 if j % 2 == 0 else 0.3)
            points.append({"x": round(x, 4), "y": round(y, 4)})

        minimal_data["patterns"].append({
            "id": i,
            "points": points,
            "hasDownConnection": i % 3 != 0,
            "hasRightConnection": i % 2 == 0
        })

    minimal_data["totalPatterns"] = len(minimal_data["patterns"])

    with open('kolamPatternsData.json', 'w') as f:
        json.dump(minimal_data, f, indent=2)

    print("✅ Created minimal test data with 16 patterns")
    return True

def test_setup():
    """Test the setup by generating a simple kolam."""
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
        pattern = generator.generate_kolam(16)  # Small test kolam

        # Create renderer and test
        renderer = KolamRenderer()
        renderer.render_to_png(pattern, 'test_kolam.png', width=400, height=400)

        print("✅ Setup test successful! Created test_kolam.png")
        print("🎉 Kolam generator is ready to use!")

        # Show some stats
        from kolam_utils import KolamUtils
        KolamUtils.print_pattern_stats(pattern)

    except Exception as e:
        print(f"❌ Setup test failed: {e}")
        print("Please check that all required dependencies are installed:")
        print("  pip install matplotlib numpy")
        return False

    return True

def main():
    """Main setup function."""
    print("🎨 Kolam Generator Setup")
    print("=" * 30)

    # First try to copy existing JSON
    if not copy_existing_json():
        print("\n⚠️  No valid pattern data found.")
        response = input("Create minimal test data instead? (y/N): ")
        if response.lower() == 'y':
            if not create_minimal_test_data():
                print("❌ Failed to create test data")
                return
        else:
            print("Setup cancelled. Please provide your kolamPatternsData.json file.")
            return

    # Ask if user wants to test
    print("\n" + "="*50)
    response = input("Would you like to run a test generation? (Y/n): ")
    if response.lower() != 'n':
        test_setup()

    print("\n🚀 Setup complete!")
    print("Usage examples:")
    print("  python kolam_cli.py generate --size 7 --output my_kolam.png")
    print("  python kolam_cli.py variants --size 5 --output variants.png")
    print("  python kolam_cli.py list-palettes")
    print("  python kolam_cli.py generate --help")

if __name__ == "__main__":
    main()
