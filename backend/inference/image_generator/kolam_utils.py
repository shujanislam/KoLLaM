#!/usr/bin/env python3
"""
Kolam Utilities
Helper functions for kolam pattern manipulation and analysis.
"""

import json
import numpy as np
from typing import Dict, List, Tuple, Optional
from pathlib import Path
import matplotlib.colors as mcolors

class KolamUtils:
    """Utility functions for kolam operations."""

    @staticmethod
    def save_pattern_to_json(pattern: Dict, filename: str) -> None:
        """Save a kolam pattern to JSON file."""
        with open(filename, 'w') as f:
            json.dump(pattern, f, indent=2)
        print(f"💾 Pattern saved to {filename}")

    @staticmethod
    def load_pattern_from_json(filename: str) -> Dict:
        """Load a kolam pattern from JSON file."""
        with open(filename, 'r') as f:
            pattern = json.load(f)
        print(f"📂 Pattern loaded from {filename}")
        return pattern

    @staticmethod
    def validate_color(color_str: str) -> bool:
        """Validate if a color string is valid for matplotlib."""
        try:
            mcolors.to_rgba(color_str)
            return True
        except ValueError:
            return False

    @staticmethod
    def get_pattern_stats(pattern: Dict) -> Dict:
        """Get statistics about a kolam pattern."""
        stats = {
            'id': pattern.get('id', 'unknown'),
            'name': pattern.get('name', 'Unknown Kolam'),
            'dimensions': pattern.get('dimensions', {}),
            'num_dots': len(pattern.get('dots', [])),
            'num_curves': len(pattern.get('curves', [])),
            'total_curve_points': sum(len(curve.get('points', [])) for curve in pattern.get('curves', [])),
        }

        if 'matrix' in pattern:
            matrix = pattern['matrix']
            stats['matrix_size'] = f"{len(matrix)}x{len(matrix[0])}"
            stats['unique_patterns'] = len(set(
                cell for row in matrix for cell in row if cell > 0
            ))

        return stats

    @staticmethod
    def print_pattern_stats(pattern: Dict) -> None:
        """Print pattern statistics in a formatted way."""
        stats = KolamUtils.get_pattern_stats(pattern)

        print("\n" + "="*50)
        print(f"📊 KOLAM PATTERN STATISTICS")
        print("="*50)
        print(f"ID: {stats['id']}")
        print(f"Name: {stats['name']}")
        print(f"Dimensions: {stats['dimensions'].get('width', 'N/A')}x{stats['dimensions'].get('height', 'N/A')}")
        if 'matrix_size' in stats:
            print(f"Matrix Size: {stats['matrix_size']}")
            print(f"Unique Patterns: {stats['unique_patterns']}")
        print(f"Dots: {stats['num_dots']}")
        print(f"Curves: {stats['num_curves']}")
        print(f"Total Curve Points: {stats['total_curve_points']}")
        print("="*50)

    @staticmethod
    def scale_pattern(pattern: Dict, scale_factor: float) -> Dict:
        """Scale a kolam pattern by a given factor."""
        scaled_pattern = pattern.copy()

        # Scale dimensions
        if 'dimensions' in pattern:
            scaled_pattern['dimensions'] = {
                'width': pattern['dimensions']['width'] * scale_factor,
                'height': pattern['dimensions']['height'] * scale_factor
            }

        # Scale dots
        scaled_dots = []
        for dot in pattern.get('dots', []):
            scaled_dot = dot.copy()
            scaled_dot['center'] = {
                'x': dot['center']['x'] * scale_factor,
                'y': dot['center']['y'] * scale_factor
            }
            if 'radius' in dot:
                scaled_dot['radius'] = dot['radius'] * scale_factor
            scaled_dots.append(scaled_dot)
        scaled_pattern['dots'] = scaled_dots

        # Scale curves
        scaled_curves = []
        for curve in pattern.get('curves', []):
            scaled_curve = curve.copy()
            scaled_points = []
            for point in curve.get('points', []):
                scaled_points.append({
                    'x': point['x'] * scale_factor,
                    'y': point['y'] * scale_factor
                })
            scaled_curve['points'] = scaled_points
            scaled_curves.append(scaled_curve)
        scaled_pattern['curves'] = scaled_curves

        return scaled_pattern

    @staticmethod
    def translate_pattern(pattern: Dict, dx: float, dy: float) -> Dict:
        """Translate a kolam pattern by dx, dy."""
        translated_pattern = pattern.copy()

        # Translate dots
        translated_dots = []
        for dot in pattern.get('dots', []):
            translated_dot = dot.copy()
            translated_dot['center'] = {
                'x': dot['center']['x'] + dx,
                'y': dot['center']['y'] + dy
            }
            translated_dots.append(translated_dot)
        translated_pattern['dots'] = translated_dots

        # Translate curves
        translated_curves = []
        for curve in pattern.get('curves', []):
            translated_curve = curve.copy()
            translated_points = []
            for point in curve.get('points', []):
                translated_points.append({
                    'x': point['x'] + dx,
                    'y': point['y'] + dy
                })
            translated_curve['points'] = translated_points
            translated_curves.append(translated_curve)
        translated_pattern['curves'] = translated_curves

        return translated_pattern

    @staticmethod
    def get_pattern_bounds(pattern: Dict) -> Tuple[float, float, float, float]:
        """Get the bounding box of a pattern (min_x, min_y, max_x, max_y)."""
        all_x = []
        all_y = []

        # Collect all coordinates
        for dot in pattern.get('dots', []):
            all_x.append(dot['center']['x'])
            all_y.append(dot['center']['y'])

        for curve in pattern.get('curves', []):
            for point in curve.get('points', []):
                all_x.append(point['x'])
                all_y.append(point['y'])

        if not all_x or not all_y:
            return 0, 0, 0, 0

        return min(all_x), min(all_y), max(all_x), max(all_y)

    @staticmethod
    def center_pattern(pattern: Dict) -> Dict:
        """Center a pattern around the origin."""
        min_x, min_y, max_x, max_y = KolamUtils.get_pattern_bounds(pattern)
        center_x = (min_x + max_x) / 2
        center_y = (min_y + max_y) / 2

        return KolamUtils.translate_pattern(pattern, -center_x, -center_y)

    @staticmethod
    def create_pattern_data_file():
        """Create the kolamPatternsData.json file from the provided data."""
        pattern_data = {
            "description": "Kolam curve patterns extracted",
            "extractedAt": "2025-01-19T12:00:00.000Z",
            "totalPatterns": 16,
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
                        {
                            "x": 0,
                            "y": -0.5
                        },
                        {
                            "x": 0.0081,
                            "y": -0.4853
                        },
                        {
                            "x": 0.0165,
                            "y": -0.4706
                        },
                        {
                            "x": 0.0252,
                            "y": -0.4559
                        },
                        {
                            "x": 0.0342,
                            "y": -0.4412
                        },
                        {
                            "x": 0.0434,
                            "y": -0.4265
                        },
                        {
                            "x": 0.0528,
                            "y": -0.4118
                        },
                        {
                            "x": 0.0624,
                            "y": -0.3971
                        },
                        {
                            "x": 0.0721,
                            "y": -0.3824
                        },
                        {
                            "x": 0.0818,
                            "y": -0.3677
                        },
                        {
                            "x": 0.0916,
                            "y": -0.353
                        },
                        {
                            "x": 0.1014,
                            "y": -0.3383
                        },
                        {
                            "x": 0.1112,
                            "y": -0.3236
                        },
                        {
                            "x": 0.121,
                            "y": -0.3089
                        },
                        {
                            "x": 0.1306,
                            "y": -0.2942
                        },
                        {
                            "x": 0.1402,
                            "y": -0.2794
                        },
                        {
                            "x": 0.1495,
                            "y": -0.2647
                        },
                        {
                            "x": 0.1587,
                            "y": -0.25
                        },
                        {
                            "x": 0.1676,
                            "y": -0.2353
                        },
                        {
                            "x": 0.1763,
                            "y": -0.2206
                        },
                        {
                            "x": 0.1846,
                            "y": -0.2059
                        },
                        {
                            "x": 0.1926,
                            "y": -0.1912
                        },
                        {
                            "x": 0.2003,
                            "y": -0.1765
                        },
                        {
                            "x": 0.2075,
                            "y": -0.1618
                        },
                        {
                            "x": 0.2143,
                            "y": -0.1471
                        },
                        {
                            "x": 0.2206,
                            "y": -0.1324
                        },
                        {
                            "x": 0.2264,
                            "y": -0.1177
                        },
                        {
                            "x": 0.2317,
                            "y": -0.103
                        },
                        {
                            "x": 0.2363,
                            "y": -0.0883
                        },
                        {
                            "x": 0.2404,
                            "y": -0.0736
                        },
                        {
                            "x": 0.2437,
                            "y": -0.0589
                        },
                        {
                            "x": 0.2464,
                            "y": -0.0442
                        },
                        {
                            "x": 0.2484,
                            "y": -0.0295
                        },
                        {
                            "x": 0.2496,
                            "y": -0.0148
                        },
                        {
                            "x": 0.25,
                            "y": -0.0001
                        },
                        {
                            "x": 0.2496,
                            "y": 0.0146
                        },
                        {
                            "x": 0.2483,
                            "y": 0.0293
                        },
                        {
                            "x": 0.2461,
                            "y": 0.044
                        },
                        {
                            "x": 0.243,
                            "y": 0.0587
                        },
                        {
                            "x": 0.239,
                            "y": 0.0734
                        },
                        {
                            "x": 0.2339,
                            "y": 0.0881
                        },
                        {
                            "x": 0.2279,
                            "y": 0.1028
                        },
                        {
                            "x": 0.2206,
                            "y": 0.1175
                        },
                        {
                            "x": 0.2122,
                            "y": 0.1322
                        },
                        {
                            "x": 0.2023,
                            "y": 0.1469
                        },
                        {
                            "x": 0.1907,
                            "y": 0.1617
                        },
                        {
                            "x": 0.1772,
                            "y": 0.1764
                        },
                        {
                            "x": 0.1612,
                            "y": 0.1911
                        },
                        {
                            "x": 0.142,
                            "y": 0.2058
                        },
                        {
                            "x": 0.1179,
                            "y": 0.2205
                        },
                        {
                            "x": 0.0848,
                            "y": 0.2352
                        },
                        {
                            "x": 0.008,
                            "y": 0.2499
                        },
                        {
                            "x": -0.008,
                            "y": 0.2499
                        },
                        {
                            "x": -0.0848,
                            "y": 0.2352
                        },
                        {
                            "x": -0.1179,
                            "y": 0.2205
                        },
                        {
                            "x": -0.142,
                            "y": 0.2058
                        },
                        {
                            "x": -0.1612,
                            "y": 0.1911
                        },
                        {
                            "x": -0.1772,
                            "y": 0.1764
                        },
                        {
                            "x": -0.1907,
                            "y": 0.1617
                        },
                        {
                            "x": -0.2023,
                            "y": 0.1469
                        },
                        {
                            "x": -0.2122,
                            "y": 0.1322
                        },
                        {
                            "x": -0.2206,
                            "y": 0.1175
                        },
                        {
                            "x": -0.2279,
                            "y": 0.1028
                        },
                        {
                            "x": -0.2339,
                            "y": 0.0881
                        },
                        {
                            "x": -0.239,
                            "y": 0.0734
                        },
                        {
                            "x": -0.243,
                            "y": 0.0587
                        },
                        {
                            "x": -0.2461,
                            "y": 0.044
                        },
                        {
                            "x": -0.2483,
                            "y": 0.0293
                        },
                        {
                            "x": -0.2496,
                            "y": 0.0146
                        },
                        {
                            "x": -0.25,
                            "y": -0.0001
                        },
                        {
                            "x": -0.2496,
                            "y": -0.0148
                        },
                        {
                            "x": -0.2484,
                            "y": -0.0295
                        },
                        {
                            "x": -0.2464,
                            "y": -0.0442
                        },
                        {
                            "x": -0.2437,
                            "y": -0.0589
                        },
                        {
                            "x": -0.2404,
                            "y": -0.0736
                        },
                        {
                            "x": -0.2363,
                            "y": -0.0883
                        },
                        {
                            "x": -0.2317,
                            "y": -0.103
                        },
                        {
                            "x": -0.2264,
                            "y": -0.1177
                        },
                        {
                            "x": -0.2206,
                            "y": -0.1324
                        },
                        {
                            "x": -0.2143,
                            "y": -0.1471
                        },
                        {
                            "x": -0.2075,
                            "y": -0.1618
                        },
                        {
                            "x": -0.2003,
                            "y": -0.1765
                        },
                        {
                            "x": -0.1926,
                            "y": -0.1912
                        },
                        {
                            "x": -0.1846,
                            "y": -0.2059
                        },
                        {
                            "x": -0.1763,
                            "y": -0.2206
                        },
                        {
                            "x": -0.1676,
                            "y": -0.2353
                        },
                        {
                            "x": -0.1587,
                            "y": -0.25
                        },
                        {
                            "x": -0.1495,
                            "y": -0.2647
                        },
                        {
                            "x": -0.1402,
                            "y": -0.2794
                        },
                        {
                            "x": -0.1306,
                            "y": -0.2942
                        },
                        {
                            "x": -0.121,
                            "y": -0.3089
                        },
                        {
                            "x": -0.1112,
                            "y": -0.3236
                        },
                        {
                            "x": -0.1014,
                            "y": -0.3383
                        },
                        {
                            "x": -0.0916,
                            "y": -0.353
                        },
                        {
                            "x": -0.0818,
                            "y": -0.3677
                        },
                        {
                            "x": -0.0721,
                            "y": -0.3824
                        },
                        {
                            "x": -0.0624,
                            "y": -0.3971
                        },
                        {
                            "x": -0.0528,
                            "y": -0.4118
                        },
                        {
                            "x": -0.0434,
                            "y": -0.4265
                        },
                        {
                            "x": -0.0342,
                            "y": -0.4412
                        },
                        {
                            "x": -0.0252,
                            "y": -0.4559
                        },
                        {
                            "x": -0.0165,
                            "y": -0.4706
                        },
                        {
                            "x": -0.0081,
                            "y": -0.4853
                        },
                        {
                            "x": 0,
                            "y": -0.5
                        }
                    ],
                    "hasDownConnection": False,
                    "hasRightConnection": False
                },
                {
                    "id": 3,
                    "points": [
                        {
                            "x": 0.5,
                            "y": 0
                        },
                        {
                            "x": 0.4853,
                            "y": 0.0081
                        },
                        {
                            "x": 0.4706,
                            "y": 0.0165
                        },
                        {
                            "x": 0.4559,
                            "y": 0.0252
                        },
                        {
                            "x": 0.4412,
                            "y": 0.0342
                        },
                        {
                            "x": 0.4265,
                            "y": 0.0434
                        },
                        {
                            "x": 0.4118,
                            "y": 0.0528
                        },
                        {
                            "x": 0.3971,
                            "y": 0.0624
                        },
                        {
                            "x": 0.3824,
                            "y": 0.0721
                        },
                        {
                            "x": 0.3677,
                            "y": 0.0818
                        },
                        {
                            "x": 0.353,
                            "y": 0.0916
                        },
                        {
                            "x": 0.3383,
                            "y": 0.1014
                        },
                        {
                            "x": 0.3236,
                            "y": 0.1112
                        },
                        {
                            "x": 0.3089,
                            "y": 0.121
                        },
                        {
                            "x": 0.2942,
                            "y": 0.1306
                        },
                        {
                            "x": 0.2794,
                            "y": 0.1402
                        },
                        {
                            "x": 0.2647,
                            "y": 0.1495
                        },
                        {
                            "x": 0.25,
                            "y": 0.1587
                        },
                        {
                            "x": 0.2353,
                            "y": 0.1676
                        },
                        {
                            "x": 0.2206,
                            "y": 0.1763
                        },
                        {
                            "x": 0.2059,
                            "y": 0.1846
                        },
                        {
                            "x": 0.1912,
                            "y": 0.1926
                        },
                        {
                            "x": 0.1765,
                            "y": 0.2003
                        },
                        {
                            "x": 0.1618,
                            "y": 0.2075
                        },
                        {
                            "x": 0.1471,
                            "y": 0.2143
                        },
                        {
                            "x": 0.1324,
                            "y": 0.2206
                        },
                        {
                            "x": 0.1177,
                            "y": 0.2264
                        },
                        {
                            "x": 0.103,
                            "y": 0.2317
                        },
                        {
                            "x": 0.0883,
                            "y": 0.2363
                        },
                        {
                            "x": 0.0736,
                            "y": 0.2404
                        },
                        {
                            "x": 0.0589,
                            "y": 0.2437
                        },
                        {
                            "x": 0.0442,
                            "y": 0.2464
                        },
                        {
                            "x": 0.0295,
                            "y": 0.2484
                        },
                        {
                            "x": 0.0148,
                            "y": 0.2496
                        },
                        {
                            "x": 0.0001,
                            "y": 0.25
                        },
                        {
                            "x": -0.0146,
                            "y": 0.2496
                        },
                        {
                            "x": -0.0293,
                            "y": 0.2483
                        },
                        {
                            "x": -0.044,
                            "y": 0.2461
                        },
                        {
                            "x": -0.0587,
                            "y": 0.243
                        },
                        {
                            "x": -0.0734,
                            "y": 0.239
                        },
                        {
                            "x": -0.0881,
                            "y": 0.2339
                        },
                        {
                            "x": -0.1028,
                            "y": 0.2279
                        },
                        {
                            "x": -0.1175,
                            "y": 0.2206
                        },
                        {
                            "x": -0.1322,
                            "y": 0.2122
                        },
                        {
                            "x": -0.1469,
                            "y": 0.2023
                        },
                        {
                            "x": -0.1617,
                            "y": 0.1907
                        },
                        {
                            "x": -0.1764,
                            "y": 0.1772
                        },
                        {
                            "x": -0.1911,
                            "y": 0.1612
                        },
                        {
                            "x": -0.2058,
                            "y": 0.142
                        },
                        {
                            "x": -0.2205,
                            "y": 0.1179
                        },
                        {
                            "x": -0.2352,
                            "y": 0.0848
                        },
                        {
                            "x": -0.2499,
                            "y": 0.008
                        },
                        {
                            "x": -0.2499,
                            "y": -0.008
                        },
                        {
                            "x": -0.2352,
                            "y": -0.0848
                        },
                        {
                            "x": -0.2205,
                            "y": -0.1179
                        },
                        {
                            "x": -0.2058,
                            "y": -0.142
                        },
                        {
                            "x": -0.1911,
                            "y": -0.1612
                        },
                        {
                            "x": -0.1764,
                            "y": -0.1772
                        },
                        {
                            "x": -0.1617,
                            "y": -0.1907
                        },
                        {
                            "x": -0.1469,
                            "y": -0.2023
                        },
                        {
                            "x": -0.1322,
                            "y": -0.2122
                        },
                        {
                            "x": -0.1175,
                            "y": -0.2206
                        },
                        {
                            "x": -0.1028,
                            "y": -0.2279
                        },
                        {
                            "x": -0.0881,
                            "y": -0.2339
                        },
                        {
                            "x": -0.0734,
                            "y": -0.239
                        },
                        {
                            "x": -0.0587,
                            "y": -0.243
                        },
                        {
                            "x": -0.044,
                            "y": -0.2461
                        },
                        {
                            "x": -0.0293,
                            "y": -0.2483
                        },
                        {
                            "x": -0.0146,
                            "y": -0.2496
                        },
                        {
                            "x": 0.0001,
                            "y": -0.25
                        },
                        {
                            "x": 0.0148,
                            "y": -0.2496
                        },
                        {
                            "x": 0.0295,
                            "y": -0.2484
                        },
                        {
                            "x": 0.0442,
                            "y": -0.2464
                        },
                        {
                            "x": 0.0589,
                            "y": -0.2437
                        },
                        {
                            "x": 0.0736,
                            "y": -0.2404
                        },
                        {
                            "x": 0.0883,
                            "y": -0.2363
                        },
                        {
                            "x": 0.103,
                            "y": -0.2317
                        },
                        {
                            "x": 0.1177,
                            "y": -0.2264
                        },
                        {
                            "x": 0.1324,
                            "y": -0.2206
                        },
                        {
                            "x": 0.1471,
                            "y": -0.2143
                        },
                        {
                            "x": 0.1618,
                            "y": -0.2075
                        },
                        {
                            "x": 0.1765,
                            "y": -0.2003
                        },
                        {
                            "x": 0.1912,
                            "y": -0.1926
                        },
                        {
                            "x": 0.2059,
                            "y": -0.1846
                        },
                        {
                            "x": 0.2206,
                            "y": -0.1763
                        },
                        {
                            "x": 0.2353,
                            "y": -0.1676
                        },
                        {
                            "x": 0.25,
                            "y": -0.1587
                        },
                        {
                            "x": 0.2647,
                            "y": -0.1495
                        },
                        {
                            "x": 0.2794,
                            "y": -0.1402
                        },
                        {
                            "x": 0.2942,
                            "y": -0.1306
                        },
                        {
                            "x": 0.3089,
                            "y": -0.121
                        },
                        {
                            "x": 0.3236,
                            "y": -0.1112
                        },
                        {
                            "x": 0.3383,
                            "y": -0.1014
                        },
                        {
                            "x": 0.353,
                            "y": -0.0916
                        },
                        {
                            "x": 0.3677,
                            "y": -0.0818
                        },
                        {
                            "x": 0.3824,
                            "y": -0.0721
                        },
                        {
                            "x": 0.3971,
                            "y": -0.0624
                        },
                        {
                            "x": 0.4118,
                            "y": -0.0528
                        },
                        {
                            "x": 0.4265,
                            "y": -0.0434
                        },
                        {
                            "x": 0.4412,
                            "y": -0.0342
                        },
                        {
                            "x": 0.4559,
                            "y": -0.0252
                        },
                        {
                            "x": 0.4706,
                            "y": -0.0165
                        },
                        {
                            "x": 0.4853,
                            "y": -0.0081
                        },
                        {
                            "x": 0.5,
                            "y": 0
                        }
                    ],
                    "hasDownConnection": False,
                    "hasRightConnection": True
                },
                {
                    "id": 4,
                    "points": [
                        {
                            "x": 0,
                            "y": 0.5
                        },
                        {
                            "x": -0.0081,
                            "y": 0.4853
                        },
                        {
                            "x": -0.0165,
                            "y": 0.4706
                        },
                        {
                            "x": -0.0252,
                            "y": 0.4559
                        },
                        {
                            "x": -0.0342,
                            "y": 0.4412
                        },
                        {
                            "x": -0.0434,
                            "y": 0.4265
                        },
                        {
                            "x": -0.0528,
                            "y": 0.4118
                        },
                        {
                            "x": -0.0624,
                            "y": 0.3971
                        },
                        {
                            "x": -0.0721,
                            "y": 0.3824
                        },
                        {
                            "x": -0.0818,
                            "y": 0.3677
                        },
                        {
                            "x": -0.0916,
                            "y": 0.353
                        },
                        {
                            "x": -0.1014,
                            "y": 0.3383
                        },
                        {
                            "x": -0.1112,
                            "y": 0.3236
                        },
                        {
                            "x": -0.121,
                            "y": 0.3089
                        },
                        {
                            "x": -0.1306,
                            "y": 0.2942
                        },
                        {
                            "x": -0.1402,
                            "y": 0.2794
                        },
                        {
                            "x": -0.1495,
                            "y": 0.2647
                        },
                        {
                            "x": -0.1587,
                            "y": 0.25
                        },
                        {
                            "x": -0.1676,
                            "y": 0.2353
                        },
                        {
                            "x": -0.1763,
                            "y": 0.2206
                        },
                        {
                            "x": -0.1846,
                            "y": 0.2059
                        },
                        {
                            "x": -0.1926,
                            "y": 0.1912
                        },
                        {
                            "x": -0.2003,
                            "y": 0.1765
                        },
                        {
                            "x": -0.2075,
                            "y": 0.1618
                        },
                        {
                            "x": -0.2143,
                            "y": 0.1471
                        },
                        {
                            "x": -0.2206,
                            "y": 0.1324
                        },
                        {
                            "x": -0.2264,
                            "y": 0.1177
                        },
                        {
                            "x": -0.2317,
                            "y": 0.103
                        },
                        {
                            "x": -0.2363,
                            "y": 0.0883
                        },
                        {
                            "x": -0.2404,
                            "y": 0.0736
                        },
                        {
                            "x": -0.2437,
                            "y": 0.0589
                        },
                        {
                            "x": -0.2464,
                            "y": 0.0442
                        },
                        {
                            "x": -0.2484,
                            "y": 0.0295
                        },
                        {
                            "x": -0.2496,
                            "y": 0.0148
                        },
                        {
                            "x": -0.25,
                            "y": 0.0001
                        },
                        {
                            "x": -0.2496,
                            "y": -0.0146
                        },
                        {
                            "x": -0.2483,
                            "y": -0.0293
                        },
                        {
                            "x": -0.2461,
                            "y": -0.044
                        },
                        {
                            "x": -0.243,
                            "y": -0.0587
                        },
                        {
                            "x": -0.239,
                            "y": -0.0734
                        },
                        {
                            "x": -0.2339,
                            "y": -0.0881
                        },
                        {
                            "x": -0.2279,
                            "y": -0.1028
                        },
                        {
                            "x": -0.2206,
                            "y": -0.1175
                        },
                        {
                            "x": -0.2122,
                            "y": -0.1322
                        },
                        {
                            "x": -0.2023,
                            "y": -0.1469
                        },
                        {
                            "x": -0.1907,
                            "y": -0.1617
                        },
                        {
                            "x": -0.1772,
                            "y": -0.1764
                        },
                        {
                            "x": -0.1612,
                            "y": -0.1911
                        },
                        {
                            "x": -0.142,
                            "y": -0.2058
                        },
                        {
                            "x": -0.1179,
                            "y": -0.2205
                        },
                        {
                            "x": -0.0848,
                            "y": -0.2352
                        },
                        {
                            "x": -0.008,
                            "y": -0.2499
                        },
                        {
                            "x": 0.008,
                            "y": -0.2499
                        },
                        {
                            "x": 0.0848,
                            "y": -0.2352
                        },
                        {
                            "x": 0.1179,
                            "y": -0.2205
                        },
                        {
                            "x": 0.142,
                            "y": -0.2058
                        },
                        {
                            "x": 0.1612,
                            "y": -0.1911
                        },
                        {
                            "x": 0.1772,
                            "y": -0.1764
                        },
                        {
                            "x": 0.1907,
                            "y": -0.1617
                        },
                        {
                            "x": 0.2023,
                            "y": -0.1469
                        },
                        {
                            "x": 0.2122,
                            "y": -0.1322
                        },
                        {
                            "x": 0.2206,
                            "y": -0.1175
                        },
                        {
                            "x": 0.2279,
                            "y": -0.1028
                        },
                        {
                            "x": 0.2339,
                            "y": -0.0881
                        },
                        {
                            "x": 0.239,
                            "y": -0.0734
                        },
                        {
                            "x": 0.243,
                            "y": -0.0587
                        },
                        {
                            "x": 0.2461,
                            "y": -0.044
                        },
                        {
                            "x": 0.2483,
                            "y": -0.0293
                        },
                        {
                            "x": 0.2496,
                            "y": -0.0146
                        },
                        {
                            "x": 0.25,
                            "y": 0.0001
                        },
                        {
                            "x": 0.2496,
                            "y": 0.0148
                        },
                        {
                            "x": 0.2484,
                            "y": 0.0295
                        },
                        {
                            "x": 0.2464,
                            "y": 0.0442
                        },
                        {
                            "x": 0.2437,
                            "y": 0.0589
                        },
                        {
                            "x": 0.2404,
                            "y": 0.0736
                        },
                        {
                            "x": 0.2363,
                            "y": 0.0883
                        },
                        {
                            "x": 0.2317,
                            "y": 0.103
                        },
                        {
                            "x": 0.2264,
                            "y": 0.1177
                        },
                        {
                            "x": 0.2206,
                            "y": 0.1324
                        },
                        {
                            "x": 0.2143,
                            "y": 0.1471
                        },
                        {
                            "x": 0.2075,
                            "y": 0.1618
                        },
                        {
                            "x": 0.2003,
                            "y": 0.1765
                        },
                        {
                            "x": 0.1926,
                            "y": 0.1912
                        },
                        {
                            "x": 0.1846,
                            "y": 0.2059
                        },
                        {
                            "x": 0.1763,
                            "y": 0.2206
                        },
                        {
                            "x": 0.1676,
                            "y": 0.2353
                        },
                        {
                            "x": 0.1587,
                            "y": 0.25
                        },
                        {
                            "x": 0.1495,
                            "y": 0.2647
                        },
                        {
                            "x": 0.1402,
                            "y": 0.2794
                        },
                        {
                            "x": 0.1306,
                            "y": 0.2942
                        },
                        {
                            "x": 0.121,
                            "y": 0.3089
                        },
                        {
                            "x": 0.1112,
                            "y": 0.3236
                        },
                        {
                            "x": 0.1014,
                            "y": 0.3383
                        },
                        {
                            "x": 0.0916,
                            "y": 0.353
                        },
                        {
                            "x": 0.0818,
                            "y": 0.3677
                        },
                        {
                            "x": 0.0721,
                            "y": 0.3824
                        },
                        {
                            "x": 0.0624,
                            "y": 0.3971
                        },
                        {
                            "x": 0.0528,
                            "y": 0.4118
                        },
                        {
                            "x": 0.0434,
                            "y": 0.4265
                        },
                        {
                            "x": 0.0342,
                            "y": 0.4412
                        },
                        {
                            "x": 0.0252,
                            "y": 0.4559
                        },
                        {
                            "x": 0.0165,
                            "y": 0.4706
                        },
                        {
                            "x": 0.0081,
                            "y": 0.4853
                        },
                        {
                            "x": 0,
                            "y": 0.5
                        }
                    ],
                    "hasDownConnection": True,
                    "hasRightConnection": False
                },
                {
                    "id": 5,
                    "points": [
                        {
                            "x": -0.5,
                            "y": 0
                        },
                        {
                            "x": -0.4853,
                            "y": -0.0081
                        },
                        {
                            "x": -0.4706,
                            "y": -0.0165
                        },
                        {
                            "x": -0.4559,
                            "y": -0.0252
                        },
                        {
                            "x": -0.4412,
                            "y": -0.0342
                        },
                        {
                            "x": -0.4265,
                            "y": -0.0434
                        },
                        {
                            "x": -0.4118,
                            "y": -0.0528
                        },
                        {
                            "x": -0.3971,
                            "y": -0.0624
                        },
                        {
                            "x": -0.3824,
                            "y": -0.0721
                        },
                        {
                            "x": -0.3677,
                            "y": -0.0818
                        },
                        {
                            "x": -0.353,
                            "y": -0.0916
                        },
                        {
                            "x": -0.3383,
                            "y": -0.1014
                        },
                        {
                            "x": -0.3236,
                            "y": -0.1112
                        },
                        {
                            "x": -0.3089,
                            "y": -0.121
                        },
                        {
                            "x": -0.2942,
                            "y": -0.1306
                        },
                        {
                            "x": -0.2794,
                            "y": -0.1402
                        },
                        {
                            "x": -0.2647,
                            "y": -0.1495
                        },
                        {
                            "x": -0.25,
                            "y": -0.1587
                        },
                        {
                            "x": -0.2353,
                            "y": -0.1676
                        },
                        {
                            "x": -0.2206,
                            "y": -0.1763
                        },
                        {
                            "x": -0.2059,
                            "y": -0.1846
                        },
                        {
                            "x": -0.1912,
                            "y": -0.1926
                        },
                        {
                            "x": -0.1765,
                            "y": -0.2003
                        },
                        {
                            "x": -0.1618,
                            "y": -0.2075
                        },
                        {
                            "x": -0.1471,
                            "y": -0.2143
                        },
                        {
                            "x": -0.1324,
                            "y": -0.2206
                        },
                        {
                            "x": -0.1177,
                            "y": -0.2264
                        },
                        {
                            "x": -0.103,
                            "y": -0.2317
                        },
                        {
                            "x": -0.0883,
                            "y": -0.2363
                        },
                        {
                            "x": -0.0736,
                            "y": -0.2404
                        },
                        {
                            "x": -0.0589,
                            "y": -0.2437
                        },
                        {
                            "x": -0.0442,
                            "y": -0.2464
                        },
                        {
                            "x": -0.0295,
                            "y": -0.2484
                        },
                        {
                            "x": -0.0148,
                            "y": -0.2496
                        },
                        {
                            "x": -0.0001,
                            "y": -0.25
                        },
                        {
                            "x": 0.0146,
                            "y": -0.2496
                        },
                        {
                            "x": 0.0293,
                            "y": -0.2483
                        },
                        {
                            "x": 0.044,
                            "y": -0.2461
                        },
                        {
                            "x": 0.0587,
                            "y": -0.243
                        },
                        {
                            "x": 0.0734,
                            "y": -0.239
                        },
                        {
                            "x": 0.0881,
                            "y": -0.2339
                        },
                        {
                            "x": 0.1028,
                            "y": -0.2279
                        },
                        {
                            "x": 0.1175,
                            "y": -0.2206
                        },
                        {
                            "x": 0.1322,
                            "y": -0.2122
                        },
                        {
                            "x": 0.1469,
                            "y": -0.2023
                        },
                        {
                            "x": 0.1617,
                            "y": -0.1907
                        },
                        {
                            "x": 0.1764,
                            "y": -0.1772
                        },
                        {
                            "x": 0.1911,
                            "y": -0.1612
                        },
                        {
                            "x": 0.2058,
                            "y": -0.142
                        },
                        {
                            "x": 0.2205,
                            "y": -0.1179
                        },
                        {
                            "x": 0.2352,
                            "y": -0.0848
                        },
                        {
                            "x": 0.2499,
                            "y": -0.008
                        },
                        {
                            "x": 0.2499,
                            "y": 0.008
                        },
                        {
                            "x": 0.2352,
                            "y": 0.0848
                        },
                        {
                            "x": 0.2205,
                            "y": 0.1179
                        },
                        {
                            "x": 0.2058,
                            "y": 0.142
                        },
                        {
                            "x": 0.1911,
                            "y": 0.1612
                        },
                        {
                            "x": 0.1764,
                            "y": 0.1772
                        },
                        {
                            "x": 0.1617,
                            "y": 0.1907
                        },
                        {
                            "x": 0.1469,
                            "y": 0.2023
                        },
                        {
                            "x": 0.1322,
                            "y": 0.2122
                        },
                        {
                            "x": 0.1175,
                            "y": 0.2206
                        },
                        {
                            "x": 0.1028,
                            "y": 0.2279
                        },
                        {
                            "x": 0.0881,
                            "y": 0.2339
                        },
                        {
                            "x": 0.0734,
                            "y": 0.239
                        },
                        {
                            "x": 0.0587,
                            "y": 0.243
                        },
                        {
                            "x": 0.044,
                            "y": 0.2461
                        },
                        {
                            "x": 0.0293,
                            "y": 0.2483
                        },
                        {
                            "x": 0.0146,
                            "y": 0.2496
                        },
                        {
                            "x": -0.0001,
                            "y": 0.25
                        },
                        {
                            "x": -0.0148,
                            "y": 0.2496
                        },
                        {
                            "x": -0.0295,
                            "y": 0.2484
                        },
                        {
                            "x": -0.0442,
                            "y": 0.2464
                        },
                        {
                            "x": -0.0589,
                            "y": 0.2437
                        },
                        {
                            "x": -0.0736,
                            "y": 0.2404
                        },
                        {
                            "x": -0.0883,
                            "y": 0.2363
                        },
                        {
                            "x": -0.103,
                            "y": 0.2317
                        },
                        {
                            "x": -0.1177,
                            "y": 0.2264
                        },
                        {
                            "x": -0.1324,
                            "y": 0.2206
                        },
                        {
                            "x": -0.1471,
                            "y": 0.2143
                        },
                        {
                            "x": -0.1618,
                            "y": 0.2075
                        },
                        {
                            "x": -0.1765,
                            "y": 0.2003
                        },
                        {
                            "x": -0.1912,
                            "y": 0.1926
                        },
                        {
                            "x": -0.2059,
                            "y": 0.1846
                        },
                        {
                            "x": -0.2206,
                            "y": 0.1763
                        },
                        {
                            "x": -0.2353,
                            "y": 0.1676
                        },
                        {
                            "x": -0.25,
                            "y": 0.1587
                        },
                        {
                            "x": -0.2647,
                            "y": 0.1495
                        },
                        {
                            "x": -0.2794,
                            "y": 0.1402
                        },
                        {
                            "x": -0.2942,
                            "y": 0.1306
                        },
                        {
                            "x": -0.3089,
                            "y": 0.121
                        },
                        {
                            "x": -0.3236,
                            "y": 0.1112
                        },
                        {
                            "x": -0.3383,
                            "y": 0.1014
                        },
                        {
                            "x": -0.353,
                            "y": 0.0916
                        },
                        {
                            "x": -0.3677,
                            "y": 0.0818
                        },
                        {
                            "x": -0.3824,
                            "y": 0.0721
                        },
                        {
                            "x": -0.3971,
                            "y": 0.0624
                        },
                        {
                            "x": -0.4118,
                            "y": 0.0528
                        },
                        {
                            "x": -0.4265,
                            "y": 0.0434
                        },
                        {
                            "x": -0.4412,
                            "y": 0.0342
                        },
                        {
                            "x": -0.4559,
                            "y": 0.0252
                        },
                        {
                            "x": -0.4706,
                            "y": 0.0165
                        },
                        {
                            "x": -0.4853,
                            "y": 0.0081
                        },
                        {
                            "x": -0.5,
                            "y": 0
                        }
                    ],
                    "hasDownConnection": False,
                    "hasRightConnection": False
                },
                {
                    "id": 6,
                    "points": [
                        {
                            "x": 0,
                            "y": -0.5
                        },
                        {
                            "x": -0.0298,
                            "y": -0.4498
                        },
                        {
                            "x": -0.0579,
                            "y": -0.4013
                        },
                        {
                            "x": -0.0843,
                            "y": -0.3544
                        },
                        {
                            "x": -0.1091,
                            "y": -0.3092
                        },
                        {
                            "x": -0.1322,
                            "y": -0.2657
                        },
                        {
                            "x": -0.1537,
                            "y": -0.2239
                        },
                        {
                            "x": -0.1735,
                            "y": -0.1837
                        },
                        {
                            "x": -0.1916,
                            "y": -0.1451
                        },
                        {
                            "x": -0.208,
                            "y": -0.1083
                        },
                        {
                            "x": -0.2228,
                            "y": -0.0731
                        },
                        {
                            "x": -0.2359,
                            "y": -0.0396
                        },
                        {
                            "x": -0.2474,
                            "y": -0.0077
                        },
                        {
                            "x": -0.2572,
                            "y": 0.0225
                        },
                        {
                            "x": -0.2653,
                            "y": 0.051
                        },
                        {
                            "x": -0.2718,
                            "y": 0.0779
                        },
                        {
                            "x": -0.2766,
                            "y": 0.1031
                        },
                        {
                            "x": -0.2797,
                            "y": 0.1266
                        },
                        {
                            "x": -0.2811,
                            "y": 0.1485
                        },
                        {
                            "x": -0.2809,
                            "y": 0.1687
                        },
                        {
                            "x": -0.2791,
                            "y": 0.1872
                        },
                        {
                            "x": -0.2755,
                            "y": 0.2041
                        },
                        {
                            "x": -0.2703,
                            "y": 0.2193
                        },
                        {
                            "x": -0.2634,
                            "y": 0.2328
                        },
                        {
                            "x": -0.2549,
                            "y": 0.2447
                        },
                        {
                            "x": -0.2447,
                            "y": 0.2549
                        },
                        {
                            "x": -0.2328,
                            "y": 0.2634
                        },
                        {
                            "x": -0.2193,
                            "y": 0.2703
                        },
                        {
                            "x": -0.2041,
                            "y": 0.2755
                        },
                        {
                            "x": -0.1872,
                            "y": 0.2791
                        },
                        {
                            "x": -0.1687,
                            "y": 0.2809
                        },
                        {
                            "x": -0.1485,
                            "y": 0.2811
                        },
                        {
                            "x": -0.1266,
                            "y": 0.2797
                        },
                        {
                            "x": -0.1031,
                            "y": 0.2766
                        },
                        {
                            "x": -0.0779,
                            "y": 0.2718
                        },
                        {
                            "x": -0.051,
                            "y": 0.2653
                        },
                        {
                            "x": -0.0225,
                            "y": 0.2572
                        },
                        {
                            "x": 0.0077,
                            "y": 0.2474
                        },
                        {
                            "x": 0.0396,
                            "y": 0.2359
                        },
                        {
                            "x": 0.0731,
                            "y": 0.2228
                        },
                        {
                            "x": 0.1083,
                            "y": 0.208
                        },
                        {
                            "x": 0.1451,
                            "y": 0.1916
                        },
                        {
                            "x": 0.1837,
                            "y": 0.1735
                        },
                        {
                            "x": 0.2239,
                            "y": 0.1537
                        },
                        {
                            "x": 0.2657,
                            "y": 0.1322
                        },
                        {
                            "x": 0.3092,
                            "y": 0.1091
                        },
                        {
                            "x": 0.3544,
                            "y": 0.0843
                        },
                        {
                            "x": 0.4013,
                            "y": 0.0579
                        },
                        {
                            "x": 0.4498,
                            "y": 0.0298
                        },
                        {
                            "x": 0.5,
                            "y": 0
                        },
                        {
                            "x": 0,
                            "y": -0.5
                        }
                    ],
                    "hasDownConnection": False,
                    "hasRightConnection": False
                },
                {
                    "id": 7,
                    "points": [
                        {
                            "x": 0.5,
                            "y": 0
                        },
                        {
                            "x": 0.4498,
                            "y": -0.0298
                        },
                        {
                            "x": 0.4013,
                            "y": -0.0579
                        },
                        {
                            "x": 0.3544,
                            "y": -0.0843
                        },
                        {
                            "x": 0.3092,
                            "y": -0.1091
                        },
                        {
                            "x": 0.2657,
                            "y": -0.1322
                        },
                        {
                            "x": 0.2239,
                            "y": -0.1537
                        },
                        {
                            "x": 0.1837,
                            "y": -0.1735
                        },
                        {
                            "x": 0.1451,
                            "y": -0.1916
                        },
                        {
                            "x": 0.1083,
                            "y": -0.208
                        },
                        {
                            "x": 0.0731,
                            "y": -0.2228
                        },
                        {
                            "x": 0.0396,
                            "y": -0.2359
                        },
                        {
                            "x": 0.0077,
                            "y": -0.2474
                        },
                        {
                            "x": -0.0225,
                            "y": -0.2572
                        },
                        {
                            "x": -0.051,
                            "y": -0.2653
                        },
                        {
                            "x": -0.0779,
                            "y": -0.2718
                        },
                        {
                            "x": -0.1031,
                            "y": -0.2766
                        },
                        {
                            "x": -0.1266,
                            "y": -0.2797
                        },
                        {
                            "x": -0.1485,
                            "y": -0.2811
                        },
                        {
                            "x": -0.1687,
                            "y": -0.2809
                        },
                        {
                            "x": -0.1872,
                            "y": -0.2791
                        },
                        {
                            "x": -0.2041,
                            "y": -0.2755
                        },
                        {
                            "x": -0.2193,
                            "y": -0.2703
                        },
                        {
                            "x": -0.2328,
                            "y": -0.2634
                        },
                        {
                            "x": -0.2447,
                            "y": -0.2549
                        },
                        {
                            "x": -0.2549,
                            "y": -0.2447
                        },
                        {
                            "x": -0.2634,
                            "y": -0.2328
                        },
                        {
                            "x": -0.2703,
                            "y": -0.2193
                        },
                        {
                            "x": -0.2755,
                            "y": -0.2041
                        },
                        {
                            "x": -0.2791,
                            "y": -0.1872
                        },
                        {
                            "x": -0.2809,
                            "y": -0.1687
                        },
                        {
                            "x": -0.2811,
                            "y": -0.1485
                        },
                        {
                            "x": -0.2797,
                            "y": -0.1266
                        },
                        {
                            "x": -0.2766,
                            "y": -0.1031
                        },
                        {
                            "x": -0.2718,
                            "y": -0.0779
                        },
                        {
                            "x": -0.2653,
                            "y": -0.051
                        },
                        {
                            "x": -0.2572,
                            "y": -0.0225
                        },
                        {
                            "x": -0.2474,
                            "y": 0.0077
                        },
                        {
                            "x": -0.2359,
                            "y": 0.0396
                        },
                        {
                            "x": -0.2228,
                            "y": 0.0731
                        },
                        {
                            "x": -0.208,
                            "y": 0.1083
                        },
                        {
                            "x": -0.1916,
                            "y": 0.1451
                        },
                        {
                            "x": -0.1735,
                            "y": 0.1837
                        },
                        {
                            "x": -0.1537,
                            "y": 0.2239
                        },
                        {
                            "x": -0.1322,
                            "y": 0.2657
                        },
                        {
                            "x": -0.1091,
                            "y": 0.3092
                        },
                        {
                            "x": -0.0843,
                            "y": 0.3544
                        },
                        {
                            "x": -0.0579,
                            "y": 0.4013
                        },
                        {
                            "x": -0.0298,
                            "y": 0.4498
                        },
                        {
                            "x": 0,
                            "y": 0.5
                        },
                        {
                            "x": 0.5,
                            "y": 0
                        }
                    ],
                    "hasDownConnection": False,
                    "hasRightConnection": True
                },
                {
                    "id": 8,
                    "points": [
                        {
                            "x": 0,
                            "y": 0.5
                        },
                        {
                            "x": 0.0298,
                            "y": 0.4498
                        },
                        {
                            "x": 0.0579,
                            "y": 0.4013
                        },
                        {
                            "x": 0.0843,
                            "y": 0.3544
                        },
                        {
                            "x": 0.1091,
                            "y": 0.3092
                        },
                        {
                            "x": 0.1322,
                            "y": 0.2657
                        },
                        {
                            "x": 0.1537,
                            "y": 0.2239
                        },
                        {
                            "x": 0.1735,
                            "y": 0.1837
                        },
                        {
                            "x": 0.1916,
                            "y": 0.1451
                        },
                        {
                            "x": 0.208,
                            "y": 0.1083
                        },
                        {
                            "x": 0.2228,
                            "y": 0.0731
                        },
                        {
                            "x": 0.2359,
                            "y": 0.0396
                        },
                        {
                            "x": 0.2474,
                            "y": 0.0077
                        },
                        {
                            "x": 0.2572,
                            "y": -0.0225
                        },
                        {
                            "x": 0.2653,
                            "y": -0.051
                        },
                        {
                            "x": 0.2718,
                            "y": -0.0779
                        },
                        {
                            "x": 0.2766,
                            "y": -0.1031
                        },
                        {
                            "x": 0.2797,
                            "y": -0.1266
                        },
                        {
                            "x": 0.2811,
                            "y": -0.1485
                        },
                        {
                            "x": 0.2809,
                            "y": -0.1687
                        },
                        {
                            "x": 0.2791,
                            "y": -0.1872
                        },
                        {
                            "x": 0.2755,
                            "y": -0.2041
                        },
                        {
                            "x": 0.2703,
                            "y": -0.2193
                        },
                        {
                            "x": 0.2634,
                            "y": -0.2328
                        },
                        {
                            "x": 0.2549,
                            "y": -0.2447
                        },
                        {
                            "x": 0.2447,
                            "y": -0.2549
                        },
                        {
                            "x": 0.2328,
                            "y": -0.2634
                        },
                        {
                            "x": 0.2193,
                            "y": -0.2703
                        },
                        {
                            "x": 0.2041,
                            "y": -0.2755
                        },
                        {
                            "x": 0.1872,
                            "y": -0.2791
                        },
                        {
                            "x": 0.1687,
                            "y": -0.2809
                        },
                        {
                            "x": 0.1485,
                            "y": -0.2811
                        },
                        {
                            "x": 0.1266,
                            "y": -0.2797
                        },
                        {
                            "x": 0.1031,
                            "y": -0.2766
                        },
                        {
                            "x": 0.0779,
                            "y": -0.2718
                        },
                        {
                            "x": 0.051,
                            "y": -0.2653
                        },
                        {
                            "x": 0.0225,
                            "y": -0.2572
                        },
                        {
                            "x": -0.0077,
                            "y": -0.2474
                        },
                        {
                            "x": -0.0396,
                            "y": -0.2359
                        },
                        {
                            "x": -0.0731,
                            "y": -0.2228
                        },
                        {
                            "x": -0.1083,
                            "y": -0.208
                        },
                        {
                            "x": -0.1451,
                            "y": -0.1916
                        },
                        {
                            "x": -0.1837,
                            "y": -0.1735
                        },
                        {
                            "x": -0.2239,
                            "y": -0.1537
                        },
                        {
                            "x": -0.2657,
                            "y": -0.1322
                        },
                        {
                            "x": -0.3092,
                            "y": -0.1091
                        },
                        {
                            "x": -0.3544,
                            "y": -0.0843
                        },
                        {
                            "x": -0.4013,
                            "y": -0.0579
                        },
                        {
                            "x": -0.4498,
                            "y": -0.0298
                        },
                        {
                            "x": -0.5,
                            "y": 0
                        },
                        {
                            "x": 0,
                            "y": 0.5
                        }
                    ],
                    "hasDownConnection": True,
                    "hasRightConnection": False
                },
                {
                    "id": 9,
                    "points": [
                        {
                            "x": -0.5,
                            "y": 0
                        },
                        {
                            "x": -0.4498,
                            "y": 0.0298
                        },
                        {
                            "x": -0.4013,
                            "y": 0.0579
                        },
                        {
                            "x": -0.3544,
                            "y": 0.0843
                        },
                        {
                            "x": -0.3092,
                            "y": 0.1091
                        },
                        {
                            "x": -0.2657,
                            "y": 0.1322
                        },
                        {
                            "x": -0.2239,
                            "y": 0.1537
                        },
                        {
                            "x": -0.1837,
                            "y": 0.1735
                        },
                        {
                            "x": -0.1451,
                            "y": 0.1916
                        },
                        {
                            "x": -0.1083,
                            "y": 0.208
                        },
                        {
                            "x": -0.0731,
                            "y": 0.2228
                        },
                        {
                            "x": -0.0396,
                            "y": 0.2359
                        },
                        {
                            "x": -0.0077,
                            "y": 0.2474
                        },
                        {
                            "x": 0.0225,
                            "y": 0.2572
                        },
                        {
                            "x": 0.051,
                            "y": 0.2653
                        },
                        {
                            "x": 0.0779,
                            "y": 0.2718
                        },
                        {
                            "x": 0.1031,
                            "y": 0.2766
                        },
                        {
                            "x": 0.1266,
                            "y": 0.2797
                        },
                        {
                            "x": 0.1485,
                            "y": 0.2811
                        },
                        {
                            "x": 0.1687,
                            "y": 0.2809
                        },
                        {
                            "x": 0.1872,
                            "y": 0.2791
                        },
                        {
                            "x": 0.2041,
                            "y": 0.2755
                        },
                        {
                            "x": 0.2193,
                            "y": 0.2703
                        },
                        {
                            "x": 0.2328,
                            "y": 0.2634
                        },
                        {
                            "x": 0.2447,
                            "y": 0.2549
                        },
                        {
                            "x": 0.2549,
                            "y": 0.2447
                        },
                        {
                            "x": 0.2634,
                            "y": 0.2328
                        },
                        {
                            "x": 0.2703,
                            "y": 0.2193
                        },
                        {
                            "x": 0.2755,
                            "y": 0.2041
                        },
                        {
                            "x": 0.2791,
                            "y": 0.1872
                        },
                        {
                            "x": 0.2809,
                            "y": 0.1687
                        },
                        {
                            "x": 0.2811,
                            "y": 0.1485
                        },
                        {
                            "x": 0.2797,
                            "y": 0.1266
                        },
                        {
                            "x": 0.2766,
                            "y": 0.1031
                        },
                        {
                            "x": 0.2718,
                            "y": 0.0779
                        },
                        {
                            "x": 0.2653,
                            "y": 0.051
                        },
                        {
                            "x": 0.2572,
                            "y": 0.0225
                        },
                        {
                            "x": 0.2474,
                            "y": -0.0077
                        },
                        {
                            "x": 0.2359,
                            "y": -0.0396
                        },
                        {
                            "x": 0.2228,
                            "y": -0.0731
                        },
                        {
                            "x": 0.208,
                            "y": -0.1083
                        },
                        {
                            "x": 0.1916,
                            "y": -0.1451
                        },
                        {
                            "x": 0.1735,
                            "y": -0.1837
                        },
                        {
                            "x": 0.1537,
                            "y": -0.2239
                        },
                        {
                            "x": 0.1322,
                            "y": -0.2657
                        },
                        {
                            "x": 0.1091,
                            "y": -0.3092
                        },
                        {
                            "x": 0.0843,
                            "y": -0.3544
                        },
                        {
                            "x": 0.0579,
                            "y": -0.4013
                        },
                        {
                            "x": 0.0298,
                            "y": -0.4498
                        },
                        {
                            "x": 0,
                            "y": -0.5
                        },
                        {
                            "x": -0.5,
                            "y": 0
                        }
                    ],
                    "hasDownConnection": False,
                    "hasRightConnection": False
                },
                {
                    "id": 10,
                    "points": [
                        {
                            "x": -0.5,
                            "y": 0
                        },
                        {
                            "x": -0.4796,
                            "y": 0.02
                        },
                        {
                            "x": -0.4592,
                            "y": 0.0392
                        },
                        {
                            "x": -0.4388,
                            "y": 0.0575
                        },
                        {
                            "x": -0.4184,
                            "y": 0.075
                        },
                        {
                            "x": -0.398,
                            "y": 0.0916
                        },
                        {
                            "x": -0.3776,
                            "y": 0.1075
                        },
                        {
                            "x": -0.3571,
                            "y": 0.1224
                        },
                        {
                            "x": -0.3367,
                            "y": 0.1366
                        },
                        {
                            "x": -0.3163,
                            "y": 0.1499
                        },
                        {
                            "x": -0.2959,
                            "y": 0.1624
                        },
                        {
                            "x": -0.2755,
                            "y": 0.1741
                        },
                        {
                            "x": -0.2551,
                            "y": 0.1849
                        },
                        {
                            "x": -0.2347,
                            "y": 0.1949
                        },
                        {
                            "x": -0.2143,
                            "y": 0.2041
                        },
                        {
                            "x": -0.1939,
                            "y": 0.2124
                        },
                        {
                            "x": -0.1735,
                            "y": 0.2199
                        },
                        {
                            "x": -0.1531,
                            "y": 0.2266
                        },
                        {
                            "x": -0.1327,
                            "y": 0.2324
                        },
                        {
                            "x": -0.1122,
                            "y": 0.2374
                        },
                        {
                            "x": -0.0918,
                            "y": 0.2416
                        },
                        {
                            "x": -0.0714,
                            "y": 0.2449
                        },
                        {
                            "x": -0.051,
                            "y": 0.2474
                        },
                        {
                            "x": -0.0306,
                            "y": 0.2491
                        },
                        {
                            "x": -0.0102,
                            "y": 0.2499
                        },
                        {
                            "x": 0.0102,
                            "y": 0.2499
                        },
                        {
                            "x": 0.0306,
                            "y": 0.2491
                        },
                        {
                            "x": 0.051,
                            "y": 0.2474
                        },
                        {
                            "x": 0.0714,
                            "y": 0.2449
                        },
                        {
                            "x": 0.0918,
                            "y": 0.2416
                        },
                        {
                            "x": 0.1122,
                            "y": 0.2374
                        },
                        {
                            "x": 0.1327,
                            "y": 0.2324
                        },
                        {
                            "x": 0.1531,
                            "y": 0.2266
                        },
                        {
                            "x": 0.1735,
                            "y": 0.2199
                        },
                        {
                            "x": 0.1939,
                            "y": 0.2124
                        },
                        {
                            "x": 0.2143,
                            "y": 0.2041
                        },
                        {
                            "x": 0.2347,
                            "y": 0.1949
                        },
                        {
                            "x": 0.2551,
                            "y": 0.1849
                        },
                        {
                            "x": 0.2755,
                            "y": 0.1741
                        },
                        {
                            "x": 0.2959,
                            "y": 0.1624
                        },
                        {
                            "x": 0.3163,
                            "y": 0.1499
                        },
                        {
                            "x": 0.3367,
                            "y": 0.1366
                        },
                        {
                            "x": 0.3571,
                            "y": 0.1224
                        },
                        {
                            "x": 0.3776,
                            "y": 0.1075
                        },
                        {
                            "x": 0.398,
                            "y": 0.0916
                        },
                        {
                            "x": 0.4184,
                            "y": 0.075
                        },
                        {
                            "x": 0.4388,
                            "y": 0.0575
                        },
                        {
                            "x": 0.4592,
                            "y": 0.0392
                        },
                        {
                            "x": 0.4796,
                            "y": 0.02
                        },
                        {
                            "x": 0.5,
                            "y": 0
                        },
                        {
                            "x": 0.5,
                            "y": 0
                        },
                        {
                            "x": 0.4796,
                            "y": -0.02
                        },
                        {
                            "x": 0.4592,
                            "y": -0.0392
                        },
                        {
                            "x": 0.4388,
                            "y": -0.0575
                        },
                        {
                            "x": 0.4184,
                            "y": -0.075
                        },
                        {
                            "x": 0.398,
                            "y": -0.0916
                        },
                        {
                            "x": 0.3776,
                            "y": -0.1075
                        },
                        {
                            "x": 0.3571,
                            "y": -0.1224
                        },
                        {
                            "x": 0.3367,
                            "y": -0.1366
                        },
                        {
                            "x": 0.3163,
                            "y": -0.1499
                        },
                        {
                            "x": 0.2959,
                            "y": -0.1624
                        },
                        {
                            "x": 0.2755,
                            "y": -0.1741
                        },
                        {
                            "x": 0.2551,
                            "y": -0.1849
                        },
                        {
                            "x": 0.2347,
                            "y": -0.1949
                        },
                        {
                            "x": 0.2143,
                            "y": -0.2041
                        },
                        {
                            "x": 0.1939,
                            "y": -0.2124
                        },
                        {
                            "x": 0.1735,
                            "y": -0.2199
                        },
                        {
                            "x": 0.1531,
                            "y": -0.2266
                        },
                        {
                            "x": 0.1327,
                            "y": -0.2324
                        },
                        {
                            "x": 0.1122,
                            "y": -0.2374
                        },
                        {
                            "x": 0.0918,
                            "y": -0.2416
                        },
                        {
                            "x": 0.0714,
                            "y": -0.2449
                        },
                        {
                            "x": 0.051,
                            "y": -0.2474
                        },
                        {
                            "x": 0.0306,
                            "y": -0.2491
                        },
                        {
                            "x": 0.0102,
                            "y": -0.2499
                        },
                        {
                            "x": -0.0102,
                            "y": -0.2499
                        },
                        {
                            "x": -0.0306,
                            "y": -0.2491
                        },
                        {
                            "x": -0.051,
                            "y": -0.2474
                        },
                        {
                            "x": -0.0714,
                            "y": -0.2449
                        },
                        {
                            "x": -0.0918,
                            "y": -0.2416
                        },
                        {
                            "x": -0.1122,
                            "y": -0.2374
                        },
                        {
                            "x": -0.1327,
                            "y": -0.2324
                        },
                        {
                            "x": -0.1531,
                            "y": -0.2266
                        },
                        {
                            "x": -0.1735,
                            "y": -0.2199
                        },
                        {
                            "x": -0.1939,
                            "y": -0.2124
                        },
                        {
                            "x": -0.2143,
                            "y": -0.2041
                        },
                        {
                            "x": -0.2347,
                            "y": -0.1949
                        },
                        {
                            "x": -0.2551,
                            "y": -0.1849
                        },
                        {
                            "x": -0.2755,
                            "y": -0.1741
                        },
                        {
                            "x": -0.2959,
                            "y": -0.1624
                        },
                        {
                            "x": -0.3163,
                            "y": -0.1499
                        },
                        {
                            "x": -0.3367,
                            "y": -0.1366
                        },
                        {
                            "x": -0.3571,
                            "y": -0.1224
                        },
                        {
                            "x": -0.3776,
                            "y": -0.1075
                        },
                        {
                            "x": -0.398,
                            "y": -0.0916
                        },
                        {
                            "x": -0.4184,
                            "y": -0.075
                        },
                        {
                            "x": -0.4388,
                            "y": -0.0575
                        },
                        {
                            "x": -0.4592,
                            "y": -0.0392
                        },
                        {
                            "x": -0.4796,
                            "y": -0.02
                        },
                        {
                            "x": -0.5,
                            "y": 0
                        }
                    ],
                    "hasDownConnection": False,
                    "hasRightConnection": False
                },
                {
                    "id": 11,
                    "points": [
                        {
                            "x": 0,
                            "y": -0.5
                        },
                        {
                            "x": -0.02,
                            "y": -0.4796
                        },
                        {
                            "x": -0.0392,
                            "y": -0.4592
                        },
                        {
                            "x": -0.0575,
                            "y": -0.4388
                        },
                        {
                            "x": -0.075,
                            "y": -0.4184
                        },
                        {
                            "x": -0.0916,
                            "y": -0.398
                        },
                        {
                            "x": -0.1075,
                            "y": -0.3776
                        },
                        {
                            "x": -0.1224,
                            "y": -0.3571
                        },
                        {
                            "x": -0.1366,
                            "y": -0.3367
                        },
                        {
                            "x": -0.1499,
                            "y": -0.3163
                        },
                        {
                            "x": -0.1624,
                            "y": -0.2959
                        },
                        {
                            "x": -0.1741,
                            "y": -0.2755
                        },
                        {
                            "x": -0.1849,
                            "y": -0.2551
                        },
                        {
                            "x": -0.1949,
                            "y": -0.2347
                        },
                        {
                            "x": -0.2041,
                            "y": -0.2143
                        },
                        {
                            "x": -0.2124,
                            "y": -0.1939
                        },
                        {
                            "x": -0.2199,
                            "y": -0.1735
                        },
                        {
                            "x": -0.2266,
                            "y": -0.1531
                        },
                        {
                            "x": -0.2324,
                            "y": -0.1327
                        },
                        {
                            "x": -0.2374,
                            "y": -0.1122
                        },
                        {
                            "x": -0.2416,
                            "y": -0.0918
                        },
                        {
                            "x": -0.2449,
                            "y": -0.0714
                        },
                        {
                            "x": -0.2474,
                            "y": -0.051
                        },
                        {
                            "x": -0.2491,
                            "y": -0.0306
                        },
                        {
                            "x": -0.2499,
                            "y": -0.0102
                        },
                        {
                            "x": -0.2499,
                            "y": 0.0102
                        },
                        {
                            "x": -0.2491,
                            "y": 0.0306
                        },
                        {
                            "x": -0.2474,
                            "y": 0.051
                        },
                        {
                            "x": -0.2449,
                            "y": 0.0714
                        },
                        {
                            "x": -0.2416,
                            "y": 0.0918
                        },
                        {
                            "x": -0.2374,
                            "y": 0.1122
                        },
                        {
                            "x": -0.2324,
                            "y": 0.1327
                        },
                        {
                            "x": -0.2266,
                            "y": 0.1531
                        },
                        {
                            "x": -0.2199,
                            "y": 0.1735
                        },
                        {
                            "x": -0.2124,
                            "y": 0.1939
                        },
                        {
                            "x": -0.2041,
                            "y": 0.2143
                        },
                        {
                            "x": -0.1949,
                            "y": 0.2347
                        },
                        {
                            "x": -0.1849,
                            "y": 0.2551
                        },
                        {
                            "x": -0.1741,
                            "y": 0.2755
                        },
                        {
                            "x": -0.1624,
                            "y": 0.2959
                        },
                        {
                            "x": -0.1499,
                            "y": 0.3163
                        },
                        {
                            "x": -0.1366,
                            "y": 0.3367
                        },
                        {
                            "x": -0.1224,
                            "y": 0.3571
                        },
                        {
                            "x": -0.1075,
                            "y": 0.3776
                        },
                        {
                            "x": -0.0916,
                            "y": 0.398
                        },
                        {
                            "x": -0.075,
                            "y": 0.4184
                        },
                        {
                            "x": -0.0575,
                            "y": 0.4388
                        },
                        {
                            "x": -0.0392,
                            "y": 0.4592
                        },
                        {
                            "x": -0.02,
                            "y": 0.4796
                        },
                        {
                            "x": 0,
                            "y": 0.5
                        },
                        {
                            "x": 0,
                            "y": 0.5
                        },
                        {
                            "x": 0.02,
                            "y": 0.4796
                        },
                        {
                            "x": 0.0392,
                            "y": 0.4592
                        },
                        {
                            "x": 0.0575,
                            "y": 0.4388
                        },
                        {
                            "x": 0.075,
                            "y": 0.4184
                        },
                        {
                            "x": 0.0916,
                            "y": 0.398
                        },
                        {
                            "x": 0.1075,
                            "y": 0.3776
                        },
                        {
                            "x": 0.1224,
                            "y": 0.3571
                        },
                        {
                            "x": 0.1366,
                            "y": 0.3367
                        },
                        {
                            "x": 0.1499,
                            "y": 0.3163
                        },
                        {
                            "x": 0.1624,
                            "y": 0.2959
                        },
                        {
                            "x": 0.1741,
                            "y": 0.2755
                        },
                        {
                            "x": 0.1849,
                            "y": 0.2551
                        },
                        {
                            "x": 0.1949,
                            "y": 0.2347
                        },
                        {
                            "x": 0.2041,
                            "y": 0.2143
                        },
                        {
                            "x": 0.2124,
                            "y": 0.1939
                        },
                        {
                            "x": 0.2199,
                            "y": 0.1735
                        },
                        {
                            "x": 0.2266,
                            "y": 0.1531
                        },
                        {
                            "x": 0.2324,
                            "y": 0.1327
                        },
                        {
                            "x": 0.2374,
                            "y": 0.1122
                        },
                        {
                            "x": 0.2416,
                            "y": 0.0918
                        },
                        {
                            "x": 0.2449,
                            "y": 0.0714
                        },
                        {
                            "x": 0.2474,
                            "y": 0.051
                        },
                        {
                            "x": 0.2491,
                            "y": 0.0306
                        },
                        {
                            "x": 0.2499,
                            "y": 0.0102
                        },
                        {
                            "x": 0.2499,
                            "y": -0.0102
                        },
                        {
                            "x": 0.2491,
                            "y": -0.0306
                        },
                        {
                            "x": 0.2474,
                            "y": -0.051
                        },
                        {
                            "x": 0.2449,
                            "y": -0.0714
                        },
                        {
                            "x": 0.2416,
                            "y": -0.0918
                        },
                        {
                            "x": 0.2374,
                            "y": -0.1122
                        },
                        {
                            "x": 0.2324,
                            "y": -0.1327
                        },
                        {
                            "x": 0.2266,
                            "y": -0.1531
                        },
                        {
                            "x": 0.2199,
                            "y": -0.1735
                        },
                        {
                            "x": 0.2124,
                            "y": -0.1939
                        },
                        {
                            "x": 0.2041,
                            "y": -0.2143
                        },
                        {
                            "x": 0.1949,
                            "y": -0.2347
                        },
                        {
                            "x": 0.1849,
                            "y": -0.2551
                        },
                        {
                            "x": 0.1741,
                            "y": -0.2755
                        },
                        {
                            "x": 0.1624,
                            "y": -0.2959
                        },
                        {
                            "x": 0.1499,
                            "y": -0.3163
                        },
                        {
                            "x": 0.1366,
                            "y": -0.3367
                        },
                        {
                            "x": 0.1224,
                            "y": -0.3571
                        },
                        {
                            "x": 0.1075,
                            "y": -0.3776
                        },
                        {
                            "x": 0.0916,
                            "y": -0.398
                        },
                        {
                            "x": 0.075,
                            "y": -0.4184
                        },
                        {
                            "x": 0.0575,
                            "y": -0.4388
                        },
                        {
                            "x": 0.0392,
                            "y": -0.4592
                        },
                        {
                            "x": 0.02,
                            "y": -0.4796
                        },
                        {
                            "x": 0,
                            "y": -0.5
                        }
                    ],
                    "hasDownConnection": False,
                    "hasRightConnection": False
                },
                {
                    "id": 12,
                    "points": [
                        {
                            "x": -0.5,
                            "y": 0
                        },
                        {
                            "x": -0.4796,
                            "y": 0.02
                        },
                        {
                            "x": -0.4592,
                            "y": 0.0392
                        },
                        {
                            "x": -0.4388,
                            "y": 0.0575
                        },
                        {
                            "x": -0.4184,
                            "y": 0.075
                        },
                        {
                            "x": -0.398,
                            "y": 0.0916
                        },
                        {
                            "x": -0.3776,
                            "y": 0.1075
                        },
                        {
                            "x": -0.3571,
                            "y": 0.1224
                        },
                        {
                            "x": -0.3367,
                            "y": 0.1366
                        },
                        {
                            "x": -0.3163,
                            "y": 0.1499
                        },
                        {
                            "x": -0.2959,
                            "y": 0.1624
                        },
                        {
                            "x": -0.2755,
                            "y": 0.1741
                        },
                        {
                            "x": -0.2551,
                            "y": 0.1849
                        },
                        {
                            "x": -0.2347,
                            "y": 0.1949
                        },
                        {
                            "x": -0.2143,
                            "y": 0.2041
                        },
                        {
                            "x": -0.1939,
                            "y": 0.2124
                        },
                        {
                            "x": -0.1735,
                            "y": 0.2199
                        },
                        {
                            "x": -0.1531,
                            "y": 0.2266
                        },
                        {
                            "x": -0.1327,
                            "y": 0.2324
                        },
                        {
                            "x": -0.1122,
                            "y": 0.2374
                        },
                        {
                            "x": -0.0918,
                            "y": 0.2416
                        },
                        {
                            "x": -0.0714,
                            "y": 0.2449
                        },
                        {
                            "x": -0.051,
                            "y": 0.2474
                        },
                        {
                            "x": -0.0306,
                            "y": 0.2491
                        },
                        {
                            "x": -0.0102,
                            "y": 0.2499
                        },
                        {
                            "x": 0.0102,
                            "y": 0.2499
                        },
                        {
                            "x": 0.0306,
                            "y": 0.2491
                        },
                        {
                            "x": 0.051,
                            "y": 0.2474
                        },
                        {
                            "x": 0.0714,
                            "y": 0.2449
                        },
                        {
                            "x": 0.0918,
                            "y": 0.2416
                        },
                        {
                            "x": 0.1122,
                            "y": 0.2374
                        },
                        {
                            "x": 0.1327,
                            "y": 0.2324
                        },
                        {
                            "x": 0.1531,
                            "y": 0.2266
                        },
                        {
                            "x": 0.1735,
                            "y": 0.2199
                        },
                        {
                            "x": 0.1939,
                            "y": 0.2124
                        },
                        {
                            "x": 0.2143,
                            "y": 0.2041
                        },
                        {
                            "x": 0.2347,
                            "y": 0.1949
                        },
                        {
                            "x": 0.2551,
                            "y": 0.1849
                        },
                        {
                            "x": 0.2755,
                            "y": 0.1741
                        },
                        {
                            "x": 0.2959,
                            "y": 0.1624
                        },
                        {
                            "x": 0.3163,
                            "y": 0.1499
                        },
                        {
                            "x": 0.3367,
                            "y": 0.1366
                        },
                        {
                            "x": 0.3571,
                            "y": 0.1224
                        },
                        {
                            "x": 0.3776,
                            "y": 0.1075
                        },
                        {
                            "x": 0.398,
                            "y": 0.0916
                        },
                        {
                            "x": 0.4184,
                            "y": 0.075
                        },
                        {
                            "x": 0.4388,
                            "y": 0.0575
                        },
                        {
                            "x": 0.4592,
                            "y": 0.0392
                        },
                        {
                            "x": 0.4796,
                            "y": 0.02
                        },
                        {
                            "x": 0.5,
                            "y": 0
                        },
                        {
                            "x": 0,
                            "y": -0.5
                        },
                        {
                            "x": -0.5,
                            "y": 0
                        }
                    ],
                    "hasDownConnection": False,
                    "hasRightConnection": False
                },
                {
                    "id": 13,
                    "points": [
                        {
                            "x": 0,
                            "y": -0.5
                        },
                        {
                            "x": -0.02,
                            "y": -0.4796
                        },
                        {
                            "x": -0.0392,
                            "y": -0.4592
                        },
                        {
                            "x": -0.0575,
                            "y": -0.4388
                        },
                        {
                            "x": -0.075,
                            "y": -0.4184
                        },
                        {
                            "x": -0.0916,
                            "y": -0.398
                        },
                        {
                            "x": -0.1075,
                            "y": -0.3776
                        },
                        {
                            "x": -0.1224,
                            "y": -0.3571
                        },
                        {
                            "x": -0.1366,
                            "y": -0.3367
                        },
                        {
                            "x": -0.1499,
                            "y": -0.3163
                        },
                        {
                            "x": -0.1624,
                            "y": -0.2959
                        },
                        {
                            "x": -0.1741,
                            "y": -0.2755
                        },
                        {
                            "x": -0.1849,
                            "y": -0.2551
                        },
                        {
                            "x": -0.1949,
                            "y": -0.2347
                        },
                        {
                            "x": -0.2041,
                            "y": -0.2143
                        },
                        {
                            "x": -0.2124,
                            "y": -0.1939
                        },
                        {
                            "x": -0.2199,
                            "y": -0.1735
                        },
                        {
                            "x": -0.2266,
                            "y": -0.1531
                        },
                        {
                            "x": -0.2324,
                            "y": -0.1327
                        },
                        {
                            "x": -0.2374,
                            "y": -0.1122
                        },
                        {
                            "x": -0.2416,
                            "y": -0.0918
                        },
                        {
                            "x": -0.2449,
                            "y": -0.0714
                        },
                        {
                            "x": -0.2474,
                            "y": -0.051
                        },
                        {
                            "x": -0.2491,
                            "y": -0.0306
                        },
                        {
                            "x": -0.2499,
                            "y": -0.0102
                        },
                        {
                            "x": -0.2499,
                            "y": 0.0102
                        },
                        {
                            "x": -0.2491,
                            "y": 0.0306
                        },
                        {
                            "x": -0.2474,
                            "y": 0.051
                        },
                        {
                            "x": -0.2449,
                            "y": 0.0714
                        },
                        {
                            "x": -0.2416,
                            "y": 0.0918
                        },
                        {
                            "x": -0.2374,
                            "y": 0.1122
                        },
                        {
                            "x": -0.2324,
                            "y": 0.1327
                        },
                        {
                            "x": -0.2266,
                            "y": 0.1531
                        },
                        {
                            "x": -0.2199,
                            "y": 0.1735
                        },
                        {
                            "x": -0.2124,
                            "y": 0.1939
                        },
                        {
                            "x": -0.2041,
                            "y": 0.2143
                        },
                        {
                            "x": -0.1949,
                            "y": 0.2347
                        },
                        {
                            "x": -0.1849,
                            "y": 0.2551
                        },
                        {
                            "x": -0.1741,
                            "y": 0.2755
                        },
                        {
                            "x": -0.1624,
                            "y": 0.2959
                        },
                        {
                            "x": -0.1499,
                            "y": 0.3163
                        },
                        {
                            "x": -0.1366,
                            "y": 0.3367
                        },
                        {
                            "x": -0.1224,
                            "y": 0.3571
                        },
                        {
                            "x": -0.1075,
                            "y": 0.3776
                        },
                        {
                            "x": -0.0916,
                            "y": 0.398
                        },
                        {
                            "x": -0.075,
                            "y": 0.4184
                        },
                        {
                            "x": -0.0575,
                            "y": 0.4388
                        },
                        {
                            "x": -0.0392,
                            "y": 0.4592
                        },
                        {
                            "x": -0.02,
                            "y": 0.4796
                        },
                        {
                            "x": 0,
                            "y": 0.5
                        },
                        {
                            "x": 0.5,
                            "y": 0
                        },
                        {
                            "x": 0,
                            "y": -0.5
                        }
                    ],
                    "hasDownConnection": False,
                    "hasRightConnection": False
                },
                {
                    "id": 14,
                    "points": [
                        {
                            "x": 0.5,
                            "y": 0
                        },
                        {
                            "x": 0.4796,
                            "y": -0.02
                        },
                        {
                            "x": 0.4592,
                            "y": -0.0392
                        },
                        {
                            "x": 0.4388,
                            "y": -0.0575
                        },
                        {
                            "x": 0.4184,
                            "y": -0.075
                        },
                        {
                            "x": 0.398,
                            "y": -0.0916
                        },
                        {
                            "x": 0.3776,
                            "y": -0.1075
                        },
                        {
                            "x": 0.3571,
                            "y": -0.1224
                        },
                        {
                            "x": 0.3367,
                            "y": -0.1366
                        },
                        {
                            "x": 0.3163,
                            "y": -0.1499
                        },
                        {
                            "x": 0.2959,
                            "y": -0.1624
                        },
                        {
                            "x": 0.2755,
                            "y": -0.1741
                        },
                        {
                            "x": 0.2551,
                            "y": -0.1849
                        },
                        {
                            "x": 0.2347,
                            "y": -0.1949
                        },
                        {
                            "x": 0.2143,
                            "y": -0.2041
                        },
                        {
                            "x": 0.1939,
                            "y": -0.2124
                        },
                        {
                            "x": 0.1735,
                            "y": -0.2199
                        },
                        {
                            "x": 0.1531,
                            "y": -0.2266
                        },
                        {
                            "x": 0.1327,
                            "y": -0.2324
                        },
                        {
                            "x": 0.1122,
                            "y": -0.2374
                        },
                        {
                            "x": 0.0918,
                            "y": -0.2416
                        },
                        {
                            "x": 0.0714,
                            "y": -0.2449
                        },
                        {
                            "x": 0.051,
                            "y": -0.2474
                        },
                        {
                            "x": 0.0306,
                            "y": -0.2491
                        },
                        {
                            "x": 0.0102,
                            "y": -0.2499
                        },
                        {
                            "x": -0.0102,
                            "y": -0.2499
                        },
                        {
                            "x": -0.0306,
                            "y": -0.2491
                        },
                        {
                            "x": -0.051,
                            "y": -0.2474
                        },
                        {
                            "x": -0.0714,
                            "y": -0.2449
                        },
                        {
                            "x": -0.0918,
                            "y": -0.2416
                        },
                        {
                            "x": -0.1122,
                            "y": -0.2374
                        },
                        {
                            "x": -0.1327,
                            "y": -0.2324
                        },
                        {
                            "x": -0.1531,
                            "y": -0.2266
                        },
                        {
                            "x": -0.1735,
                            "y": -0.2199
                        },
                        {
                            "x": -0.1939,
                            "y": -0.2124
                        },
                        {
                            "x": -0.2143,
                            "y": -0.2041
                        },
                        {
                            "x": -0.2347,
                            "y": -0.1949
                        },
                        {
                            "x": -0.2551,
                            "y": -0.1849
                        },
                        {
                            "x": -0.2755,
                            "y": -0.1741
                        },
                        {
                            "x": -0.2959,
                            "y": -0.1624
                        },
                        {
                            "x": -0.3163,
                            "y": -0.1499
                        },
                        {
                            "x": -0.3367,
                            "y": -0.1366
                        },
                        {
                            "x": -0.3571,
                            "y": -0.1224
                        },
                        {
                            "x": -0.3776,
                            "y": -0.1075
                        },
                        {
                            "x": -0.398,
                            "y": -0.0916
                        },
                        {
                            "x": -0.4184,
                            "y": -0.075
                        },
                        {
                            "x": -0.4388,
                            "y": -0.0575
                        },
                        {
                            "x": -0.4592,
                            "y": -0.0392
                        },
                        {
                            "x": -0.4796,
                            "y": -0.02
                        },
                        {
                            "x": -0.5,
                            "y": 0
                        },
                        {
                            "x": 0,
                            "y": 0.5
                        },
                        {
                            "x": 0.5,
                            "y": 0
                        }
                    ],
                    "hasDownConnection": False,
                    "hasRightConnection": True
                },
                {
                    "id": 15,
                    "points": [
                        {
                            "x": 0,
                            "y": 0.5
                        },
                        {
                            "x": 0.02,
                            "y": 0.4796
                        },
                        {
                            "x": 0.0392,
                            "y": 0.4592
                        },
                        {
                            "x": 0.0575,
                            "y": 0.4388
                        },
                        {
                            "x": 0.075,
                            "y": 0.4184
                        },
                        {
                            "x": 0.0916,
                            "y": 0.398
                        },
                        {
                            "x": 0.1075,
                            "y": 0.3776
                        },
                        {
                            "x": 0.1224,
                            "y": 0.3571
                        },
                        {
                            "x": 0.1366,
                            "y": 0.3367
                        },
                        {
                            "x": 0.1499,
                            "y": 0.3163
                        },
                        {
                            "x": 0.1624,
                            "y": 0.2959
                        },
                        {
                            "x": 0.1741,
                            "y": 0.2755
                        },
                        {
                            "x": 0.1849,
                            "y": 0.2551
                        },
                        {
                            "x": 0.1949,
                            "y": 0.2347
                        },
                        {
                            "x": 0.2041,
                            "y": 0.2143
                        },
                        {
                            "x": 0.2124,
                            "y": 0.1939
                        },
                        {
                            "x": 0.2199,
                            "y": 0.1735
                        },
                        {
                            "x": 0.2266,
                            "y": 0.1531
                        },
                        {
                            "x": 0.2324,
                            "y": 0.1327
                        },
                        {
                            "x": 0.2374,
                            "y": 0.1122
                        },
                        {
                            "x": 0.2416,
                            "y": 0.0918
                        },
                        {
                            "x": 0.2449,
                            "y": 0.0714
                        },
                        {
                            "x": 0.2474,
                            "y": 0.051
                        },
                        {
                            "x": 0.2491,
                            "y": 0.0306
                        },
                        {
                            "x": 0.2499,
                            "y": 0.0102
                        },
                        {
                            "x": 0.2499,
                            "y": -0.0102
                        },
                        {
                            "x": 0.2491,
                            "y": -0.0306
                        },
                        {
                            "x": 0.2474,
                            "y": -0.051
                        },
                        {
                            "x": 0.2449,
                            "y": -0.0714
                        },
                        {
                            "x": 0.2416,
                            "y": -0.0918
                        },
                        {
                            "x": 0.2374,
                            "y": -0.1122
                        },
                        {
                            "x": 0.2324,
                            "y": -0.1327
                        },
                        {
                            "x": 0.2266,
                            "y": -0.1531
                        },
                        {
                            "x": 0.2199,
                            "y": -0.1735
                        },
                        {
                            "x": 0.2124,
                            "y": -0.1939
                        },
                        {
                            "x": 0.2041,
                            "y": -0.2143
                        },
                        {
                            "x": 0.1949,
                            "y": -0.2347
                        },
                        {
                            "x": 0.1849,
                            "y": -0.2551
                        },
                        {
                            "x": 0.1741,
                            "y": -0.2755
                        },
                        {
                            "x": 0.1624,
                            "y": -0.2959
                        },
                        {
                            "x": 0.1499,
                            "y": -0.3163
                        },
                        {
                            "x": 0.1366,
                            "y": -0.3367
                        },
                        {
                            "x": 0.1224,
                            "y": -0.3571
                        },
                        {
                            "x": 0.1075,
                            "y": -0.3776
                        },
                        {
                            "x": 0.0916,
                            "y": -0.398
                        },
                        {
                            "x": 0.075,
                            "y": -0.4184
                        },
                        {
                            "x": 0.0575,
                            "y": -0.4388
                        },
                        {
                            "x": 0.0392,
                            "y": -0.4592
                        },
                        {
                            "x": 0.02,
                            "y": -0.4796
                        },
                        {
                            "x": 0,
                            "y": -0.5
                        },
                        {
                            "x": -0.5,
                            "y": 0
                        },
                        {
                            "x": 0,
                            "y": 0.5
                        }
                    ],
                    "hasDownConnection": True,
                    "hasRightConnection": False
                },
                {
                    "id": 16,
                    "points": [
                        {
                            "x": 0,
                            "y": -0.5
                        },
                        {
                            "x": 0.5,
                            "y": 0
                        },
                        {
                            "x": 0,
                            "y": 0.5
                        },
                        {
                            "x": -0.5,
                            "y": 0
                        },
                        {
                            "x": 0,
                            "y": -0.5
                        }
                    ],
                    "hasDownConnection": False,
                    "hasRightConnection": False
                }
            ]
        }

        with open('kolamPatternsData.json', 'w') as f:
            json.dump(pattern_data, f, indent=2)

        print("✅ Created kolamPatternsData.json file")
        print("⚠️  Note: Only pattern 1 is included. Please add all 16 patterns from your data.")

