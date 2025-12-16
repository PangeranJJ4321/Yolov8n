import json
import numpy as np
import os

def analyze_json(json_path):
    with open(json_path, 'r') as f:
        data = json.load(f)
    
    tracks = {}
    for item in data:
        track_id = item.get('track_id')
        if track_id is None:
            continue
            
        if track_id not in tracks:
            tracks[track_id] = {'diameters': [], 'depths': [], 'confs': []}
            
        tracks[track_id]['diameters'].append(item['diameter_cm'])
        tracks[track_id]['depths'].append(item['depth_cm'])
        tracks[track_id]['confs'].append(item['confidence'])
    
    print("System Measurement Summary:")
    print(f"{'ID':<5} | {'Count':<5} | {'Conf':<5} | {'Diam (cm)':<10} | {'Depth (cm)':<10}")
    print("-" * 50)
    
    summary = []
    
    for tid, vals in tracks.items():
        count = len(vals['diameters'])
        mean_conf = np.mean(vals['confs'])
        mean_diam = np.mean(vals['diameters'])
        std_diam = np.std(vals['diameters'])
        
        # Robust depth estimation (median or percentile)
        # Using 90th percentile to be consistent with our "deepest point" logic, 
        # or maybe median of the sequence is better for stability?
        # Let's use Median for the "Final Estimate" of the pothole.
        mean_depth = np.median(vals['depths']) 
        max_depth = np.max(vals['depths'])
        
        print(f"{tid:<5} | {count:<5} | {mean_conf:.2f}  | {mean_diam:.1f} +/-{std_diam:.1f} | {mean_depth:.1f} (Max: {max_depth:.1f})")
        
        summary.append({
            'id': tid,
            'diam': mean_diam,
            'depth': mean_depth
        })
        
    return summary

if __name__ == "__main__":
    analyze_json(r"d:\PANGERAN\rsic\Yolov8n\output\final_test_results\video3_measurements.json")
