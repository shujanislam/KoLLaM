#!/usr/bin/env python3
"""
Streamlined Kolam Pattern Generator
"""

import numpy as np
import json
import random
from dataclasses import dataclass
from typing import List, Dict, Optional

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
    CELL_SPACING = 60

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

    def __init__(self, json_file_path: str):
        with open(json_file_path, 'r') as f:
            data = json.load(f)
        self.patterns = self._load_patterns(data['patterns'])
        self.h_self = self._find_self_inverse(self.H_INV)
        self.v_self = self._find_self_inverse(self.V_INV)

    def _load_patterns(self, patterns_data: List[Dict]) -> List[KolamPattern]:
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
        result = []
        for i, val in enumerate(inv):
            if val == i + 1:
                result.append(i + 1)
        return result

    def _intersect(self, arr1: List[int], arr2: List[int]) -> List[int]:
        return list(set(arr1) & set(arr2))

    def _random_choice(self, arr: List[int]) -> int:
        if not arr:
            return 1
        return random.choice(arr)

    def _ones(self, size: int) -> List[List[int]]:
        return [[1 for _ in range(size)] for _ in range(size)]

    def propose_kolam_1d(self, size_of_kolam: int) -> List[List[int]]:
        odd = (size_of_kolam % 2) != 0
        hp = (size_of_kolam - 1) // 2 if odd else size_of_kolam // 2
        Mat = self._ones(hp + 2)

        # Main grid generation
        for i in range(1, hp + 1):
            for j in range(1, hp + 1):
                pt_dn_value = self.PT_DN[Mat[i - 1][j] - 1]
                valid_by_up = self.MATE_PT_DN[pt_dn_value + 1]

                pt_rt_value = self.PT_RT[Mat[i][j - 1] - 1]
                valid_by_lt = self.MATE_PT_RT[pt_rt_value + 1]

                valids = self._intersect(valid_by_up, valid_by_lt)
                Mat[i][j] = self._random_choice(valids)

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
            Mat[hp + 1][j] = self._random_choice(valids)

        # Right column
        for i in range(1, hp + 1):
            pt_dn_value = self.PT_DN[Mat[i - 1][hp + 1] - 1]
            valid_by_up = self.MATE_PT_DN[pt_dn_value + 1]

            pt_rt_value = self.PT_RT[Mat[i][hp] - 1]
            valid_by_lt = self.MATE_PT_RT[pt_rt_value + 1]

            valids = self._intersect(valid_by_up, valid_by_lt)
            valids = self._intersect(valids, self.h_self)
            Mat[i][hp + 1] = self._random_choice(valids)

        # Corner element
        pt_dn_value = self.PT_DN[Mat[hp][hp + 1] - 1]
        valid_by_up = self.MATE_PT_DN[pt_dn_value + 1]

        pt_rt_value = self.PT_RT[Mat[hp + 1][hp] - 1]
        valid_by_lt = self.MATE_PT_RT[pt_rt_value + 1]

        valids = self._intersect(valid_by_up, valid_by_lt)
        valids = self._intersect(valids, self.h_self)
        valids = self._intersect(valids, self.v_self)
        Mat[hp + 1][hp + 1] = self._random_choice(valids)

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

            for i in range(hp):
                for j in range(hp):
                    M[i][j] = Mat1[i][j]
                    M[i][hp + 1 + j] = Mat2[i][j]
                    M[hp + 1 + i][j] = Mat3[i][j]
                    M[hp + 1 + i][hp + 1 + j] = Mat4[i][j]

            for i in range(hp):
                M[i][hp] = Mat[i + 1][hp + 1]
                M[hp + 1 + i][hp] = self.V_INV[Mat[hp - i][hp + 1] - 1]

            for j in range(hp):
                M[hp][j] = Mat[hp + 1][j + 1]
                M[hp][hp + 1 + j] = self.H_INV[Mat[hp + 1][hp - j] - 1]

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
        matrix = self.propose_kolam_1d(size)
        m, n = len(matrix), len(matrix[0])
        flipped_matrix = [matrix[m - 1 - i] for i in range(m)]

        dots = []
        curves = []

        for i in range(m):
            for j in range(n):
                if flipped_matrix[i][j] > 0:
                    dot_center = {
                        'x': (j + 1) * self.CELL_SPACING,
                        'y': (i + 1) * self.CELL_SPACING
                    }
                    dots.append({
                        'id': f'dot-{i}-{j}',
                        'center': dot_center,
                        'radius': 3
                    })

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

        return {
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

    def generate_invalid_kolam(self, size: int, invalid_type: str = "broken_loops") -> Dict:
        """Generate intentionally invalid kolams for dataset"""
        pattern = self.generate_kolam(size)

        if invalid_type == "broken_loops":
            # Remove random curves to break loops
            num_to_remove = max(1, len(pattern['curves']) // 4)
            indices_to_remove = random.sample(range(len(pattern['curves'])), num_to_remove)
            pattern['curves'] = [curve for i, curve in enumerate(pattern['curves'])
                               if i not in indices_to_remove]

        elif invalid_type == "asymmetry":
            # Break symmetry by directly manipulating dots and curves after generation
            # This bypasses the symmetric generation algorithm

            # Method 1: Remove dots/curves from one side only
            if random.choice([True, False]):
                # Remove elements from right half
                center_x = pattern['dimensions']['width'] / 2
                pattern['dots'] = [dot for dot in pattern['dots']
                                 if not (dot['center']['x'] > center_x and random.random() < 0.3)]
                pattern['curves'] = [curve for curve in pattern['curves']
                                   if not (len(curve['points']) > 0 and
                                          curve['points'][0]['x'] > center_x and
                                          random.random() < 0.3)]
            else:
                # Remove elements from bottom half
                center_y = pattern['dimensions']['height'] / 2
                pattern['dots'] = [dot for dot in pattern['dots']
                                 if not (dot['center']['y'] > center_y and random.random() < 0.3)]
                pattern['curves'] = [curve for curve in pattern['curves']
                                   if not (len(curve['points']) > 0 and
                                          curve['points'][0]['y'] > center_y and
                                          random.random() < 0.3)]

            # Method 2: Add extra random elements on one side
            if random.choice([True, False]):
                # Add extra dots on one side
                for _ in range(random.randint(1, 3)):
                    side_bias = random.choice(['left', 'right', 'top', 'bottom'])
                    if side_bias == 'right':
                        x = random.uniform(pattern['dimensions']['width'] * 0.7, pattern['dimensions']['width'] * 0.9)
                        y = random.uniform(pattern['dimensions']['height'] * 0.2, pattern['dimensions']['height'] * 0.8)
                    elif side_bias == 'left':
                        x = random.uniform(pattern['dimensions']['width'] * 0.1, pattern['dimensions']['width'] * 0.3)
                        y = random.uniform(pattern['dimensions']['height'] * 0.2, pattern['dimensions']['height'] * 0.8)
                    elif side_bias == 'top':
                        x = random.uniform(pattern['dimensions']['width'] * 0.2, pattern['dimensions']['width'] * 0.8)
                        y = random.uniform(pattern['dimensions']['height'] * 0.1, pattern['dimensions']['height'] * 0.3)
                    else:  # bottom
                        x = random.uniform(pattern['dimensions']['width'] * 0.2, pattern['dimensions']['width'] * 0.8)
                        y = random.uniform(pattern['dimensions']['height'] * 0.7, pattern['dimensions']['height'] * 0.9)

                    pattern['dots'].append({
                        'id': f'asymmetric-dot-{len(pattern["dots"])}',
                        'center': {'x': x, 'y': y},
                        'radius': random.uniform(2, 5)
                    })

        elif invalid_type == "displaced_dots":
            # Randomly displace some dots
            for dot in random.sample(pattern['dots'], max(1, len(pattern['dots']) // 3)):
                dot['center']['x'] += random.uniform(-20, 20)
                dot['center']['y'] += random.uniform(-20, 20)

        pattern['id'] = f"invalid-{invalid_type}-{pattern['id']}"
        pattern['name'] = f"Invalid {invalid_type.replace('_', ' ').title()} - {pattern['name']}"
        return pattern
