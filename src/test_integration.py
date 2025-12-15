"""
Script test integrasi untuk memverifikasi sistem deteksi pothole secara keseluruhan.
Menggunakan:
1. Model: runs/segment/yolov8m-seg-custom/weights/best.pt
2. Kalibrasi: calibration_results/camera_params.yaml
3. Test Data: datasets/potholes_video/pothole_video.mp4
"""

import cv2
import numpy as np
from pathlib import Path
import sys
import os

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.pothole_detection_system import PotholeDetectionSystem

def main():
    print("=" * 60)
    print("🚀 MULAI INTEGRATION TEST")
    print("=" * 60)
    
    # 1. Setup Paths
    # Gunakan absolute path agar aman dijalankan dari mana saja
    base_dir = Path(os.getcwd())
    
    # Path Model (Segmentation)
    model_path = base_dir / "runs/segment/yolov8m-seg-custom/weights/best.pt"
    
    # Path Kalibrasi
    calib_path = base_dir / "calibration_results/camera_params.yaml"
    
    # Path Output
    output_dir = base_dir / "output/sem_test_results"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Verify Paths
    if not model_path.exists():
        print(f"❌ Model tidak ditemukan: {model_path}")
        return
    
    if not calib_path.exists():
        print(f"❌ File kalibrasi tidak ditemukan: {calib_path}")
        return
        
    print(f"✅ Model Path: {model_path}")
    print(f"✅ Calibration Path: {calib_path}")
    
    # 2. Initialize System
    print("\n🔄 Menginisialisasi Sistem...")
    try:
        system = PotholeDetectionSystem(
            yolo_model_path=model_path,
            depth_model_type="small",      # Gunakan small agar cepat
            camera_calib_path=calib_path,
            camera_height=1.5,             # Asumsi tinggi kamera 1.5 meter
            conf_threshold=0.25,
            enable_tracking=True
        )
    except Exception as e:
        print(f"❌ Gagal inisialisasi sistem: {e}")
        return
        
    # 3. Test Video Processing
    print("\n🎬 Running Video Test...")
    video_path = base_dir / "datasets/potholes_video/pothole_video.mp4"
    output_video = output_dir / "detected_video.avi"
    
    if video_path.exists():
        system.process_video(
            video_path=video_path,
            output_path=output_video,
            show_preview=False,    # False agar automation lancar
            frame_skip=1,
            save_measurements=True
        )
        print(f"✅ Video test selesai. Output: {output_video}")
    else:
        print(f"⚠️ Video test dilewati (file tidak ada): {video_path}")
        
    # 4. Test Single Image Processing (Salah satu contoh dari test dataset)
    print("\n📸 Running Single Image Test...")
    test_images_dir = base_dir / "datasets/potholes_raw/test/images"
    # Ambil gambar pertama yang ditemukan
    image_files = list(test_images_dir.glob("*.jpg"))
    
    if image_files:
        test_img_path = image_files[0]
        img = cv2.imread(str(test_img_path))
        
        if img is not None:
            results = system.process_frame(img)
            
            # Visualize
            vis_img = system.visualize_results(img, results)
            
            # Save
            output_img = output_dir / "detected_image.jpg"
            cv2.imwrite(str(output_img), vis_img)
            
            print(f"✅ Image test selesai: {test_img_path.name}")
            print(f"   Saved to: {output_img}")
            
            # Print measurements
            print(f"\n📊 Pengukuran pada gambar test:")
            for m in results['measurements']:
                print(f"   - Conf: {m.confidence:.2f}, Diameter: {m.diameter_cm:.1f}cm, Depth: {m.depth_cm:.1f}cm")
        else:
            print("❌ Gagal load image test")
    else:
        print("⚠️ Image test dilewati (tidak ada jpg di folder test)")
        
    print("\n" + "=" * 60)
    print("✅ SEMUA TEST SELESAI")
    print("=" * 60)

if __name__ == "__main__":
    main()
