"""
Camera Calibration Script untuk Pothole Detection System
Mengikuti metodologi BAB 3.4 dari proposal penelitian

Langkah-langkah:
1. Cetak checkerboard pattern (25mm x 25mm)
2. Ambil 15-20 foto dari berbagai sudut dan jarak
3. Jalankan script ini untuk kalibrasi
4. Simpan parameter intrinsik ke YAML/JSON
"""

import cv2
import numpy as np
import yaml
import json
import os
from pathlib import Path
import argparse
 

def create_checkerboard_pattern(pattern_size=(9, 6), square_size=25):
    """Buat checkerboard pattern untuk kalibrasi
    
    Args:
        pattern_size: Tuple (width, height) internal corners, default: (9, 6)
        square_size: Ukuran kotak dalam mm, default: 25
    
    Returns:
        objp: 3D object points
        pattern_size: Pattern size yang digunakan
    """
    # Buat objek points untuk kalibrasi
    objp = np.zeros((pattern_size[0] * pattern_size[1], 3), np.float32)
    objp[:, :2] = np.mgrid[0:pattern_size[0], 0:pattern_size[1]].T.reshape(-1, 2)
    objp *= square_size  # Convert to mm
    
    return objp, pattern_size


def calibrate_camera(images_folder, output_file="camera_params.yaml", 
                     pattern_size=(9, 6), square_size=25):
    """
    Kalibrasi kamera menggunakan gambar checkerboard
    
    Args:
        images_folder: Path ke folder berisi gambar kalibrasi
        output_file: File output untuk menyimpan parameter
        pattern_size: Tuple (width, height) internal corners, default: (9, 6)
        square_size: Ukuran kotak dalam mm, default: 25
    """
    
    # Setup output directory handling
    output_path = Path(output_file)
    if len(output_path.parts) == 1:
        # If just filename provided, use calibration_results folder
        output_dir = Path("calibration_results")
        output_file = output_dir / output_file
    else:
        # Use the parent directory of the provided output file
        output_dir = output_path.parent
        
    # Create directory if it doesn't exist
    output_dir.mkdir(parents=True, exist_ok=True)
    print(f"📂 Output akan disimpan di: {output_dir}")
    objp, pattern_size = create_checkerboard_pattern(pattern_size, square_size)
    objpoints = []  # 3D points in real world space
    imgpoints = []  # 2D points in image plane
    
    # Get list of calibration images
    image_files = []
    for ext in ['*.jpg', '*.jpeg', '*.png', '*.bmp']:
        image_files.extend(Path(images_folder).glob(ext))
    
    if not image_files:
        print(f"❌ Tidak ada gambar kalibrasi ditemukan di {images_folder}")
        print("Pastikan folder berisi gambar .jpg/.png/.bmp")
        return False
    
    print(f"📁 Ditemukan {len(image_files)} gambar kalibrasi")
    print(f"📐 Pattern size: {pattern_size[0]}×{pattern_size[1]} internal corners")
    print(f"📏 Square size: {square_size}mm")
    
    # Process each image
    successful_detections = 0
    
    for i, img_path in enumerate(image_files):
        print(f"🔄 Memproses {i+1}/{len(image_files)}: {img_path.name}")
        
        # Load image
        img = cv2.imread(str(img_path))
        if img is None:
            print(f"   ⚠️  Gagal load: {img_path}")
            continue
            
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        # Find chessboard corners
        ret, corners = cv2.findChessboardCorners(gray, pattern_size, None)
        
        if ret:
            # Refine corner positions
            criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
            corners2 = cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)
            
            objpoints.append(objp)
            imgpoints.append(corners2)
            successful_detections += 1
            
            # Draw and display corners
            img_with_corners = img.copy()
            cv2.drawChessboardCorners(img_with_corners, pattern_size, corners2, ret)
            
            # Save visualization
            output_viz = output_dir / f"calibration_viz_{img_path.stem}.jpg"
            cv2.imwrite(str(output_viz), img_with_corners)
            print(f"   ✅ Detected corners - saved: {output_viz}")
        else:
            print(f"   ❌ Tidak ditemukan corners")
    
    print(f"\n📊 Hasil deteksi: {successful_detections}/{len(image_files)} gambar berhasil")
    
    if successful_detections < 10:
        print("❌ Minimal 10 gambar diperlukan untuk kalibrasi yang baik")
        return False
    
    # Perform calibration
    print("\n🔧 Melakukan kalibrasi kamera...")
    img_shape = gray.shape[::-1]  # (width, height)
    
    ret, K, dist, rvecs, tvecs = cv2.calibrateCamera(
        objpoints, imgpoints, img_shape, None, None
    )
    
    if not ret:
        print("❌ Kalibrasi gagal")
        return False
    
    # Calculate reprojection error
    total_error = 0
    for i in range(len(objpoints)):
        imgpoints2, _ = cv2.projectPoints(objpoints[i], rvecs[i], tvecs[i], K, dist)
        error = cv2.norm(imgpoints[i], imgpoints2, cv2.NORM_L2) / len(imgpoints2)
        total_error += error
    
    mean_error = total_error / len(objpoints)
    
    print(f"✅ Kalibrasi berhasil!")
    print(f"📏 Reprojection error: {mean_error:.3f} pixels")
    print(f"📐 Image size: {img_shape}")
    print(f"🔍 Focal length: fx={K[0,0]:.1f}, fy={K[1,1]:.1f}")
    print(f"📍 Principal point: cx={K[0,2]:.1f}, cy={K[1,2]:.1f}")
    
    # Save parameters
    camera_params = {
        'camera_matrix': K.tolist(),
        'distortion_coefficients': dist.tolist(),
        'image_size': img_shape,
        'reprojection_error': float(mean_error),
        'successful_images': successful_detections,
        'total_images': len(image_files),
        'calibration_date': str(Path().cwd()),
        'checkerboard_size': pattern_size,
        'square_size_mm': square_size
    }
    
    # Save as YAML
    with open(output_file, 'w') as f:
        yaml.dump(camera_params, f, default_flow_style=False)
    
    # Save as JSON (backup)
    json_file = output_file.with_suffix('.json')
    with open(json_file, 'w') as f:
        json.dump(camera_params, f, indent=2)
    
    print(f"💾 Parameter tersimpan ke: {output_file} dan {json_file}")
    
    # Test undistortion
    test_undistortion(images_folder, K, dist, output_dir)
    
    return True


