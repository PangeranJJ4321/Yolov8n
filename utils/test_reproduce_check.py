import numpy as np
import sys
import os

# We assume we are running from the root directory d:\PANGERAN\rsic\Yolov8n
from src.pothole_detection_system import PotholeDetectionSystem

def test_z_base_logic():
    print("🧪 Testing z_base calculation logic...")
    
    class MockSystem(PotholeDetectionSystem):
        def __init__(self):
            pass 
            
    system = MockSystem()
    
    # Scenario: 
    # Depth map represents DISTANCE (meters).
    # Foreground noise (0.8m), Surface (5.0m), Pothole (5.2m).
    
    np.random.seed(42)
    n_points = 1000
    
    road = np.random.normal(5.0, 0.05, int(n_points * 0.8))
    pothole = np.random.normal(5.2, 0.05, int(n_points * 0.15))
    noise = np.random.normal(0.8, 0.05, int(n_points * 0.05))
    
    roi_depth = np.concatenate([road, pothole, noise])
    
    print(f"Stats:")
    print(f"  Min: {roi_depth.min():.4f}")
    print(f"  Mean: {roi_depth.mean():.4f}")
    print(f"  10th percentile (old bug): {np.percentile(roi_depth, 10):.4f}")
    print(f"  90th percentile (new fix): {np.percentile(roi_depth, 90):.4f}")
    
    # Run the actual method
    z_base = system._calculate_z_base(roi_depth)
    print(f"\nCalculated z_base: {z_base:.4f}")
    
    if z_base < 2.0:
        print("\n❌ FAILURE: z_base picked up foreground noise/closest point!")
        sys.exit(1)
    elif z_base > 5.1:
        print("\n✅ SUCCESS: z_base picked up the deeper point!")
        sys.exit(0)
    else:
        print(f"\n⚠️  UNCERTAIN: z_base = {z_base}")
        sys.exit(1)

if __name__ == "__main__":
    test_z_base_logic()