class ColorPalettes:
    """Predefined color palettes for kolam rendering."""

    CLASSIC = {'dots': 'white', 'lines': 'white', 'bg': 'black'}
    GOLDEN = {'dots': '#FFD700', 'lines': '#FFA500', 'bg': '#8B0000'}
    OCEAN = {'dots': '#00CED1', 'lines': '#1E90FF', 'bg': '#191970'}
    FOREST = {'dots': '#90EE90', 'lines': '#32CD32', 'bg': '#006400'}
    SUNSET = {'dots': '#FF6347', 'lines': '#FF4500', 'bg': '#8B0000'}
    ROYAL = {'dots': '#DDA0DD', 'lines': '#9370DB', 'bg': '#4B0082'}
    EMERALD = {'dots': '#50C878', 'lines': '#00FF7F', 'bg': '#013220'}
    COPPER = {'dots': '#B87333', 'lines': '#CD7F32', 'bg': '#2F1B14'}
    LAVENDER = {'dots': '#E6E6FA', 'lines': '#DDA0DD', 'bg': '#301934'}
    FIRE = {'dots': '#FF4500', 'lines': '#DC143C', 'bg': '#000000'}

    @classmethod
    def get_all_palettes(cls) -> Dict[str, Dict[str, str]]:
        """Get all available color palettes."""
        return {
            'classic': cls.CLASSIC,
            'golden': cls.GOLDEN,
            'ocean': cls.OCEAN,
            'forest': cls.FOREST,
            'sunset': cls.SUNSET,
            'royal': cls.ROYAL,
            'emerald': cls.EMERALD,
            'copper': cls.COPPER,
            'lavender': cls.LAVENDER,
            'fire': cls.FIRE,
        }

    @classmethod
    def get_palette(cls, name: str) -> Dict[str, str]:
        """Get a specific color palette by name."""
        palettes = cls.get_all_palettes()
        return palettes.get(name.lower(), cls.CLASSIC)
