"""
Pothole Tracker - BoT-SORT Implementation
Tracking pothole lintas frame dengan ID konsisten

Author: Skripsi Project
Date: 2025
"""

import cv2
import numpy as np
from typing import List, Dict, Tuple, Optional, TYPE_CHECKING
from collections import deque
import warnings
warnings.filterwarnings('ignore')

if TYPE_CHECKING:
    from pothole_detection_system import PotholeMeasurement

try:
    from kalman_filter import MeasurementKalmanFilter
    KALMAN_AVAILABLE = True
except ImportError:
    KALMAN_AVAILABLE = False
    MeasurementKalmanFilter = None


class Track:
    """Class untuk menyimpan state track"""
    def __init__(self, track_id: int, bbox: np.ndarray, measurement: 'PotholeMeasurement', frame_id: int):
        """
        Initialize track
        
        Args:
            track_id: Unique track ID
            bbox: Bounding box [x1, y1, x2, y2]
            measurement: PotholeMeasurement object
            frame_id: Current frame ID
        """
        self.track_id = track_id
        self.bbox = bbox.astype(float)
        self.measurement = measurement
        self.frame_id = frame_id
        
        # Track state
        self.is_confirmed = False
        self.time_since_update = 0
        self.hit_streak = 1
        self.age = 1
        
        # Measurement history (untuk Kalman filter nanti)
        self.measurement_history = deque(maxlen=30)  # Store last 30 measurements
        self.measurement_history.append(measurement)
        
        # Kalman filter untuk temporal filtering
        if KALMAN_AVAILABLE:
            self.kalman_filter = MeasurementKalmanFilter(
                initial_diameter=measurement.diameter_cm,
                initial_depth=measurement.depth_cm,
                process_noise=0.1,
                measurement_noise=1.0
            )
        else:
            self.kalman_filter = None
    
    def update(self, bbox: np.ndarray, measurement, frame_id: int, apply_kalman: bool = True):
        """
        Update track dengan detection baru
        
        Args:
            bbox: Bounding box
            measurement: PotholeMeasurement object
            frame_id: Current frame ID
            apply_kalman: Apply Kalman filter untuk smooth measurements
        """
        self.bbox = bbox.astype(float)
        self.frame_id = frame_id
        self.time_since_update = 0
        self.hit_streak += 1
        self.age += 1
        
        # Apply Kalman filter jika available
        if apply_kalman and self.kalman_filter is not None:
            # Update Kalman filter dengan measurement baru
            filtered_diameter, filtered_depth = self.kalman_filter.update(
                measurement.diameter_cm,
                measurement.depth_cm
            )
            
            # Create filtered measurement (copy original dengan filtered values)
            from pothole_detection_system import PotholeMeasurement
            filtered_measurement = PotholeMeasurement(
                bbox=measurement.bbox,
                confidence=measurement.confidence,
                diameter_cm=filtered_diameter,
                depth_cm=filtered_depth,
                z_surface=measurement.z_surface,
                z_base=measurement.z_base,
                z_avg=measurement.z_avg,
                mask=measurement.mask
            )
            self.measurement = filtered_measurement
        else:
            self.measurement = measurement
        
        self.measurement_history.append(self.measurement)
    
    def predict(self):
        """Predict next position dan measurements"""
        # Predict bbox position (simple linear motion model)
        if len(self.measurement_history) >= 2:
            # Estimate velocity dari 2 measurement terakhir
            prev_bbox = np.array(self.measurement_history[-2].bbox, dtype=float)
            curr_bbox = np.array(self.measurement_history[-1].bbox, dtype=float)
            
            # Simple velocity estimation
            velocity = (curr_bbox - prev_bbox) * 0.5  # Damping factor
            self.bbox = self.bbox + velocity
        
        # Predict measurements dengan Kalman filter
        if self.kalman_filter is not None:
            pred_diameter, pred_depth = self.kalman_filter.predict()
            # Update measurement dengan predicted values (untuk association)
            if hasattr(self, 'measurement') and self.measurement is not None:
                from pothole_detection_system import PotholeMeasurement
                self.measurement = PotholeMeasurement(
                    bbox=tuple(self.bbox.astype(int)),
                    confidence=self.measurement.confidence,
                    diameter_cm=pred_diameter,
                    depth_cm=pred_depth,
                    z_surface=self.measurement.z_surface,
                    z_base=self.measurement.z_base,
                    z_avg=self.measurement.z_avg,
                    mask=self.measurement.mask
                )
        
        self.age += 1
        self.time_since_update += 1
    
    def get_filtered_measurements(self) -> Tuple[float, float]:
        """
        Get Kalman-filtered measurements
        
        Returns:
            Tuple (filtered_diameter, filtered_depth) atau (raw_diameter, raw_depth) jika filter tidak available
        """
        if self.kalman_filter is not None:
            return self.kalman_filter.get_filtered_measurements()
        elif self.measurement is not None:
            return (self.measurement.diameter_cm, self.measurement.depth_cm)
        else:
            return (0.0, 0.0)
    
    def get_state(self) -> np.ndarray:
        """Get current state (bbox)"""
        return self.bbox.copy()


