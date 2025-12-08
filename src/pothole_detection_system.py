"""
Pothole Detection System - Integrasi YOLO + Depth Estimation
Pipeline lengkap untuk deteksi dan pengukuran pothole

Author: Skripsi Project
Date: 2025
"""

import cv2
import numpy as np
from pathlib import Path
from typing import List, Dict, Tuple, Optional, Union
from ultralytics import YOLO
from .depth_estimation import DepthEstimator
from .pothole_tracker import PotholeTracker, Track
import warnings
warnings.filterwarnings('ignore')


class PotholeMeasurement:
    """Data class untuk menyimpan hasil pengukuran pothole"""
    def __init__(self, 
                 bbox: Tuple[int, int, int, int],
                 confidence: float,
                 diameter_cm: float,
                 depth_cm: float,
                 z_surface: float,
                 z_base: float,
                 z_avg: float,
                 mask: Optional[np.ndarray] = None):
        self.bbox = bbox  # (x1, y1, x2, y2)
        self.confidence = confidence
        self.diameter_cm = diameter_cm
        self.depth_cm = depth_cm
        self.z_surface = z_surface  # meter
        self.z_base = z_base  # meter
        self.z_avg = z_avg  # meter
        self.mask = mask  # segmentation mask (optional)
    
    def to_dict(self) -> dict:
        """Convert ke dictionary untuk serialization"""
        return {
            'bbox': self.bbox,
            'confidence': self.confidence,
            'diameter_cm': self.diameter_cm,
            'depth_cm': self.depth_cm,
            'z_surface_m': self.z_surface,
            'z_base_m': self.z_base,
            'z_avg_m': self.z_avg
        }


