"""
Contoh Penggunaan PotholeDetectionSystem
Demonstrasi pipeline lengkap: YOLO Detection + Depth Estimation + Measurement
"""

import cv2
import numpy as np
from pathlib import Path
from pothole_detection_system import PotholeDetectionSystem
import matplotlib.pyplot as plt


def example_single_image():
    """Contoh penggunaan untuk single image"""
    print("=" * 60)
    print("CONTOH 1: Processing Single Image")
    print("=" * 60)
    
    # Initialize system dengan tracking enabled
    system = PotholeDetectionSystem(
        yolo_model_path="runs/detect/yolov8n-potholes-ft/weights/best.pt",
        depth_model_type="small",
        camera_calib_path="camera_params.json",  # Sesuaikan path
        camera_height=1.5,
        conf_threshold=0.25,
        enable_tracking=True,  # Enable BoT-SORT tracking
        tracker_max_age=30,    # Keep lost tracks for 30 frames
        tracker_min_hits=3     # Confirm track after 3 hits
    )
    
    # Load image
    image_path = "datasets/potholes_raw/test/images/your_image.jpg"  # Sesuaikan path
    if not Path(image_path).exists():
        print(f"⚠️  Image tidak ditemukan: {image_path}")
        print("   Silakan sesuaikan path dengan struktur project Anda")
        return
    
    image = cv2.imread(image_path)
    if image is None:
        print(f"❌ Gagal load image: {image_path}")
        return
    
    # Process frame
    results = system.process_frame(image)
    
    # Print results
    print(f"\n📊 Results:")
    print(f"   Detections: {len(results['measurements'])} potholes found")
    print(f"   Tracks: {len(results.get('tracks', []))} confirmed tracks")
    print(f"   Scale factor: {results['scale_factor']:.4f}")
    
    # Print tracked potholes
    if 'tracks' in results and len(results['tracks']) > 0:
        for track in results['tracks']:
            measurement = track.measurement
            print(f"\n   Track ID {track.track_id} (Age: {track.age}, Hits: {track.hit_streak}):")
            print(f"      Confidence: {measurement.confidence:.3f}")
            print(f"      Diameter: {measurement.diameter_cm:.2f} cm")
            print(f"      Depth: {measurement.depth_cm:.2f} cm")
            print(f"      Z_surface: {measurement.z_surface:.3f} m")
            print(f"      Z_base: {measurement.z_base:.3f} m")
    else:
        # Print untracked measurements
        for i, measurement in enumerate(results['measurements']):
            print(f"\n   Pothole {i+1}:")
            print(f"      Confidence: {measurement.confidence:.3f}")
            print(f"      Diameter: {measurement.diameter_cm:.2f} cm")
            print(f"      Depth: {measurement.depth_cm:.2f} cm")
    
    # Visualize dengan tracking
    vis_image = system.visualize_results(image, results, 
                                         show_depth=True, 
                                         show_measurements=True,
                                         show_tracks=True)  # Show track IDs
    
    # Save result
    output_path = "output/detected_image.jpg"
    Path(output_path).parent.mkdir(exist_ok=True)
    cv2.imwrite(output_path, vis_image)
    print(f"\n💾 Result saved to: {output_path}")
    
    # Display (optional)
    # plt.figure(figsize=(15, 10))
    # plt.imshow(cv2.cvtColor(vis_image, cv2.COLOR_BGR2RGB))
    # plt.title('Pothole Detection Results')
    # plt.axis('off')
    # plt.show()


