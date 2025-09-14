#!/usr/bin/env python3
"""
Kolam CLI - Command Line Interface
Advanced command-line interface for generating kolam patterns.
"""

import argparse
import sys
import json
from pathlib import Path
from typing import Optional, List

from kolam_generator import KolamGenerator
from kolam_renderer import KolamRenderer
from kolam_utils import KolamUtils, ColorPalettes

def setup_data_file():
    """Set up the kolamPatternsData.json file if it doesn't exist."""
    if not Path('kolamPatternsData.json').exists():
        print("⚠️  kolamPatternsData.json not found. Creating template...")
        KolamUtils.create_pattern_data_file()
        print("📝 Please replace the template with your complete pattern data.")
        return False
    return True

def load_patterns_data():
    """Load pattern data from JSON file."""
    try:
        with open('kolamPatternsData.json', 'r') as f:
            data = json.load(f)
            return data['patterns']
    except FileNotFoundError:
        print("❌ Error: kolamPatternsData.json not found!")
        print("Please save your pattern data to kolamPatternsData.json")
        sys.exit(1)
    except KeyError:
        print("❌ Error: Invalid pattern data format!")
        sys.exit(1)

def generate_single_kolam(args):
    """Generate a single kolam pattern."""
    patterns_data = load_patterns_data()
    generator = KolamGenerator(patterns_data)
    renderer = KolamRenderer()

    # Generate pattern
    pattern = generator.generate_kolam(args.size)

    # Print statistics if requested
    if args.verbose:
        KolamUtils.print_pattern_stats(pattern)

    # Apply transformations
    if args.scale != 1.0:
        pattern = KolamUtils.scale_pattern(pattern, args.scale)
        print(f"🔄 Scaled pattern by factor {args.scale}")

    if args.center:
        pattern = KolamUtils.center_pattern(pattern)
        print("🎯 Centered pattern")

    # Save pattern data if requested
    if args.save_json:
        json_filename = args.output.replace('.png', '.json')
        KolamUtils.save_pattern_to_json(pattern, json_filename)

    # Get colors
    if args.palette:
        colors = ColorPalettes.get_palette(args.palette)
        dot_color = colors['dots']
        line_color = colors['lines']
        background_color = colors['bg']
    else:
        dot_color = args.dot_color
        line_color = args.line_color
        background_color = args.background

    # Render to PNG
    renderer.render_to_png(
        pattern,
        args.output,
        dot_color=dot_color,
        line_color=line_color,
        background_color=background_color,
        width=args.width,
        height=args.height,
        dpi=args.dpi,
        line_width=args.line_width,
        dot_size=args.dot_size,
        smooth_curves=not args.no_smooth
    )

    print(f"🎉 Kolam saved as {args.output}")

def generate_color_variants(args):
    """Generate multiple color variants of a kolam."""
    patterns_data = load_patterns_data()
    generator = KolamGenerator(patterns_data)
    renderer = KolamRenderer()

    # Generate pattern
    pattern = generator.generate_kolam(args.size)

    if args.verbose:
        KolamUtils.print_pattern_stats(pattern)

    # Generate variants
    base_name = args.output.replace('.png', '')
    variant_files = renderer.create_color_variants(pattern, base_name)

    print(f"🎨 Generated {len(variant_files)} color variants:")
    for file in variant_files:
        print(f"   📁 {file}")

def generate_animation_frames(args):
    """Generate animation frames for a kolam."""
    patterns_data = load_patterns_data()
    generator = KolamGenerator(patterns_data)
    renderer = KolamRenderer()

    # Generate pattern
    pattern = generator.generate_kolam(args.size)

    # Get colors
    if args.palette:
        colors = ColorPalettes.get_palette(args.palette)
        dot_color = colors['dots']
        line_color = colors['lines']
        background_color = colors['bg']
    else:
        dot_color = args.dot_color
        line_color = args.line_color
        background_color = args.background

    # Generate frames
    base_name = args.output.replace('.png', '')
    frame_files = renderer.render_with_animation_frames(
        pattern,
        base_name,
        num_frames=args.frames,
        dot_color=dot_color,
        line_color=line_color,
        background_color=background_color,
        width=args.width,
        height=args.height,
        dpi=args.dpi
    )

    print(f"🎬 Generated {len(frame_files)} animation frames")
    print("💡 Use a tool like ImageMagick to create animated GIF:")
    print(f"   convert -delay {args.delay} {base_name}_frame_*.png {base_name}.gif")

def generate_batch(args):
    """Generate multiple kolams with different sizes."""
    patterns_data = load_patterns_data()
    generator = KolamGenerator(patterns_data)
    renderer = KolamRenderer()

    sizes = list(range(args.min_size, args.max_size + 1))

    # Get colors
    if args.palette:
        colors = ColorPalettes.get_palette(args.palette)
        dot_color = colors['dots']
        line_color = colors['lines']
        background_color = colors['bg']
    else:
        dot_color = args.dot_color
        line_color = args.line_color
        background_color = args.background

    print(f"🔄 Generating batch of {len(sizes)} kolams...")

    for i, size in enumerate(sizes, 1):
        pattern = generator.generate_kolam(size)

        output_file = f"{args.prefix}_size_{size:02d}.png"

        renderer.render_to_png(
            pattern,
            output_file,
            dot_color=dot_color,
            line_color=line_color,
            background_color=background_color,
            width=args.width,
            height=args.height,
            dpi=args.dpi
        )

        print(f"   [{i}/{len(sizes)}] Generated {output_file}")

    print(f"✅ Batch generation complete!")

