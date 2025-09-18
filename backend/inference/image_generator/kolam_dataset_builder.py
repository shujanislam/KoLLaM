import os
import json
import shutil
from kolam_generator import KolamGenerator
from kolam_renderer import KolamRenderer
from kolam_utils import ColorPalettes

def build_dataset(output_dir="kolam_dataset", num_variations=10):
    """Generate flat kolam dataset with 5 unique color schemes."""

    # always clear old dataset
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)
    os.makedirs(output_dir, exist_ok=True)

    # Load patterns
    with open("kolamPatternsData.json", "r") as f:
        data = json.load(f)

    generator = KolamGenerator(data["patterns"])
    renderer = KolamRenderer()

    # pick the 5 unique schemes
    selected_schemes = {
        "classic": ColorPalettes.CLASSIC,
        "ocean": ColorPalettes.OCEAN,
        "forest": ColorPalettes.FOREST,
        "sunset": ColorPalettes.SUNSET,
        "royal": ColorPalettes.ROYAL,
    }

    for scheme_name, colors in selected_schemes.items():
        print(f"\n🎨 Generating dataset for scheme: {scheme_name}")
        image_index = 1

        for size in range(5, 17):  # sizes 5x5 → 16x16
            for _ in range(num_variations):
                pattern = generator.generate_kolam(size)

                filename = f"kolam_{scheme_name}_{image_index:03d}.png"
                filepath = os.path.join(output_dir, filename)

                renderer.render_to_png(
                    pattern,
                    filepath,
                    dot_color=colors["dots"],
                    line_color=colors["lines"],
                    background_color=colors["bg"],
                    width=size * 128,
                    height=size * 128
                )

                print(f"✅ Saved {filepath}")
                image_index += 1

if __name__ == "__main__":
    build_dataset()
