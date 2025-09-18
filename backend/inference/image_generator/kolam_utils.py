#!/usr/bin/env python3
"""
Streamlined Kolam Utilities
"""

import json
from typing import Dict, List, Tuple

class KolamUtils:

    @staticmethod
    def save_pattern_to_json(pattern: Dict, filename: str) -> None:
        with open(filename, 'w') as f:
            json.dump(pattern, f, indent=2)

    @staticmethod
    def load_pattern_from_json(filename: str) -> Dict:
        with open(filename, 'r') as f:
            return json.load(f)

    @staticmethod
    def get_pattern_stats(pattern: Dict) -> Dict:
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
    def scale_pattern(pattern: Dict, scale_factor: float) -> Dict:
        scaled_pattern = pattern.copy()

        if 'dimensions' in pattern:
            scaled_pattern['dimensions'] = {
                'width': pattern['dimensions']['width'] * scale_factor,
                'height': pattern['dimensions']['height'] * scale_factor
            }

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
    def get_pattern_bounds(pattern: Dict) -> Tuple[float, float, float, float]:
        all_x = []
        all_y = []

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
