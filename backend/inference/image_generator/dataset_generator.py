#!/usr/bin/env python3
"""
Kolam Dataset Generator - Generate complete datasets of valid and invalid kolams
"""

import os
import random
from typing import List
from kolam_generator import KolamGenerator
from kolam_renderer import KolamRenderer, ColorPalettes

class KolamDatasetGenerator:

    def __init__(self, json_path: str):
        self.generator = KolamGenerator(json_path)
        self.renderer = KolamRenderer()
        self.themes = list(ColorPalettes.THEMES.keys())

    def generate_valid_dataset(self, output_dir: str = "dataset",
                              sizes: List[int] = None,
                              num_per_size: int = 5,
                              themes_per_size: int = 3) -> List[str]:
        """Generate valid kolam dataset"""

        if sizes is None:
            sizes = [3, 5, 7, 9, 11, 13, 15]

        valid_dir = os.path.join(output_dir, "valid")
        os.makedirs(valid_dir, exist_ok=True)

        generated_files = []

        for size in sizes:
            for i in range(num_per_size):
                # Select random themes for variety
                selected_themes = random.sample(self.themes, min(themes_per_size, len(self.themes)))

                for theme in selected_themes:
                    pattern = self.generator.generate_kolam(size)
                    color_scheme = ColorPalettes.get_theme(theme)

                    filename = f"valid_kolam_s{size:02d}_i{i:03d}_{theme}.png"
                    filepath = os.path.join(valid_dir, filename)

                    # Vary image sizes for diversity
                    width = random.choice([512, 768, 1024])
                    height = width  # Keep square

                    self.renderer.render_to_png(pattern, filepath, color_scheme, width, height)
                    generated_files.append(filepath)

        return generated_files

    def generate_invalid_dataset(self, output_dir: str = "dataset",
                                sizes: List[int] = None,
                                num_per_size: int = 3,
                                themes_per_size: int = 2) -> List[str]:
        """Generate invalid kolam dataset"""

        if sizes is None:
            sizes = [3, 5, 7, 9, 11, 13, 15]

        invalid_dir = os.path.join(output_dir, "invalid")
        os.makedirs(invalid_dir, exist_ok=True)

        invalid_types = ["broken_loops", "asymmetry", "displaced_dots"]
        generated_files = []

        for size in sizes:
            for invalid_type in invalid_types:
                for i in range(num_per_size):
                    selected_themes = random.sample(self.themes, min(themes_per_size, len(self.themes)))

                    for theme in selected_themes:
                        pattern = self.generator.generate_invalid_kolam(size, invalid_type)
                        color_scheme = ColorPalettes.get_theme(theme)

                        filename = f"invalid_{invalid_type}_s{size:02d}_i{i:03d}_{theme}.png"
                        filepath = os.path.join(invalid_dir, filename)

                        width = random.choice([512, 768, 1024])
                        height = width

                        self.renderer.render_to_png(pattern, filepath, color_scheme, width, height)
                        generated_files.append(filepath)

        return generated_files

    def generate_complete_dataset(self, output_dir: str = "dataset",
                                 sizes: List[int] = None,
                                 valid_per_size: int = 5,
                                 invalid_per_size: int = 3) -> dict:
        """Generate complete dataset with both valid and invalid kolams"""

        if sizes is None:
            sizes = [3, 5, 7, 9, 11, 13, 15]

        valid_files = self.generate_valid_dataset(output_dir, sizes, valid_per_size)
        invalid_files = self.generate_invalid_dataset(output_dir, sizes, invalid_per_size)

        return {
            'valid': valid_files,
            'invalid': invalid_files,
            'total_valid': len(valid_files),
            'total_invalid': len(invalid_files),
            'sizes': sizes
        }

def main():
    """Generate complete kolam dataset"""
    json_path = "kolamPatternsData.json"

    if not os.path.exists(json_path):
        return None

    dataset_gen = KolamDatasetGenerator(json_path)

    # Generate complete dataset
    results = dataset_gen.generate_complete_dataset(
        output_dir="dataset",
        sizes=[3, 5, 7, 9, 11, 13],  # Smaller range for faster generation
        valid_per_size=10,
        invalid_per_size=10
    )

    return results

if __name__ == "__main__":
    main()
