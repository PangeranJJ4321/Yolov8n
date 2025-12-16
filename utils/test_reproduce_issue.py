import numpy as np
import sys
import os

# Add current directory to path so we can import the class
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from pothole_detection_system import PotholeDetectionSystem

def test_z_base_logic():
    print("🧪 Testing z_base calculation logic...")
    
    # Create a mock PotholeDetectionSystem (we only need the static/helper methods basically)
    # We can't easily instantiate the whole thing without models, so we'll just subclass or monkeypatch if needed.
    # Actually, _calculate_z_base is an instance method but doesn't use 'self' except potentially for logging?
    # Checking code... it is an instance method but doesn't use self! 
    # Wait, it is: def _calculate_z_base(self, roi_depth: np.ndarray) -> float:
    # It does not use self inside the method (based on my previous view_file).
    
    # Let's verify that assumption.
    # Line 212: def _calculate_z_base(self, roi_depth: np.ndarray) -> float:
    # Line 222-250: No usage of self.
    
    # So we can just create a dummy instance or invoke it unbound if we are careful, 
    # but easier to just mock the class or instantiate with dummy paths.
    
    class MockSystem(PotholeDetectionSystem):
        def __init__(self):
            pass # Skip initialization
            
    system = MockSystem()
    
    # Scenario: 
    # Depth map represents DISTANCE (meters).
    # Camera is at 1.5m height.
    # Road surface is around 5.0m distance.
    # Pothole bottom is deeper, say 5.2m distance.
    # Foreground noise (car hood) is very close, say 0.8m distance.
    
    # Create a synthetic ROI depth array
    # 80% road surface (5.0m +/- 0.05 noise)
    # 15% pothole bottom (5.2m +/- 0.05 noise)
    # 5% foreground noise (0.8m)
    
    np.random.seed(42)
    n_points = 1000
    
    road = np.random.normal(5.0, 0.05, int(n_points * 0.8))
    pothole = np.random.normal(5.2, 0.05, int(n_points * 0.15))
    noise = np.random.normal(0.8, 0.05, int(n_points * 0.05))
    
    roi_depth = np.concatenate([road, pothole, noise])
    
    print(f"Stats:")
    print(f"  Min: {roi_depth.min():.4f}")
    print(f"  Max: {roi_depth.max():.4f}")
    print(f"  Mean: {roi_depth.mean():.4f}")
    print(f"  10th percentile (currently used): {np.percentile(roi_depth, 10):.4f}")
    print(f"  90th percentile (proposed fix): {np.percentile(roi_depth, 90):.4f}")
    
    # Run the actual method
    z_base = system._calculate_z_base(roi_depth)
    print(f"\nCalculated z_base: {z_base:.4f}")
    
    # Expectation: z_base should be around 5.2m (pothole depth), NOT 0.8m (noise) or 5.0m (surface)
    # But strictly speaking, z_base should be the "deepest" valid part.
    
    if z_base < 2.0:
        print("\n❌ FAILURE: z_base picked up foreground noise/closest point!")
    elif z_base > 5.1:
        print("\n✅ SUCCESS: z_base picked up the deeper point!")
    else:
        print("\n⚠️  UNCERTAIN: z_base picked up road surface?")

if __name__ == "__main__":
    test_z_base_logic()