def example_video():
    """Contoh penggunaan untuk video"""
    print("\n" + "=" * 60)
    print("CONTOH 2: Processing Video")
    print("=" * 60)
    
    # Initialize system dengan tracking
    system = PotholeDetectionSystem(
        yolo_model_path="runs/detect/yolov8n-potholes-ft/weights/best.pt",
        depth_model_type="small",
        camera_calib_path="camera_params.json",  # Sesuaikan path
        camera_height=1.5,
        conf_threshold=0.25,
        enable_tracking=True  # Enable tracking untuk video
    )
    
    # Process video
    video_path = "datasets/potholes_video/pothole_video.mp4"  # Sesuaikan path
    if not Path(video_path).exists():
        print(f"⚠️  Video tidak ditemukan: {video_path}")
        print("   Silakan sesuaikan path dengan struktur project Anda")
        return
    
    summary = system.process_video(
        video_path=video_path,
        output_path="output/detected_video.avi",
        show_preview=False,  # Set True untuk preview real-time
        frame_skip=1,  # Process setiap frame
        save_measurements=True
    )
    
    print(f"\n📊 Summary:")
    print(f"   Total frames: {summary['total_frames']}")
    print(f"   Processed frames: {summary['processed_frames']}")
    print(f"   Total detections: {summary['total_detections']}")
    print(f"   Output video: {summary['output_video']}")
    if summary['measurements_file']:
        print(f"   Measurements: {summary['measurements_file']}")
        print(f"   Note: Measurements include track_id untuk tracking lintas frame")


def example_step_by_step():
    """Contoh penggunaan step-by-step untuk kontrol lebih detail"""
    print("\n" + "=" * 60)
    print("CONTOH 3: Step-by-Step Processing")
    print("=" * 60)
    
    # Initialize system
    system = PotholeDetectionSystem(
        yolo_model_path="runs/detect/yolov8n-potholes-ft/weights/best.pt",
        depth_model_type="small",
        camera_calib_path="camera_params.json",
        camera_height=1.5
    )
    
    # Load image
    image_path = "datasets/potholes_raw/test/images/your_image.jpg"
    image = cv2.imread(image_path)
    if image is None:
        print(f"❌ Gagal load image: {image_path}")
        return
    
    # Step 1: Undistort
    image_undistorted = system.depth_estimator.undistort_image(image)
    
    # Step 2: YOLO Detection
    yolo_results = system.yolo_model(image_undistorted, conf=0.25)
    detections = yolo_results[0].boxes if len(yolo_results) > 0 else []
    print(f"   YOLO detections: {len(detections)} potholes")
    
    # Step 3: Depth Estimation
    depth_map_rel, _ = system.depth_estimator.estimate_depth(image_undistorted)
    depth_map_abs, scale_factor = system.depth_estimator.scale_recovery(depth_map_rel)
    print(f"   Depth map generated, scale factor: {scale_factor:.4f}")
    
    # Step 4: Calculate Measurements
    measurements = system._calculate_measurements(detections, depth_map_abs)
    print(f"   Measurements calculated: {len(measurements)} potholes")
    
    # Step 5: Tracking (jika enabled)
    tracks = []
    if system.enable_tracking:
        tracks = system.tracker.update(measurements)
        print(f"   Tracks: {len(tracks)} confirmed tracks")
    
    # Step 6: Visualize
    results = {
        'detections': yolo_results,
        'depth_map_absolute': depth_map_abs,
        'measurements': measurements,
        'tracks': tracks
    }
    vis_image = system.visualize_results(image, results, show_tracks=system.enable_tracking)
    
    # Save
    cv2.imwrite("output/step_by_step_result.jpg", vis_image)
    print(f"   Result saved to: output/step_by_step_result.jpg")


if __name__ == "__main__":
    print("\n🚀 Pothole Detection System - Contoh Penggunaan")
    print("=" * 60)
    print("\nPilih contoh yang ingin dijalankan:")
    print("1. Single Image Processing")
    print("2. Video Processing")
    print("3. Step-by-Step Processing")
    print("\n⚠️  Pastikan path model, kalibrasi, dan data sudah sesuai!")
    print("=" * 60)
    
    # Uncomment salah satu untuk test
    # example_single_image()
    # example_video()
    # example_step_by_step()
    
    print("\n💡 Uncomment salah satu fungsi di atas untuk menjalankan contoh")