class PotholeDetectionSystem:
    """
    Sistem terintegrasi untuk deteksi dan pengukuran pothole
    Menggabungkan YOLOv8 detection + DepthAnything V2 depth estimation
    """
    
    def __init__(self,
                 yolo_model_path: Union[str, Path],
                 depth_model_type: str = "small",
                 camera_calib_path: Optional[Union[str, Path]] = None,
                 camera_height: float = 1.5,
                 conf_threshold: float = 0.25,
                 enable_tracking: bool = True,
                 tracker_max_age: int = 30,
                 tracker_min_hits: int = 3):
        """
        Initialize Pothole Detection System
        
        Args:
            yolo_model_path: Path ke model YOLO (.pt file)
            depth_model_type: Tipe model DepthAnything ('small', 'base', 'large')
            camera_calib_path: Path ke file kalibrasi JSON
            camera_height: Tinggi kamera dari jalan (meter)
            conf_threshold: Confidence threshold untuk YOLO detection
            enable_tracking: Enable BoT-SORT tracking
            tracker_max_age: Maximum frames to keep lost tracks
            tracker_min_hits: Minimum hits to confirm track
        """
        # Load YOLO model
        print("🔄 Loading YOLO model...")
        self.yolo_model = YOLO(str(yolo_model_path))
        self.conf_threshold = conf_threshold
        print(f"✅ YOLO model loaded: {yolo_model_path}")
        
        # Initialize Depth Estimator
        print("🔄 Initializing Depth Estimator...")
        self.depth_estimator = DepthEstimator(
            model_type=depth_model_type,
            calib_path=camera_calib_path,
            camera_height=camera_height
        )
        print("✅ Depth Estimator initialized")
        
        # Initialize Tracker
        self.enable_tracking = enable_tracking
        if enable_tracking:
            print("🔄 Initializing BoT-SORT Tracker...")
            self.tracker = PotholeTracker(
                max_age=tracker_max_age,
                min_hits=tracker_min_hits,
                enable_kalman=True,  # Enable Kalman filter untuk temporal filtering
                kalman_process_noise=0.1,
                kalman_measurement_noise=1.0
            )
            print("✅ Tracker initialized (with Kalman Filter)")
        else:
            self.tracker = None
        
        # Get camera matrix for measurements
        if self.depth_estimator.camera_matrix is not None:
            self.fx = self.depth_estimator.camera_matrix[0, 0]
            self.fy = self.depth_estimator.camera_matrix[1, 1]
            self.cx = self.depth_estimator.camera_matrix[0, 2]
            self.cy = self.depth_estimator.camera_matrix[1, 2]
        else:
            # Default focal length (akan di-override jika kalibrasi tersedia)
            self.fx = 1000.0
            self.fy = 1000.0
            self.cx = 320.0
            self.cy = 240.0
            print("⚠️  Camera calibration not available, using default focal length")
        
        print("✅ PotholeDetectionSystem initialized")
    
    def _extract_roi_depth(self,
                          depth_map: np.ndarray,
                          bbox: Tuple[int, int, int, int],
                          border_width: int = 10) -> Tuple[np.ndarray, np.ndarray]:
        """
        Ekstrak ROI depth dan border depth dari bounding box
        
        Args:
            depth_map: Depth map absolut (meter)
            bbox: Bounding box (x1, y1, x2, y2)
            border_width: Lebar border untuk estimasi Z_surface (pixels)
            
        Returns:
            Tuple (roi_depth, border_depth)
        """
        x1, y1, x2, y2 = bbox
        h, w = depth_map.shape
        
        # Clamp bbox ke image boundaries
        x1 = max(0, int(x1))
        y1 = max(0, int(y1))
        x2 = min(w, int(x2))
        y2 = min(h, int(y2))
        
        # Extract ROI depth
        roi_depth = depth_map[y1:y2, x1:x2]
        
        # Extract border region (area di sekitar bbox)
        border_x1 = max(0, x1 - border_width)
        border_y1 = max(0, y1 - border_width)
        border_x2 = min(w, x2 + border_width)
        border_y2 = min(h, y2 + border_width)
        
        border_region = depth_map[border_y1:border_y2, border_x1:border_x2]
        
        # Create border mask (area border tapi bukan ROI)
        border_mask = np.ones((border_y2 - border_y1, border_x2 - border_x1), dtype=bool)
        
        # Convert to local coordinates within border region
        local_y1 = max(0, y1 - border_y1)
        local_x1 = max(0, x1 - border_x1)
        local_y2 = min(border_y2 - border_y1, y2 - border_y1)
        local_x2 = min(border_x2 - border_x1, x2 - border_x1)
        
        # Only mask out ROI if valid
        if local_y2 > local_y1 and local_x2 > local_x1:
            border_mask[local_y1:local_y2, local_x1:local_x2] = False
        
        border_depth = border_region[border_mask]
        
        return roi_depth, border_depth
    
    def _calculate_z_surface(self, border_depth: np.ndarray) -> float:
        """
        Hitung Z_surface menggunakan median (robust terhadap outlier)
        
        Args:
            border_depth: Depth values dari border region
            
        Returns:
            Z_surface dalam meter
        """
        if len(border_depth) == 0:
            return np.nan
        
        # Filter out invalid depths
        valid_depths = border_depth[border_depth > 0]
        if len(valid_depths) == 0:
            return np.nan
        
        # Use median (robust statistic)
        z_surface = np.median(valid_depths)
        return float(z_surface)
    
    def _calculate_z_base(self, roi_depth: np.ndarray) -> float:
        """
        Hitung Z_base menggunakan percentile 10% dengan outlier removal (IQR)
        
        Args:
            roi_depth: Depth values dari ROI pothole
            
        Returns:
            Z_base dalam meter
        """
        if roi_depth.size == 0:
            return np.nan
        
        # Flatten dan filter valid depths
        roi_flat = roi_depth.flatten()
        valid_depths = roi_flat[roi_flat > 0]
        
        if len(valid_depths) == 0:
            return np.nan
        
        # Outlier removal dengan IQR method
        Q1 = np.percentile(valid_depths, 25)
        Q3 = np.percentile(valid_depths, 75)
        IQR = Q3 - Q1
        
        if IQR > 0:
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            filtered_depths = valid_depths[(valid_depths >= lower_bound) & 
                                          (valid_depths <= upper_bound)]
        else:
            filtered_depths = valid_depths
        
        if len(filtered_depths) == 0:
            return np.nan
        
        # Use percentile 10% (bagian terdalam)
        z_base = np.percentile(filtered_depths, 10)
        return float(z_base)
    
    def _calculate_diameter(self,
                           bbox: Tuple[int, int, int, int],
                           z_avg: float,
                           use_mask: bool = False,
                           mask: Optional[np.ndarray] = None) -> float:
        """
        Hitung diameter pothole dalam cm
        
        Args:
            bbox: Bounding box (x1, y1, x2, y2)
            z_avg: Average depth (meter)
            use_mask: Gunakan segmentation mask jika tersedia
            mask: Segmentation mask (optional)
            
        Returns:
            Diameter dalam cm
        """
        x1, y1, x2, y2 = bbox
        
        if use_mask and mask is not None:
            # Use segmentation mask - fit ellipse
            contours, _ = cv2.findContours(mask.astype(np.uint8), 
                                          cv2.RETR_EXTERNAL, 
                                          cv2.CHAIN_APPROX_SIMPLE)
            if len(contours) > 0:
                # Find largest contour
                largest_contour = max(contours, key=cv2.contourArea)
                if len(largest_contour) >= 5:  # Need at least 5 points for ellipse
                    ellipse = cv2.fitEllipse(largest_contour)
                    (center, axes, angle) = ellipse
                    major_axis_px = max(axes)
                    # Convert to cm
                    diameter_cm = (major_axis_px * z_avg * 100) / self.fx
                    return float(diameter_cm)
        
        # Fallback: use bounding box width
        width_px = x2 - x1
        
        # Skip tiny bounding boxes yang menghasilkan diameter sangat noisy
        if width_px < 8:
            return float('nan')  # Skip bbox terlalu kecil
        
        diameter_cm = (width_px * z_avg * 100) / self.fx
        return float(diameter_cm)
    
    def _calculate_measurements(self,
                                detections: List,
                                depth_map_abs: np.ndarray) -> List[PotholeMeasurement]:
        """
        Hitung diameter dan kedalaman untuk setiap deteksi
        
        Args:
            detections: List detections dari YOLO (results[0].boxes)
            depth_map_abs: Depth map absolut (meter)
            
        Returns:
            List of PotholeMeasurement objects
        """
        measurements = []
        
        for det in detections:
            # Extract bounding box - gunakan API Ultralytics yang stabil
            # Support untuk berbagai versi API
            if hasattr(det, 'xyxy'):
                if hasattr(det.xyxy, 'cpu'):
                    bbox = det.xyxy[0].cpu().numpy()  # (x1, y1, x2, y2)
                else:
                    bbox = det.xyxy[0]  # Already numpy
            elif hasattr(det, 'boxes'):
                bbox = det.boxes.xyxy[0].cpu().numpy()
            else:
                continue  # Skip jika format tidak dikenal
            
            # Extract confidence
            if hasattr(det, 'conf'):
                if hasattr(det.conf, 'cpu'):
                    confidence = float(det.conf[0].cpu().numpy())
                else:
                    confidence = float(det.conf[0])
            elif hasattr(det, 'boxes'):
                confidence = float(det.boxes.conf[0].cpu().numpy())
            else:
                confidence = 0.5  # Default
            
            # Skip jika confidence terlalu rendah
            if confidence < self.conf_threshold:
                continue
            
            # Extract ROI dan border depth
            roi_depth, border_depth = self._extract_roi_depth(depth_map_abs, bbox)
            
            # Calculate Z_surface (median dari border)
            z_surface = self._calculate_z_surface(border_depth)
            if np.isnan(z_surface):
                continue
            
            # Calculate Z_base (percentile 10% dari ROI dengan IQR filtering)
            z_base = self._calculate_z_base(roi_depth)
            if np.isnan(z_base):
                continue
            
            # Calculate Z_avg
            z_avg = (z_surface + z_base) / 2
            
            # Calculate diameter
            mask = None
            if hasattr(det, 'masks') and det.masks is not None:
                try:
                    mask_data = det.masks.data
                    if mask_data is not None and len(mask_data) > 0:
                        mask = mask_data[0].cpu().numpy()
                        # Resize mask to image size
                        h, w = depth_map_abs.shape
                        mask = cv2.resize(mask, (w, h))
                        diameter_cm = self._calculate_diameter(bbox, z_avg, use_mask=True, mask=mask)
                    else:
                        # Fallback to bbox if mask is empty
                        diameter_cm = self._calculate_diameter(bbox, z_avg, use_mask=False)
                except Exception as e:
                    # Fallback to bbox if mask processing fails
                    print(f"⚠️  Warning: Error processing mask: {e}")
                    diameter_cm = self._calculate_diameter(bbox, z_avg, use_mask=False)
            else:
                # Use bounding box
                diameter_cm = self._calculate_diameter(bbox, z_avg, use_mask=False)
            
            # Calculate depth (cm)
            depth_cm = (z_surface - z_base) * 100
            
            # Skip jika diameter NaN (bbox terlalu kecil)
            if np.isnan(diameter_cm):
                continue
            
            # Create measurement object
            measurement = PotholeMeasurement(
                bbox=tuple(bbox.astype(int)),
                confidence=confidence,
                diameter_cm=diameter_cm,
                depth_cm=depth_cm,
                z_surface=z_surface,
                z_base=z_base,
                z_avg=z_avg,
                mask=mask
            )
            
            measurements.append(measurement)
        
        return measurements
    
    def process_frame(self, image: np.ndarray) -> Dict:
        """
        Process single frame: Detection + Depth Estimation + Measurement + Tracking
        
        Args:
            image: Input image (BGR format)
            
        Returns:
            Dictionary dengan hasil:
            - detections: YOLO detections
            - depth_map_relative: Depth map relatif
            - depth_map_absolute: Depth map absolut
            - measurements: List of PotholeMeasurement
            - tracks: List of Track objects (jika tracking enabled)
            - image_undistorted: Undistorted image
        """
        # Step 1: Undistort image (jika kalibrasi tersedia)
        image_undistorted = self.depth_estimator.undistort_image(image)
        
        # Step 2: YOLO Detection - gunakan API yang stabil
        results = self.yolo_model(image_undistorted, conf=self.conf_threshold)
        res = results[0] if len(results) > 0 else None
        
        # Step 3: Depth Estimation (selalu dilakukan untuk konsistensi)
        depth_map_rel, _ = self.depth_estimator.estimate_depth(image_undistorted)
        
        # Step 4: Scale Recovery
        if self.depth_estimator.camera_params is not None and not self.depth_estimator._using_dummy:
            depth_map_abs, scale_factor = self.depth_estimator.scale_recovery(depth_map_rel)
        else:
            if self.depth_estimator._using_dummy:
                print("⚠️  Warning: Using dummy depth map, scale recovery skipped")
            depth_map_abs = depth_map_rel
            scale_factor = 1.0
        
        if res is None:
            # No detections
            return {
                'detections': [],
                'depth_map_relative': depth_map_rel,
                'depth_map_absolute': depth_map_abs,
                'measurements': [],
                'tracks': [],
                'image_undistorted': image_undistorted,
                'scale_factor': scale_factor
            }
        
        # Extract detections dengan API yang kompatibel
        if hasattr(res, 'boxes'):
            detections = res.boxes
        else:
            detections = res
        
        # Step 5: Calculate Measurements
        measurements = self._calculate_measurements(detections, depth_map_abs)
        
        # Step 6: Tracking (jika enabled)
        tracks = []
        if self.enable_tracking and self.tracker is not None:
            tracks = self.tracker.update(measurements)
        
        return {
            'detections': results,
            'depth_map_relative': depth_map_rel,
            'depth_map_absolute': depth_map_abs,
            'scale_factor': scale_factor,
            'measurements': measurements,
            'tracks': tracks,
            'image_undistorted': image_undistorted
        }
    
    def visualize_results(self,
                         image: np.ndarray,
                         results: Dict,
                         show_depth: bool = True,
                         show_measurements: bool = True,
                         show_tracks: bool = True) -> np.ndarray:
        """
        Visualisasi hasil detection, measurement, dan tracking
        
        Args:
            image: Original image
            results: Dictionary dari process_frame()
            show_depth: Tampilkan depth overlay
            show_measurements: Tampilkan measurement annotations
            show_tracks: Tampilkan track IDs
            
        Returns:
            Visualized image
        """
        vis_image = image.copy()
        
        # Draw depth overlay
        if show_depth and 'depth_map_absolute' in results:
            depth_colored = self.depth_estimator.visualize_depth(
                results['depth_map_absolute'], colormap='jet'
            )
            vis_image = self.depth_estimator.create_depth_overlay(
                vis_image, depth_colored, alpha=0.3
            )
        
        # Draw tracks (jika tracking enabled)
        if show_tracks and 'tracks' in results and len(results['tracks']) > 0:
            for track in results['tracks']:
                x1, y1, x2, y2 = track.bbox.astype(int)
                track_id = track.track_id
                measurement = track.measurement
                
                # Color berdasarkan track ID (untuk visualisasi)
                color = self._get_track_color(track_id)
                
                # Draw bounding box dengan track ID
                cv2.rectangle(vis_image, (x1, y1), (x2, y2), color, 2)
                
                # Draw track ID
                track_label = f"ID: {track_id}"
                (text_w, text_h), _ = cv2.getTextSize(track_label, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2)
                cv2.rectangle(vis_image, (x1, y1 - text_h - 60), 
                            (x1 + max(text_w, 200), y1), color, -1)
                
                # Text dengan track info
                cv2.putText(vis_image, track_label, (x1, y1 - 45),
                          cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
                
                if show_measurements:
                    # Show filtered measurements (dari Kalman filter)
                    filtered_d, filtered_h = track.get_filtered_measurements()
                    info = f"D: {filtered_d:.1f}cm (KF), H: {filtered_h:.1f}cm (KF)"
                    conf_text = f"Conf: {measurement.confidence:.2f} | Age: {track.age}"
                    cv2.putText(vis_image, info, (x1, y1 - 25),
                              cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
                    cv2.putText(vis_image, conf_text, (x1, y1 - 10),
                              cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1)
        
        # Draw detections tanpa track (jika tracking disabled atau detections tidak ter-track)
        elif show_measurements and 'measurements' in results:
            for i, measurement in enumerate(results['measurements']):
                x1, y1, x2, y2 = measurement.bbox
                
                # Draw bounding box
                cv2.rectangle(vis_image, (x1, y1), (x2, y2), (0, 255, 0), 2)
                
                # Draw measurement info
                label = f"Pothole {i+1}"
                info = f"D: {measurement.diameter_cm:.1f}cm, H: {measurement.depth_cm:.1f}cm"
                conf_text = f"Conf: {measurement.confidence:.2f}"
                
                # Background for text
                (text_w, text_h), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2)
                cv2.rectangle(vis_image, (x1, y1 - text_h - 50), 
                            (x1 + max(text_w, 200), y1), (0, 255, 0), -1)
                
                # Text
                cv2.putText(vis_image, label, (x1, y1 - 35),
                          cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 2)
                cv2.putText(vis_image, info, (x1, y1 - 20),
                          cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)
                cv2.putText(vis_image, conf_text, (x1, y1 - 5),
                          cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 0, 0), 1)
        
        return vis_image
    
    def _get_track_color(self, track_id: int) -> Tuple[int, int, int]:
        """Get consistent color untuk track ID"""
        # Generate color berdasarkan track ID
        np.random.seed(track_id)
        color = np.random.randint(0, 255, 3).tolist()
        return tuple(color)
    
    def process_video(self,
                     video_path: Union[str, Path],
                     output_path: Optional[Union[str, Path]] = None,
                     show_preview: bool = False,
                     frame_skip: int = 1,
                     save_measurements: bool = True) -> Dict:
        """
        Process video dengan detection dan measurement
        
        Args:
            video_path: Path ke input video
            output_path: Path untuk output video (None = auto-generate)
            show_preview: Tampilkan preview saat processing
            frame_skip: Process setiap N frame (1 = semua frame)
            save_measurements: Simpan measurements ke JSON
            
        Returns:
            Dictionary dengan summary results
        """
        video_path = Path(video_path)
        if not video_path.exists():
            raise FileNotFoundError(f"Video tidak ditemukan: {video_path}")
        
        # Open video
        cap = cv2.VideoCapture(str(video_path))
        if not cap.isOpened():
            raise ValueError(f"Gagal membuka video: {video_path}")
        
        # Get video properties
        fps = int(cap.get(cv2.CAP_PROP_FPS))
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        
        print(f"\n🎬 Processing video: {video_path.name}")
        print(f"   Resolution: {width}x{height}")
        print(f"   FPS: {fps}")
        print(f"   Total frames: {total_frames}")
        print(f"   Frame skip: {frame_skip}")
        
        # Setup output video
        if output_path is None:
            output_path = video_path.parent / f"{video_path.stem}_detected.avi"
        else:
            output_path = Path(output_path)
        
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        out = cv2.VideoWriter(str(output_path), fourcc, fps, (width, height))
        
        frame_count = 0
        processed_count = 0
        all_measurements = []  # Store all measurements across frames
        
        print("\n🔄 Processing frames...")
        try:
            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                
                # Skip frames jika diperlukan
                if frame_count % frame_skip != 0:
                    frame_count += 1
                    continue
                
                # Process frame
                results = self.process_frame(frame)
                
                # Store measurements with frame number and track ID
                if 'tracks' in results and len(results['tracks']) > 0:
                    # Store tracked measurements (dengan Kalman-filtered values)
                    for track in results['tracks']:
                        filtered_d, filtered_h = track.get_filtered_measurements()
                        measurement_dict = track.measurement.to_dict()
                        # Override dengan filtered values
                        measurement_dict['diameter_cm'] = filtered_d
                        measurement_dict['depth_cm'] = filtered_h
                        all_measurements.append({
                            'frame': frame_count,
                            'track_id': track.track_id,
                            'age': track.age,
                            'hit_streak': track.hit_streak,
                            'is_filtered': True,  # Indikator bahwa ini filtered
                            **measurement_dict
                        })
                else:
                    # Store untracked measurements
                    for measurement in results['measurements']:
                        all_measurements.append({
                            'frame': frame_count,
                            'track_id': None,
                            **measurement.to_dict()
                        })
                
                # Visualize
                vis_frame = self.visualize_results(frame, results)
                
                # Write frame
                out.write(vis_frame)
                processed_count += 1
                
                # Show preview
                if show_preview:
                    cv2.imshow('Pothole Detection', vis_frame)
                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        print("⏹️  Stopped by user")
                        break
                
                # Progress
                if processed_count % 10 == 0:
                    progress = (frame_count / total_frames) * 100
                    print(f"   Progress: {processed_count} frames processed ({progress:.1f}%)")
                
                frame_count += 1
                
        except KeyboardInterrupt:
            print("\n⏹️  Interrupted by user")
        finally:
            cap.release()
            out.release()
            if show_preview:
                cv2.destroyAllWindows()
        
        # Save measurements to JSON
        if save_measurements and len(all_measurements) > 0:
            import json
            measurements_file = output_path.parent / f"{video_path.stem}_measurements.json"
            with open(measurements_file, 'w') as f:
                json.dump(all_measurements, f, indent=2)
            print(f"💾 Measurements saved to: {measurements_file}")
        
        summary = {
            'total_frames': total_frames,
            'processed_frames': processed_count,
            'total_detections': len(all_measurements),
            'output_video': str(output_path),
            'measurements_file': str(measurements_file) if save_measurements else None
        }
        
        print(f"\n✅ Video processing selesai!")
        print(f"   Processed: {processed_count} frames")
        print(f"   Total detections: {len(all_measurements)}")
        print(f"   Output: {output_path}")
        
        return summary

