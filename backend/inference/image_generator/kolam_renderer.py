#!/usr/bin/env python3
"""
Streamlined Kolam Renderer
"""

import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
import numpy as np
from typing import Dict, List, Tuple

class KolamRenderer:

    def __init__(self):
        plt.ioff()  # Turn off interactive mode

    def _interpolate_curve(self, points: List[Dict], num_points: int = 50) -> Tuple[List[float], List[float]]:
        if len(points) < 2:
            return [], []

        x_coords = [p['x'] for p in points]
        y_coords = [p['y'] for p in points]

        if len(points) == 2:
            t = np.linspace(0, 1, num_points)
            x_interp = x_coords[0] + t * (x_coords[1] - x_coords[0])
            y_interp = y_coords[0] + t * (y_coords[1] - y_coords[0])
        else:
            t_original = np.linspace(0, 1, len(points))
            t_new = np.linspace(0, 1, num_points)
            x_interp = np.interp(t_new, t_original, x_coords)
            y_interp = np.interp(t_new, t_original, y_coords)

        return x_interp.tolist(), y_interp.tolist()

    def render_to_png(self, pattern: Dict, filename: str, color_scheme: Dict[str, str],
                     width: int = 800, height: int = 800, dpi: int = 150) -> None:

        fig_width = width / dpi
        fig_height = height / dpi
        fig, ax = plt.subplots(1, 1, figsize=(fig_width, fig_height), dpi=dpi)

        fig.patch.set_facecolor(color_scheme['bg'])
        ax.set_facecolor(color_scheme['bg'])

        pattern_width = pattern['dimensions']['width']
        pattern_height = pattern['dimensions']['height']

        padding = 20
        ax.set_xlim(0 - padding, pattern_width + padding)
        ax.set_ylim(0 - padding, pattern_height + padding)
        ax.set_aspect('equal')

        ax.set_xticks([])
        ax.set_yticks([])
        for spine in ax.spines.values():
            spine.set_visible(False)

        # Draw curves
        for curve in pattern['curves']:
            points = curve['points']
            if len(points) < 2:
                continue

            if len(points) > 2:
                x_smooth, y_smooth = self._interpolate_curve(points, num_points=100)
                ax.plot(x_smooth, y_smooth, color=color_scheme['lines'],
                       linewidth=2.0, linestyle='-', solid_capstyle='round',
                       solid_joinstyle='round', alpha=0.9)
            else:
                x_coords = [p['x'] for p in points]
                y_coords = [p['y'] for p in points]
                ax.plot(x_coords, y_coords, color=color_scheme['lines'],
                       linewidth=2.0, linestyle='-', solid_capstyle='round',
                       solid_joinstyle='round', alpha=0.9)

        # Draw dots
        for dot in pattern['dots']:
            center = dot['center']
            radius = dot.get('radius', 3.0)
            circle = plt.Circle((center['x'], center['y']), radius,
                              color=color_scheme['dots'], alpha=1.0, zorder=10)
            ax.add_patch(circle)

        plt.tight_layout()
        plt.savefig(filename, dpi=dpi, bbox_inches='tight', pad_inches=0.1,
                   facecolor=color_scheme['bg'], edgecolor='none', format='png')
        plt.close(fig)

class ColorPalettes:
    THEMES = {
        'classic': {'dots': 'white', 'lines': 'white', 'bg': 'black'},
        'golden': {'dots': '#FFD700', 'lines': '#FFA500', 'bg': '#8B0000'},
        'ocean': {'dots': '#00CED1', 'lines': '#1E90FF', 'bg': '#191970'},
        'forest': {'dots': '#90EE90', 'lines': '#32CD32', 'bg': '#006400'},
        'sunset': {'dots': '#FF6347', 'lines': '#FF4500', 'bg': '#8B0000'},
        'royal': {'dots': '#DDA0DD', 'lines': '#9370DB', 'bg': '#4B0082'},
        'emerald': {'dots': '#50C878', 'lines': '#00FF7F', 'bg': '#013220'},
        'copper': {'dots': '#B87333', 'lines': '#CD7F32', 'bg': '#2F1B14'},
        'lavender': {'dots': '#E6E6FA', 'lines': '#DDA0DD', 'bg': '#301934'},
        'fire': {'dots': '#FF4500', 'lines': '#DC143C', 'bg': '#000000'}
    }

    @classmethod
    def get_theme(cls, name: str) -> Dict[str, str]:
        return cls.THEMES.get(name.lower(), cls.THEMES['classic'])