def list_palettes(args):
    """List all available color palettes."""
    palettes = ColorPalettes.get_all_palettes()

    print("\n🎨 Available Color Palettes:")
    print("=" * 40)

    for name, colors in palettes.items():
        print(f"{name.upper():<12} | Dots: {colors['dots']:<10} | Lines: {colors['lines']:<10} | BG: {colors['bg']}")

    print("=" * 40)
    print("💡 Use with: --palette <name>")

def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Generate beautiful Kolam patterns as PNG images",
        epilog="Examples:\n"
               "  %(prog)s generate --size 7 --output my_kolam.png\n"
               "  %(prog)s variants --size 5 --output kolam_variants.png\n"
               "  %(prog)s animate --size 6 --frames 30 --output animation.png\n"
               "  %(prog)s batch --min-size 3 --max-size 10 --prefix batch_kolam",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # Common arguments
    common_args = argparse.ArgumentParser(add_help=False)
    common_args.add_argument('--size', type=int, default=7,
                           help='Size of kolam (3-15), default: 7')
    common_args.add_argument('--output', type=str, default='kolam.png',
                           help='Output filename, default: kolam.png')
    common_args.add_argument('--width', type=int, default=800,
                           help='Image width in pixels, default: 800')
    common_args.add_argument('--height', type=int, default=800,
                           help='Image height in pixels, default: 800')
    common_args.add_argument('--dpi', type=int, default=150,
                           help='Image DPI, default: 150')
    common_args.add_argument('--verbose', '-v', action='store_true',
                           help='Show detailed information')

    # Color arguments
    color_args = argparse.ArgumentParser(add_help=False)
    color_args.add_argument('--palette', type=str,
                          help='Use predefined color palette (run "list-palettes" to see options)')
    color_args.add_argument('--dot-color', type=str, default='white',
                          help='Color of dots, default: white')
    color_args.add_argument('--line-color', type=str, default='white',
                          help='Color of lines/curves, default: white')
    color_args.add_argument('--background', type=str, default='black',
                          help='Background color, default: black')

    # Rendering arguments
    render_args = argparse.ArgumentParser(add_help=False)
    render_args.add_argument('--line-width', type=float, default=2.0,
                           help='Width of curve lines, default: 2.0')
    render_args.add_argument('--dot-size', type=float, default=3.0,
                           help='Size of dots, default: 3.0')
    render_args.add_argument('--no-smooth', action='store_true',
                           help='Disable curve smoothing')

    # Generate single kolam
    generate_parser = subparsers.add_parser('generate', parents=[common_args, color_args, render_args],
                                          help='Generate a single kolam pattern')
    generate_parser.add_argument('--scale', type=float, default=1.0,
                               help='Scale factor for the pattern, default: 1.0')
    generate_parser.add_argument('--center', action='store_true',
                               help='Center the pattern')
    generate_parser.add_argument('--save-json', action='store_true',
                               help='Also save pattern data as JSON')

    # Generate color variants
    variants_parser = subparsers.add_parser('variants', parents=[common_args],
                                          help='Generate multiple color variants')

    # Generate animation frames
    animate_parser = subparsers.add_parser('animate', parents=[common_args, color_args],
                                         help='Generate animation frames')
    animate_parser.add_argument('--frames', type=int, default=20,
                              help='Number of animation frames, default: 20')
    animate_parser.add_argument('--delay', type=int, default=10,
                              help='Delay between frames (for ImageMagick), default: 10')

    # Generate batch
    batch_parser = subparsers.add_parser('batch', parents=[common_args, color_args],
                                       help='Generate multiple kolams with different sizes')
    batch_parser.add_argument('--min-size', type=int, default=3,
                            help='Minimum kolam size, default: 3')
    batch_parser.add_argument('--max-size', type=int, default=10,
                            help='Maximum kolam size, default: 10')
    batch_parser.add_argument('--prefix', type=str, default='kolam',
                            help='Filename prefix for batch files, default: kolam')

    # List palettes
    list_parser = subparsers.add_parser('list-palettes', help='List available color palettes')

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return

    # Validate size
    if hasattr(args, 'size'):
        if args.size < 3 or args.size > 15:
            print("❌ Error: Size must be between 3 and 15")
            sys.exit(1)

    # Validate colors if not using palette
    if hasattr(args, 'palette') and not args.palette:
        for color_name, color_value in [('dot-color', getattr(args, 'dot_color', None)),
                                       ('line-color', getattr(args, 'line_color', None)),
                                       ('background', getattr(args, 'background', None))]:
            if color_value and not KolamUtils.validate_color(color_value):
                print(f"❌ Error: Invalid color '{color_value}' for {color_name}")
                sys.exit(1)

    # Set up data file
    if args.command != 'list-palettes':
        if not setup_data_file():
            sys.exit(1)

    # Execute command
    try:
        if args.command == 'generate':
            generate_single_kolam(args)
        elif args.command == 'variants':
            generate_color_variants(args)
        elif args.command == 'animate':
            generate_animation_frames(args)
        elif args.command == 'batch':
            generate_batch(args)
        elif args.command == 'list-palettes':
            list_palettes(args)
    except KeyboardInterrupt:
        print("\n🛑 Operation cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
