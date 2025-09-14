#!/usr/bin/env python3
"""
Kolam Renderer
Handles rendering kolam patterns to PNG images with customizable colors.
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.path import Path
import numpy as np
from typing import Dict, List, Tuple, Optional
import matplotlib.colors as mcolors

class KolamRenderer:
    """Renders kolam patterns to PNG images."""

    def __init__(self):
        # Set up matplotlib for high-quality rendering
        plt.style.use('default')

    def _create_smooth_curve(self, points: List[Dict]) -> Path:
        """Create a smooth curve path from points using Bezier curves."""
        if len(points) < 2:
            return None

        # Convert points to numpy arrays for easier manipulation
        x_coords = [p['x'] for p in points]
        y_coords = [p['y'] for p in points]

        if len(points) == 2:
            # Simple line
            verts = [(x_coords[0], y_coords[0]), (x_coords[1], y_coords[1])]
            codes = [Path.MOVETO, Path.LINETO]
        else:
            # Create smooth curve using quadratic Bezier
            verts = []
            codes = []

            # Start point
            verts.append((x_coords[0], y_coords[0]))
            codes.append(Path.MOVETO)

            # Create smooth curves between consecutive points
            for i in range(1, len(points)):
                if i == len(points) - 1:
                    # Last point - just line to
                    verts.append((x_coords[i], y_coords[i]))
                    codes.append(Path.LINETO)
                else:
                    # Create quadratic Bezier curve
                    # Control point is midway between current and next
                    control_x = (x_coords[i] + x_coords[i-1]) / 2
                    control_y = (y_coords[i] + y_coords[i-1]) / 2

                    # Add control point and end point
                    verts.append((control_x, control_y))
                    verts.append((x_coords[i], y_coords[i]))
                    codes.append(Path.CURVE3)
                    codes.append(Path.CURVE3)

        return Path(verts, codes)

    def _interpolate_curve(self, points: List[Dict], num_points: int = 50) -> Tuple[List[float], List[float]]:
        """Interpolate points to create smooth curves."""
        if len(points) < 2:
            return [], []

        x_coords = [p['x'] for p in points]
        y_coords = [p['y'] for p in points]

        if len(points) == 2:
            # Linear interpolation for 2 points
            t = np.linspace(0, 1, num_points)
            x_interp = x_coords[0] + t * (x_coords[1] - x_coords[0])
            y_interp = y_coords[0] + t * (y_coords[1] - y_coords[0])
        else:
            # Spline interpolation for multiple points
            t_original = np.linspace(0, 1, len(points))
            t_new = np.linspace(0, 1, num_points)
            x_interp = np.interp(t_new, t_original, x_coords)
            y_interp = np.interp(t_new, t_original, y_coords)

        return x_interp.tolist(), y_interp.tolist()

    def render_to_png(self, pattern: Dict, filename: str,
                     dot_color: str = 'white',
                     line_color: str = 'white',
                     background_color: str = 'black',
                     width: int = 800,
                     height: int = 800,
                     dpi: int = 150,
                     line_width: float = 2.0,
                     dot_size: float = 3.0,
                     smooth_curves: bool = True) -> None:
        """
        Render kolam pattern to PNG file.

        Args:
            pattern: Kolam pattern dictionary
            filename: Output filename
            dot_color: Color for dots
            line_color: Color for curves/lines
            background_color: Background color
            width: Image width in pixels
            height: Image height in pixels
            dpi: Image DPI
            line_width: Width of curve lines
            dot_size: Size of dots
            smooth_curves: Whether to smooth the curves
        """
        # Create figure and axis
        fig_width = width / dpi
        fig_height = height / dpi
        fig, ax = plt.subplots(1, 1, figsize=(fig_width, fig_height), dpi=dpi)

        # Set background color
        fig.patch.set_facecolor(background_color)
        ax.set_facecolor(background_color)

        # Get pattern dimensions
        pattern_width = pattern['dimensions']['width']
        pattern_height = pattern['dimensions']['height']

        # Set axis limits with some padding
        padding = 20
        ax.set_xlim(0 - padding, pattern_width + padding)
        ax.set_ylim(0 - padding, pattern_height + padding)
        ax.set_aspect('equal')

        # Remove axes
        ax.set_xticks([])
        ax.set_yticks([])
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['bottom'].set_visible(False)
        ax.spines['left'].set_visible(False)

        # Draw curves first (so dots appear on top)
        for curve in pattern['curves']:
            points = curve['points']
            if len(points) < 2:
                continue

            if smooth_curves and len(points) > 2:
                # Create smooth interpolated curve
                x_smooth, y_smooth = self._interpolate_curve(points, num_points=100)
                ax.plot(x_smooth, y_smooth,
                       color=line_color,
                       linewidth=line_width,
                       linestyle='-',
                       solid_capstyle='round',
                       solid_joinstyle='round',
                       alpha=0.9)
            else:
                # Draw as connected line segments
                x_coords = [p['x'] for p in points]
                y_coords = [p['y'] for p in points]
                ax.plot(x_coords, y_coords,
                       color=line_color,
                       linewidth=line_width,
                       linestyle='-',
                       solid_capstyle='round',
                       solid_joinstyle='round',
                       alpha=0.9)

        # Draw dots
        for dot in pattern['dots']:
            center = dot['center']
            radius = dot.get('radius', dot_size)

            circle = plt.Circle((center['x'], center['y']),
                              radius,
                              color=dot_color,
                              alpha=1.0,
                              zorder=10)  # Ensure dots are on top
            ax.add_patch(circle)

        # Save the figure
        plt.tight_layout()
        plt.savefig(filename,
                   dpi=dpi,
                   bbox_inches='tight',
                   pad_inches=0.1,
                   facecolor=background_color,
                   edgecolor='none',
                   format='png')
        plt.close()

        print(f"✅ Rendered kolam to {filename} ({width}x{height}px @ {dpi}DPI)")

    def render_with_animation_frames(self, pattern: Dict,
                                   base_filename: str,
                                   num_frames: int = 20,
                                   dot_color: str = 'white',
                                   line_color: str = 'white',
                                   background_color: str = 'black',
                                   width: int = 800,
                                   height: int = 800,
                                   dpi: int = 150) -> List[str]:
        """
        Render multiple frames showing progressive drawing of the kolam.

        Returns:
            List of generated frame filenames
        """
        frame_files = []

        total_curves = len(pattern['curves'])
        total_dots = len(pattern['dots'])

        for frame in range(num_frames + 1):
            progress = frame / num_frames

            # Calculate how many elements to show
            curves_to_show = int(total_curves * progress)
            dots_to_show = int(total_dots * progress)

            # Create frame pattern
            frame_pattern = pattern.copy()
            frame_pattern['curves'] = pattern['curves'][:curves_to_show]
            frame_pattern['dots'] = pattern['dots'][:dots_to_show]

            # Generate filename
            frame_filename = f"{base_filename}_frame_{frame:03d}.png"

            # Render frame
            self.render_to_png(frame_pattern, frame_filename,
                             dot_color=dot_color,
                             line_color=line_color,
                             background_color=background_color,
                             width=width,
                             height=height,
                             dpi=dpi)

            frame_files.append(frame_filename)

        print(f"✅ Generated {len(frame_files)} animation frames")
        return frame_files

    def create_color_variants(self, pattern: Dict, base_filename: str) -> List[str]:
        """Create multiple color variants of the same kolam."""

        color_schemes = [
            {'name': 'classic', 'dots': 'white', 'lines': 'white', 'bg': 'black'},
            {'name': 'golden', 'dots': '#FFD700', 'lines': '#FFA500', 'bg': '#8B0000'},
            {'name': 'ocean', 'dots': '#00CED1', 'lines': '#1E90FF', 'bg': '#191970'},
            {'name': 'forest', 'dots': '#90EE90', 'lines': '#32CD32', 'bg': '#006400'},
            {'name': 'sunset', 'dots': '#FF6347', 'lines': '#FF4500', 'bg': '#8B0000'},
            {'name': 'royal', 'dots': '#DDA0DD', 'lines': '#9370DB', 'bg': '#4B0082'},
        ]

        generated_files = []

        for scheme in color_schemes:
            filename = f"{base_filename}_{scheme['name']}.png"
            self.render_to_png(pattern, filename,
                             dot_color=scheme['dots'],
                             line_color=scheme['lines'],
                             background_color=scheme['bg'])
            generated_files.append(filename)

        print(f"✅ Generated {len(generated_files)} color variants")
        return generated_files
