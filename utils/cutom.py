"""
Generator Checkerboard Pattern untuk Kalibrasi Kamera
Mendukung berbagai ukuran pattern termasuk kertas A4
"""

import cv2
import numpy as np
import argparse
from pathlib import Path


def mm_to_pixels(mm, dpi=300):
    """
    Konversi mm ke pixels berdasarkan DPI printer
    
    Args:
        mm: Ukuran dalam millimeter
        dpi: Dots per inch (default: 300 untuk kualitas baik)
    
    Returns:
        Ukuran dalam pixels
    """
    inches = mm / 25.4  # Convert mm to inches
    pixels = int(inches * dpi)
    return pixels


def generate_checkerboard(square_size_mm=25, pattern_size=(9, 6), 
                          filename='checkerboard_25mm.png', dpi=300):
    """
    Generate checkerboard pattern untuk kalibrasi kamera
    
    Args:
        square_size_mm: Ukuran kotak dalam mm (default: 25mm)
        pattern_size: Tuple (width, height) internal corners (default: (9, 6))
        filename: Nama file output
        dpi: DPI untuk print (default: 300)
    
    Returns:
        Tuple (filename, total_size_mm) - nama file dan ukuran total dalam mm
    """
    # Pattern size adalah internal corners, jadi total squares = pattern_size + 1
    squares_x = pattern_size[0] + 1
    squares_y = pattern_size[1] + 1
    
    # Konversi ukuran kotak dari mm ke pixels
    square_size_px = mm_to_pixels(square_size_mm, dpi)
    
    # Ukuran total image dalam pixels
    img_size = (squares_x * square_size_px, squares_y * square_size_px)
    
    # Hitung ukuran total dalam mm
    total_width_mm = squares_x * square_size_mm
    total_height_mm = squares_y * square_size_mm
    
    # Buat checkerboard pattern
    board = np.zeros((img_size[1], img_size[0]), np.uint8)
    for y in range(squares_y):
        for x in range(squares_x):
            if (x + y) % 2 == 0:
                cv2.rectangle(board, 
                            (x * square_size_px, y * square_size_px),
                            ((x + 1) * square_size_px, (y + 1) * square_size_px), 
                            255, -1)
    
    # Simpan gambar
    cv2.imwrite(filename, board)
    
    # Print informasi
    print(f"✅ Checkerboard tersimpan: {filename}")
    print(f"📐 Pattern size: {pattern_size[0]}×{pattern_size[1]} internal corners ({squares_x}×{squares_y} total squares)")
    print(f"📏 Square size: {square_size_mm}mm × {square_size_mm}mm")
    print(f"📄 Total size: {total_width_mm}mm × {total_height_mm}mm")
    print(f"🖨️  Image size: {img_size[0]}×{img_size[1]} pixels ({dpi} DPI)")
    print(f"💡 Tips: Print dengan DPI {dpi} dan pastikan 'Scale to fit' atau 'Actual size' di printer settings")
    
    return filename, (total_width_mm, total_height_mm)


def main():
    parser = argparse.ArgumentParser(
        description='Generator Checkerboard Pattern untuk Kalibrasi Kamera',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Contoh penggunaan:
  # Generate pattern standar (9×6, 25mm)
  python cutom.py
  
  # Generate pattern untuk A4 (7×10, 25mm)
  python cutom.py --pattern-size 7 10 --output checkerboard_a4.png
  
  # Generate pattern kustom (8×11, 20mm)
  python cutom.py --pattern-size 8 11 --square-size 20 --output checkerboard_custom.png
  
  # Generate dengan DPI berbeda (untuk printer 600 DPI)
  python cutom.py --dpi 600
        """
    )
    parser.add_argument('--pattern-size', type=int, nargs=2, default=[9, 6],
                        metavar=('WIDTH', 'HEIGHT'),
                        help='Pattern size (width height) internal corners, default: 9 6')
    parser.add_argument('--square-size', type=float, default=25.0,
                        help='Ukuran kotak dalam mm, default: 25.0')
    parser.add_argument('--output', '-o', default=None,
                        help='Nama file output (default: checkerboard_{pattern_size}_{square_size}mm.png)')
    parser.add_argument('--dpi', type=int, default=300,
                        help='DPI untuk print, default: 300')
    parser.add_argument('--preset', choices=['standard', 'a4'],
                        help='Preset pattern: standard (9×6) atau a4 (7×10)')
    
    args = parser.parse_args()
    
    # Handle preset
    if args.preset == 'a4':
        pattern_size = (7, 10)
        if args.output is None:
            args.output = 'checkerboard_a4_25mm.png'
    elif args.preset == 'standard':
        pattern_size = (9, 6)
    else:
        pattern_size = tuple(args.pattern_size)
    
    # Generate filename jika tidak diberikan
    if args.output is None:
        args.output = f'checkerboard_{pattern_size[0]}x{pattern_size[1]}_{int(args.square_size)}mm.png'
    
    # Generate checkerboard
    generate_checkerboard(
        square_size_mm=args.square_size,
        pattern_size=pattern_size,
        filename=args.output,
        dpi=args.dpi
    )


if __name__ == "__main__":
    main()