class PotholeTracker:
    """
    BoT-SORT inspired tracker untuk pothole tracking
    Menggunakan IoU association dan Kalman Filter untuk temporal filtering
    """
    
    def __init__(self,
                 max_age: int = 30,
                 min_hits: int = 3,
                 iou_threshold: float = 0.3,
                 match_threshold: float = 0.5,
                 enable_kalman: bool = True,
                 kalman_process_noise: float = 0.1,
                 kalman_measurement_noise: float = 1.0):
        """
        Initialize Pothole Tracker
        
        Args:
            max_age: Maximum frames to keep lost tracks
            min_hits: Minimum hits to confirm track
            iou_threshold: IoU threshold for association
            match_threshold: Minimum match score for association
            enable_kalman: Enable Kalman filter untuk temporal filtering
            kalman_process_noise: Process noise untuk Kalman filter
            kalman_measurement_noise: Measurement noise untuk Kalman filter
        """
        self.max_age = max_age
        self.min_hits = min_hits
        self.iou_threshold = iou_threshold
        self.match_threshold = match_threshold
        self.enable_kalman = enable_kalman and KALMAN_AVAILABLE
        self.kalman_process_noise = kalman_process_noise
        self.kalman_measurement_noise = kalman_measurement_noise
        
        self.tracks: List[Track] = []
        self.frame_count = 0
        self.next_id = 1
    
    def _calculate_iou(self, bbox1: np.ndarray, bbox2: np.ndarray) -> float:
        """
        Calculate Intersection over Union (IoU) between two bounding boxes
        
        Args:
            bbox1: [x1, y1, x2, y2]
            bbox2: [x1, y1, x2, y2]
            
        Returns:
            IoU score (0-1)
        """
        x1_1, y1_1, x2_1, y2_1 = bbox1
        x1_2, y1_2, x2_2, y2_2 = bbox2
        
        # Calculate intersection
        x1_i = max(x1_1, x1_2)
        y1_i = max(y1_1, y1_2)
        x2_i = min(x2_1, x2_2)
        y2_i = min(y2_1, y2_2)
        
        if x2_i < x1_i or y2_i < y1_i:
            return 0.0
        
        intersection = (x2_i - x1_i) * (y2_i - y1_i)
        
        # Calculate union
        area1 = (x2_1 - x1_1) * (y2_1 - y1_1)
        area2 = (x2_2 - x1_2) * (y2_2 - y1_2)
        union = area1 + area2 - intersection
        
        if union == 0:
            return 0.0
        
        return intersection / union
    
    def _calculate_center_distance(self, bbox1: np.ndarray, bbox2: np.ndarray) -> float:
        """
        Calculate center distance between two bounding boxes
        
        Args:
            bbox1: [x1, y1, x2, y2]
            bbox2: [x1, y1, x2, y2]
            
        Returns:
            Distance in pixels
        """
        cx1 = (bbox1[0] + bbox1[2]) / 2
        cy1 = (bbox1[1] + bbox1[3]) / 2
        cx2 = (bbox2[0] + bbox2[2]) / 2
        cy2 = (bbox2[1] + bbox2[3]) / 2
        
        return np.sqrt((cx1 - cx2)**2 + (cy1 - cy2)**2)
    
    def _associate_detections_to_tracks(self,
                                       detections: List[Tuple[np.ndarray, any]],
                                       tracks: List[Track]) -> Tuple[np.ndarray, List[int], List[int]]:
        """
        Associate detections to tracks menggunakan IoU
        
        Args:
            detections: List of (bbox, measurement) tuples
            tracks: List of active tracks
            
        Returns:
            Tuple (matches, unmatched_dets, unmatched_trks)
            - matches: Array of [det_idx, trk_idx] pairs
            - unmatched_dets: List of unmatched detection indices
            - unmatched_trks: List of unmatched track indices
        """
        if len(tracks) == 0:
            return np.empty((0, 2), dtype=int), list(range(len(detections))), []
        
        if len(detections) == 0:
            return np.empty((0, 2), dtype=int), [], list(range(len(tracks)))
        
        # Calculate cost matrix (IoU)
        cost_matrix = np.zeros((len(detections), len(tracks)))
        for i, (det_bbox, _) in enumerate(detections):
            for j, track in enumerate(tracks):
                # Predict track position
                track.predict()
                cost_matrix[i, j] = 1.0 - self._calculate_iou(det_bbox, track.get_state())
        
        # Hungarian algorithm (simple greedy matching untuk sekarang)
        # Bisa di-upgrade ke scipy.optimize.linear_sum_assignment nanti
        matches = []
        unmatched_dets = list(range(len(detections)))
        unmatched_trks = list(range(len(tracks)))
        
        # Greedy matching (prioritize high IoU)
        for _ in range(min(len(detections), len(tracks))):
            if len(unmatched_dets) == 0 or len(unmatched_trks) == 0:
                break
            
            # Find best match
            min_cost = float('inf')
            best_det = -1
            best_trk = -1
            
            for i in unmatched_dets:
                for j in unmatched_trks:
                    cost = cost_matrix[i, j]
                    iou = 1.0 - cost
                    if iou >= self.iou_threshold and cost < min_cost:
                        min_cost = cost
                        best_det = i
                        best_trk = j
            
            if best_det != -1 and best_trk != -1:
                matches.append([best_det, best_trk])
                unmatched_dets.remove(best_det)
                unmatched_trks.remove(best_trk)
            else:
                break
        
        return np.array(matches), unmatched_dets, unmatched_trks
    
    def update(self, measurements: List) -> List[Track]:
        """
        Update tracker dengan measurements baru
        
        Args:
            measurements: List of PotholeMeasurement objects
            
        Returns:
            List of confirmed tracks
        """
        self.frame_count += 1
        
        # Prepare detections
        detections = []
        for measurement in measurements:
            bbox = np.array(measurement.bbox, dtype=float)
            detections.append((bbox, measurement))
        
        # Separate confirmed and unconfirmed tracks
        confirmed_tracks = [t for t in self.tracks if t.is_confirmed]
        unconfirmed_tracks = [t for t in self.tracks if not t.is_confirmed]
        
        # Associate detections to confirmed tracks
        matches, unmatched_dets, unmatched_trks = self._associate_detections_to_tracks(
            detections, confirmed_tracks
        )
        
        # Update matched tracks
        for det_idx, trk_idx in matches:
            bbox, measurement = detections[det_idx]
            confirmed_tracks[trk_idx].update(bbox, measurement, self.frame_count, 
                                            apply_kalman=self.enable_kalman)
        
        # Handle unmatched confirmed tracks (lost tracks)
        for trk_idx in unmatched_trks:
            confirmed_tracks[trk_idx].time_since_update += 1
        
        # Associate unmatched detections to unconfirmed tracks
        if len(unconfirmed_tracks) > 0 and len(unmatched_dets) > 0:
            unmatched_detections = [detections[i] for i in unmatched_dets]
            matches2, unmatched_dets2, unmatched_trks2 = self._associate_detections_to_tracks(
                unmatched_detections, unconfirmed_tracks
            )
            
            # Update matched unconfirmed tracks
            for det_idx, trk_idx in matches2:
                bbox, measurement = unmatched_detections[det_idx]
                unconfirmed_tracks[trk_idx].update(bbox, measurement, self.frame_count,
                                                  apply_kalman=self.enable_kalman)
            
            # Create new tracks for remaining unmatched detections
            for det_idx in unmatched_dets2:
                bbox, measurement = unmatched_detections[det_idx]
                new_track = Track(self.next_id, bbox, measurement, self.frame_count)
                # Initialize Kalman filter jika enabled
                if self.enable_kalman and new_track.kalman_filter is not None:
                    new_track.kalman_filter.process_noise = self.kalman_process_noise
                    new_track.kalman_filter.measurement_noise = self.kalman_measurement_noise
                self.tracks.append(new_track)
                self.next_id += 1
        else:
            # Create new tracks for all unmatched detections
            for det_idx in unmatched_dets:
                bbox, measurement = detections[det_idx]
                new_track = Track(self.next_id, bbox, measurement, self.frame_count)
                # Initialize Kalman filter jika enabled
                if self.enable_kalman and new_track.kalman_filter is not None:
                    new_track.kalman_filter.process_noise = self.kalman_process_noise
                    new_track.kalman_filter.measurement_noise = self.kalman_measurement_noise
                self.tracks.append(new_track)
                self.next_id += 1
        
        # Update track states
        for track in self.tracks:
            if track.hit_streak >= self.min_hits:
                track.is_confirmed = True
        
        # Remove old tracks
        self.tracks = [t for t in self.tracks if t.time_since_update <= self.max_age]
        
        # Return confirmed tracks
        confirmed = [t for t in self.tracks if t.is_confirmed and t.time_since_update == 0]
        return confirmed
    
    def get_track_by_id(self, track_id: int) -> Optional[Track]:
        """Get track by ID"""
        for track in self.tracks:
            if track.track_id == track_id:
                return track
        return None
    
    def get_all_tracks(self) -> List[Track]:
        """Get all active tracks"""
        return self.tracks.copy()
    
    def reset(self):
        """Reset tracker"""
        self.tracks = []
        self.frame_count = 0
        self.next_id = 1