def test_undistortion(images_folder, K, dist, output_dir):
    """Test undistortion pada beberapa gambar"""
    print("\n🧪 Testing undistortion...")
    
    # Ensure output_dir is a Path object
    output_dir = Path(output_dir)
    
    # Load first image for test
    image_files = list(Path(images_folder).glob('*.jpg'))[:3]  # Test 3 images
    
    for img_path in image_files:
        img = cv2.imread(str(img_path))
        if img is None:
            continue
            
        # Undistort
        h, w = img.shape[:2]
        new_camera_matrix, roi = cv2.getOptimalNewCameraMatrix(K, dist, (w, h), 1, (w, h))
        undistorted = cv2.undistort(img, K, dist, None, new_camera_matrix)
        
        # Save comparison
        comparison = np.hstack([img, undistorted])
        output_name = output_dir / f"undistort_test_{img_path.stem}.jpg"
        cv2.imwrite(str(output_name), comparison)
        print(f"   📸 Saved: {output_name}")


def load_camera_params(param_file):
    """Load camera parameters dari file"""
    if param_file.endswith('.yaml'):
        with open(param_file, 'r') as f:
            params = yaml.safe_load(f)
    else:
        with open(param_file, 'r') as f:
            params = json.load(f)
    
    K = np.array(params['camera_matrix'])
    dist = np.array(params['distortion_coefficients'])
    
    return K, dist, params


def main():
    parser = argparse.ArgumentParser(
        description='Camera Calibration untuk Pothole Detection',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
    Contoh penggunaan:
    # Kalibrasi dengan pattern default (9×6, 25mm)
    python camera_calibration.py --images calibration_images/ --output params.yaml
    
    # Kalibrasi untuk kertas A4 (7×10 internal corners, 25mm)
    python camera_calibration.py --images calibration_images/ --output params.yaml --pattern-size 7 10 --square-size 25
    
    # Test parameter yang sudah ada
    python camera_calibration.py --images calibration_images/ --load params.yaml
        """
    )
    parser.add_argument('--images', required=True, help='Path ke folder gambar kalibrasi')
    parser.add_argument('--output', default='camera_params.yaml', help='File output parameter')
    parser.add_argument('--load', help='Load parameter yang sudah ada untuk testing')
    parser.add_argument('--pattern-size', type=int, nargs=2, default=[9, 6], 
                        metavar=('WIDTH', 'HEIGHT'),
                        help='Pattern size (width height) internal corners, default: 9 6')
    parser.add_argument('--square-size', type=float, default=25.0,
                        help='Ukuran kotak dalam mm, default: 25.0')
    
    args = parser.parse_args()
    
    if args.load:
        # Load existing parameters
        print(f"📂 Loading parameters dari: {args.load}")
        K, dist, params = load_camera_params(args.load)
        print(f"✅ Loaded: fx={K[0,0]:.1f}, fy={K[1,1]:.1f}")
        print(f"📏 Reprojection error: {params['reprojection_error']:.3f}")
        
        # Test undistortion
        output_dir = Path(args.load).parent if Path(args.load).parent.name else Path("calibration_results")
        output_dir.mkdir(parents=True, exist_ok=True)
        test_undistortion(args.images, K, dist, output_dir)
    else:
        # Perform calibration
        if not os.path.exists(args.images):
            print(f"❌ Folder tidak ditemukan: {args.images}")
            return
        
        pattern_size = tuple(args.pattern_size)
        calibrate_camera(args.images, args.output, pattern_size, args.square_size)


if __name__ == "__main__":
    main()
