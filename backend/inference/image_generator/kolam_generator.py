#!/usr/bin/env python3
"""
Kolam Pattern Generator
Generates valid kolam designs as PNG images based on traditional South Indian patterns.
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.path import Path
from typing import List, Dict, Tuple, Optional
import json
import random
from dataclasses import dataclass
from pathlib import Path as FilePath
import argparse

@dataclass
class Point:
    x: float
    y: float

@dataclass
class KolamPattern:
    id: int
    points: List[Point]
    has_down_connection: bool
    has_right_connection: bool

class KolamGenerator:
    """Main kolam generator class implementing the algorithm from your TypeScript code."""

    CELL_SPACING = 60

    # Core constants from your TypeScript code
    PT_DN = [0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 1, 1, 1, 0, 1, 1]
    PT_RT = [0, 0, 1, 0, 0, 1, 1, 0, 0, 1, 0, 1, 1, 1, 0, 1]

    MATE_PT_DN = {
        1: [2, 3, 5, 6, 9, 10, 12],
        2: [4, 7, 8, 11, 13, 14, 15, 16]
    }

    MATE_PT_RT = {
        1: [2, 3, 4, 6, 7, 11, 13],
        2: [5, 8, 9, 10, 12, 14, 15, 16]
    }

    H_INV = [1, 2, 5, 4, 3, 9, 8, 7, 6, 10, 11, 12, 15, 14, 13, 16]
    V_INV = [1, 4, 3, 2, 5, 7, 6, 9, 8, 10, 11, 14, 13, 12, 15, 16]

    def __init__(self, patterns_data: List[Dict]):
        """Initialize with pattern data from JSON."""
        self.patterns = self._load_patterns(patterns_data)
        self.h_self = self._find_self_inverse(self.H_INV)
        self.v_self = self._find_self_inverse(self.V_INV)

    def _load_patterns(self, patterns_data: List[Dict]) -> List[KolamPattern]:
        """Load pattern data into KolamPattern objects."""
        patterns = []
        for pattern_data in patterns_data:
            points = [Point(p['x'], p['y']) for p in pattern_data['points']]
            pattern = KolamPattern(
                id=pattern_data['id'],
                points=points,
                has_down_connection=pattern_data['hasDownConnection'],
                has_right_connection=pattern_data['hasRightConnection']
            )
            patterns.append(pattern)
        return patterns

    def _find_self_inverse(self, inv: List[int]) -> List[int]:
        """Find self-inverse elements."""
        result = []
        for i, val in enumerate(inv):
            if val == i + 1:  # 1-indexed
                result.append(i + 1)
        return result

    def _intersect(self, arr1: List[int], arr2: List[int]) -> List[int]:
        """Array intersection."""
        return list(set(arr1) & set(arr2))

    def _random_choice(self, arr: List[int]) -> int:
        """Random array element selector."""
        if not arr:
            return 1  # Default fallback
        return random.choice(arr)

    def _ones(self, size: int) -> List[List[int]]:
        """Create matrix filled with ones."""
        return [[1 for _ in range(size)] for _ in range(size)]

    def propose_kolam_1d(self, size_of_kolam: int) -> List[List[int]]:
        """
        Literal translation of propose_kolam1D.m from MATLAB.
        Generates the pattern matrix using the kolam algorithm.
        """
        odd = (size_of_kolam % 2) != 0

        if odd:
            hp = (size_of_kolam - 1) // 2
        else:
            hp = size_of_kolam // 2

        Mat = self._ones(hp + 2)

        # Main grid generation
        for i in range(1, hp + 1):
            for j in range(1, hp + 1):
                pt_dn_value = self.PT_DN[Mat[i - 1][j] - 1]
                valid_by_up = self.MATE_PT_DN[pt_dn_value + 1]

                pt_rt_value = self.PT_RT[Mat[i][j - 1] - 1]
                valid_by_lt = self.MATE_PT_RT[pt_rt_value + 1]

                valids = self._intersect(valid_by_up, valid_by_lt)

                try:
                    v = self._random_choice(valids)
                    Mat[i][j] = v
                except:
                    Mat[i][j] = 1

        # Border conditions
        Mat[hp + 1][0] = 1
        Mat[0][hp + 1] = 1

        # Bottom row
        for j in range(1, hp + 1):
            pt_dn_value = self.PT_DN[Mat[hp][j] - 1]
            valid_by_up = self.MATE_PT_DN[pt_dn_value + 1]

            pt_rt_value = self.PT_RT[Mat[hp + 1][j - 1] - 1]
            valid_by_lt = self.MATE_PT_RT[pt_rt_value + 1]

            valids = self._intersect(valid_by_up, valid_by_lt)
            valids = self._intersect(valids, self.v_self)

            try:
                v = self._random_choice(valids)
                Mat[hp + 1][j] = v
            except:
                Mat[hp + 1][j] = 1

        # Right column
        for i in range(1, hp + 1):
            pt_dn_value = self.PT_DN[Mat[i - 1][hp + 1] - 1]
            valid_by_up = self.MATE_PT_DN[pt_dn_value + 1]

            pt_rt_value = self.PT_RT[Mat[i][hp] - 1]
            valid_by_lt = self.MATE_PT_RT[pt_rt_value + 1]

            valids = self._intersect(valid_by_up, valid_by_lt)
            valids = self._intersect(valids, self.h_self)

            try:
                v = self._random_choice(valids)
                Mat[i][hp + 1] = v
            except:
                Mat[i][hp + 1] = 1

        # Corner element
        pt_dn_value = self.PT_DN[Mat[hp][hp + 1] - 1]
        valid_by_up = self.MATE_PT_DN[pt_dn_value + 1]

        pt_rt_value = self.PT_RT[Mat[hp + 1][hp] - 1]
        valid_by_lt = self.MATE_PT_RT[pt_rt_value + 1]

        valids = self._intersect(valid_by_up, valid_by_lt)
        valids = self._intersect(valids, self.h_self)
        valids = self._intersect(valids, self.v_self)

        try:
            v = self._random_choice(valids)
            Mat[hp + 1][hp + 1] = v
        except:
            Mat[hp + 1][hp + 1] = 1

        # Extract core matrix
        Mat1 = [[Mat[i][j] for j in range(1, hp + 1)] for i in range(1, hp + 1)]

        # Create symmetric sections
        Mat3 = [[self.V_INV[Mat1[hp - 1 - i][j] - 1] for j in range(hp)] for i in range(hp)]
        Mat2 = [[self.H_INV[Mat1[i][hp - 1 - j] - 1] for j in range(hp)] for i in range(hp)]
        Mat4 = [[self.V_INV[Mat2[hp - 1 - i][j] - 1] for j in range(hp)] for i in range(hp)]

        # Final assembly
        if odd:
            size = 2 * hp + 1
            M = [[1 for _ in range(size)] for _ in range(size)]

            # Copy sections
            for i in range(hp):
                for j in range(hp):
                    M[i][j] = Mat1[i][j]
                    M[i][hp + 1 + j] = Mat2[i][j]
                    M[hp + 1 + i][j] = Mat3[i][j]
                    M[hp + 1 + i][hp + 1 + j] = Mat4[i][j]

            # Middle column
            for i in range(hp):
                M[i][hp] = Mat[i + 1][hp + 1]
                M[hp + 1 + i][hp] = self.V_INV[Mat[hp - i][hp + 1] - 1]

            # Middle row
            for j in range(hp):
                M[hp][j] = Mat[hp + 1][j + 1]
                M[hp][hp + 1 + j] = self.H_INV[Mat[hp + 1][hp - j] - 1]

            # Center
            M[hp][hp] = Mat[hp + 1][hp + 1]
        else:
            size = 2 * hp
            M = [[1 for _ in range(size)] for _ in range(size)]

            for i in range(hp):
                for j in range(hp):
                    M[i][j] = Mat1[i][j]
                    M[i][hp + j] = Mat2[i][j]
                    M[hp + i][j] = Mat3[i][j]
                    M[hp + i][hp + j] = Mat4[i][j]

        return M

    def generate_kolam(self, size: int) -> Dict:
        """Generate a complete kolam pattern."""
        print(f"🎨 Generating 1D Kolam of size {size}")

        matrix = self.propose_kolam_1d(size)
        print(f"📊 Generated matrix: {len(matrix)}x{len(matrix[0])}")

        # Flip matrix vertically (as in draw_kolam)
        m = len(matrix)
        n = len(matrix[0])
        flipped_matrix = [matrix[m - 1 - i] for i in range(m)]

        dots = []
        curves = []

        # Generate dots and curves from matrix
        for i in range(m):
            for j in range(n):
                if flipped_matrix[i][j] > 0:
                    # Add dot
                    dot_center = {
                        'x': (j + 1) * self.CELL_SPACING,
                        'y': (i + 1) * self.CELL_SPACING
                    }
                    dots.append({
                        'id': f'dot-{i}-{j}',
                        'center': dot_center,
                        'radius': 3
                    })

                    # Add curve
                    pattern_index = flipped_matrix[i][j] - 1
                    if 0 <= pattern_index < len(self.patterns):
                        pattern = self.patterns[pattern_index]

                        curve_points = []
                        for point in pattern.points:
                            curve_points.append({
                                'x': ((j + 1) + point.x) * self.CELL_SPACING,
                                'y': ((i + 1) + point.y) * self.CELL_SPACING
                            })

                        if curve_points:
                            curves.append({
                                'id': f'curve-{i}-{j}',
                                'points': curve_points
                            })

        pattern = {
            'id': f'kolam-{m}x{n}',
            'name': f'Kolam {m}×{n}',
            'dots': dots,
            'curves': curves,
            'dimensions': {
                'width': (n + 1) * self.CELL_SPACING,
                'height': (m + 1) * self.CELL_SPACING
            },
            'matrix': flipped_matrix
        }

        print(f"✅ Created kolam with {len(dots)} dots and {len(curves)} curves")
        return pattern


def main():
    """Main function with command line interface."""
    parser = argparse.ArgumentParser(description='Generate Kolam patterns as PNG images')
    parser.add_argument('--size', type=int, default=7, help='Size of kolam (3-15)')
    parser.add_argument('--output', type=str, default='kolam.png', help='Output filename')
    parser.add_argument('--dot-color', type=str, default='white', help='Color of dots')
    parser.add_argument('--line-color', type=str, default='white', help='Color of lines/curves')
    parser.add_argument('--background', type=str, default='black', help='Background color')
    parser.add_argument('--width', type=int, default=800, help='Image width in pixels')
    parser.add_argument('--height', type=int, default=800, help='Image height in pixels')
    parser.add_argument('--dpi', type=int, default=150, help='Image DPI')

    args = parser.parse_args()

    # Load pattern data from JSON (you'll need to save the JSON data to a file)
    # For now, we'll use a placeholder - you should save your kolamPatternsData.json
    # and load it here
    try:
        with open('kolamPatternsData.json', 'r') as f:
            data = json.load(f)
            patterns_data = data['patterns']
    except FileNotFoundError:
        print("❌ Error: kolamPatternsData.json not found!")
        print("Please save your pattern data to kolamPatternsData.json")
        return

    # Create generator and generate pattern
    generator = KolamGenerator(patterns_data)
    pattern = generator.generate_kolam(args.size)

    # Render and save
    from kolam_renderer import KolamRenderer
    renderer = KolamRenderer()
    renderer.render_to_png(
        pattern,
        args.output,
        dot_color=args.dot_color,
        line_color=args.line_color,
        background_color=args.background,
        width=args.width,
        height=args.height,
        dpi=args.dpi
    )

    print(f"🎉 Kolam saved as {args.output}")

if __name__ == "__main__":
    main()
