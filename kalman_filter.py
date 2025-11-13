"""
Kalman Filter untuk Temporal Filtering Measurements
Stabilisasi pengukuran diameter & depth lintas frame

Author: Skripsi Project
Date: 2025
"""

import numpy as np
from typing import Tuple, Optional


class MeasurementKalmanFilter:
    """
    Kalman Filter untuk filtering temporal measurements (diameter & depth)
    
    State Vector: [diameter, depth, velocity_diameter, velocity_depth]^T
    Measurement: [diameter, depth]^T
    """
    
    def __init__(self,
                 initial_diameter: float = 0.0,
                 initial_depth: float = 0.0,
                 process_noise: float = 0.1,
                 measurement_noise: float = 1.0):
        """
        Initialize Kalman Filter
        
        Args:
            initial_diameter: Initial diameter estimate (cm)
            initial_depth: Initial depth estimate (cm)
            process_noise: Process noise covariance (Q) - seberapa cepat state berubah
            measurement_noise: Measurement noise covariance (R) - seberapa percaya measurement
        """
        # State vector: [diameter, depth, velocity_diameter, velocity_depth]
        self.state = np.array([initial_diameter, initial_depth, 0.0, 0.0], dtype=float)
        
        # State covariance matrix (4x4)
        self.covariance = np.eye(4, dtype=float) * 100.0  # Initial uncertainty
        
        # State transition matrix (constant velocity model)
        # x_k = F * x_{k-1}
        # [diameter]   [1  0  dt  0 ] [diameter]
        # [depth]    = [0  1  0  dt] [depth]
        # [v_diam]    [0  0  1   0 ] [v_diam]
        # [v_depth]   [0  0  0   1 ] [v_depth]
        dt = 1.0  # Time step (1 frame)
        self.F = np.array([
            [1.0, 0.0, dt,  0.0],
            [0.0, 1.0, 0.0, dt],
            [0.0, 0.0, 1.0, 0.0],
            [0.0, 0.0, 0.0, 1.0]
        ], dtype=float)
        
        # Observation matrix (measure diameter dan depth saja)
        # z = H * x
        # [diameter]   [1  0  0  0] [diameter]
        # [depth]    = [0  1  0  0] [depth]
        #                        [v_diam]
        #                        [v_depth]
        self.H = np.array([
            [1.0, 0.0, 0.0, 0.0],
            [0.0, 1.0, 0.0, 0.0]
        ], dtype=float)
        
        # Process noise covariance (Q)
        # Mengontrol seberapa cepat state bisa berubah
        self._process_noise = process_noise
        self._measurement_noise = measurement_noise
        self._update_noise_matrices()
        
        # Track initialization
        self.is_initialized = False
        self.update_count = 0
    
    def _update_noise_matrices(self):
        """Update noise matrices dengan current parameters"""
        # Process noise covariance (Q)
        self.Q = np.eye(4, dtype=float) * self._process_noise
        self.Q[0, 0] = self._process_noise * 0.5  # Diameter change slower
        self.Q[1, 1] = self._process_noise * 0.5  # Depth change slower
        self.Q[2, 2] = self._process_noise * 2.0   # Velocity can change faster
        self.Q[3, 3] = self._process_noise * 2.0
        
        # Measurement noise covariance (R)
        # Mengontrol seberapa percaya pada measurement
        self.R = np.eye(2, dtype=float) * self._measurement_noise
        self.R[0, 0] = self._measurement_noise * 1.0  # Diameter measurement noise
        self.R[1, 1] = self._measurement_noise * 1.0  # Depth measurement noise
    
    @property
    def process_noise(self) -> float:
        return self._process_noise
    
    @process_noise.setter
    def process_noise(self, value: float):
        self._process_noise = value
        self._update_noise_matrices()
    
    @property
    def measurement_noise(self) -> float:
        return self._measurement_noise
    
    @measurement_noise.setter
    def measurement_noise(self, value: float):
        self._measurement_noise = value
        self._update_noise_matrices()
    
    def initialize(self, diameter: float, depth: float):
        """
        Initialize filter dengan measurement pertama
        
        Args:
            diameter: Initial diameter measurement (cm)
            depth: Initial depth measurement (cm)
        """
        self.state[0] = diameter
        self.state[1] = depth
        self.state[2] = 0.0  # velocity_diameter
        self.state[3] = 0.0  # velocity_depth
        
        # High initial uncertainty
        self.covariance = np.eye(4, dtype=float) * 100.0
        self.is_initialized = True
        self.update_count = 1
    
    def predict(self) -> Tuple[float, float]:
        """
        Prediction step: Predict next state berdasarkan model
        
        Returns:
            Tuple (predicted_diameter, predicted_depth)
        """
        if not self.is_initialized:
            return (0.0, 0.0)
        
        # Predict state
        self.state = self.F @ self.state
        
        # Predict covariance
        self.covariance = self.F @ self.covariance @ self.F.T + self.Q
        
        return (float(self.state[0]), float(self.state[1]))
    
    def update(self, diameter: float, depth: float) -> Tuple[float, float]:
        """
        Update step: Update state dengan measurement baru
        
        Args:
            diameter: Measured diameter (cm)
            depth: Measured depth (cm)
            
        Returns:
            Tuple (filtered_diameter, filtered_depth)
        """
        # Initialize jika belum
        if not self.is_initialized:
            self.initialize(diameter, depth)
            return (diameter, depth)
        
        # Prediction step
        self.predict()
        
        # Measurement vector
        z = np.array([diameter, depth], dtype=float)
        
        # Innovation (measurement residual)
        innovation = z - self.H @ self.state
        
        # Innovation covariance
        S = self.H @ self.covariance @ self.H.T + self.R
        
        # Kalman gain
        K = self.covariance @ self.H.T @ np.linalg.inv(S)
        
        # Update state
        self.state = self.state + K @ innovation
        
        # Update covariance
        I = np.eye(4, dtype=float)
        self.covariance = (I - K @ self.H) @ self.covariance
        
        self.update_count += 1
        
        return (float(self.state[0]), float(self.state[1]))
    
    def get_state(self) -> Tuple[float, float, float, float]:
        """
        Get current state
        
        Returns:
            Tuple (diameter, depth, velocity_diameter, velocity_depth)
        """
        return (
            float(self.state[0]),
            float(self.state[1]),
            float(self.state[2]),
            float(self.state[3])
        )
    
    def get_filtered_measurements(self) -> Tuple[float, float]:
        """
        Get filtered measurements (diameter & depth)
        
        Returns:
            Tuple (filtered_diameter, filtered_depth)
        """
        return (float(self.state[0]), float(self.state[1]))
    
    def reset(self):
        """Reset filter"""
        self.state = np.array([0.0, 0.0, 0.0, 0.0], dtype=float)
        self.covariance = np.eye(4, dtype=float) * 100.0
        self.is_initialized = False
        self.update_count = 0
    
    def get_uncertainty(self) -> Tuple[float, float]:
        """
        Get uncertainty (standard deviation) untuk diameter dan depth
        
        Returns:
            Tuple (diameter_std, depth_std)
        """
        diameter_std = np.sqrt(self.covariance[0, 0])
        depth_std = np.sqrt(self.covariance[1, 1])
        return (float(diameter_std), float(depth_std))

