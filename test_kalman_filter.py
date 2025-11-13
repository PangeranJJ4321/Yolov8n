"""
Test script untuk Kalman Filter
Demonstrasi temporal filtering untuk measurements
"""

import numpy as np
import matplotlib.pyplot as plt
from kalman_filter import MeasurementKalmanFilter

# Simulasi noisy measurements
np.random.seed(42)
true_diameter = 45.0  # cm
true_depth = 10.0    # cm

# Generate noisy measurements (simulasi fluktuasi)
n_frames = 50
measurements_d = []
measurements_h = []
filtered_d = []
filtered_h = []

# Initialize Kalman filter
kf = MeasurementKalmanFilter(
    initial_diameter=true_diameter,
    initial_depth=true_depth,
    process_noise=0.1,
    measurement_noise=1.0
)

# Simulate measurements dengan noise
for i in range(n_frames):
    # Add noise to true values
    noisy_d = true_diameter + np.random.normal(0, 2.0)  # ±2cm noise
    noisy_h = true_depth + np.random.normal(0, 0.5)    # ±0.5cm noise
    
    # Add occasional outliers
    if i % 10 == 0:
        noisy_d += np.random.normal(0, 5.0)  # Larger outlier
        noisy_h += np.random.normal(0, 2.0)
    
    measurements_d.append(noisy_d)
    measurements_h.append(noisy_h)
    
    # Update Kalman filter
    filtered_d_val, filtered_h_val = kf.update(noisy_d, noisy_h)
    filtered_d.append(filtered_d_val)
    filtered_h.append(filtered_h_val)

# Visualize results
fig, axes = plt.subplots(2, 1, figsize=(12, 8))

# Plot diameter
axes[0].plot(range(n_frames), measurements_d, 'b.', alpha=0.5, label='Raw Measurements')
axes[0].plot(range(n_frames), filtered_d, 'r-', linewidth=2, label='Kalman Filtered')
axes[0].axhline(y=true_diameter, color='g', linestyle='--', linewidth=2, label='True Value')
axes[0].set_xlabel('Frame')
axes[0].set_ylabel('Diameter (cm)')
axes[0].set_title('Kalman Filter: Diameter Filtering')
axes[0].legend()
axes[0].grid(True, alpha=0.3)

# Plot depth
axes[1].plot(range(n_frames), measurements_h, 'b.', alpha=0.5, label='Raw Measurements')
axes[1].plot(range(n_frames), filtered_h, 'r-', linewidth=2, label='Kalman Filtered')
axes[1].axhline(y=true_depth, color='g', linestyle='--', linewidth=2, label='True Value')
axes[1].set_xlabel('Frame')
axes[1].set_ylabel('Depth (cm)')
axes[1].set_title('Kalman Filter: Depth Filtering')
axes[1].legend()
axes[1].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('kalman_filter_test.png', dpi=150, bbox_inches='tight')
print("✅ Test plot saved to kalman_filter_test.png")

# Calculate statistics
raw_d_std = np.std(measurements_d)
raw_h_std = np.std(measurements_h)
filtered_d_std = np.std(filtered_d)
filtered_h_std = np.std(filtered_h)

print(f"\n📊 Statistics:")
print(f"Diameter - Raw std: {raw_d_std:.2f}cm, Filtered std: {filtered_d_std:.2f}cm")
print(f"Depth - Raw std: {raw_h_std:.2f}cm, Filtered std: {filtered_h_std:.2f}cm")
print(f"Reduction - Diameter: {(1 - filtered_d_std/raw_d_std)*100:.1f}%, Depth: {(1 - filtered_h_std/raw_h_std)*100:.1f}%")

