import json
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path
import os

def analyze_results(json_path: str, output_dir: str):
    json_path = Path(json_path)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    if not json_path.exists():
        print(f"❌ JSON file not found: {json_path}")
        return

    print(f"📊 Loading data from {json_path}...")
    with open(json_path, 'r') as f:
        data = json.load(f)
    
    if not data:
        print("⚠️ No data found in JSON.")
        return

    # Extract data
    frames = []
    diameters = []
    depths = []
    track_ids = []
    confidences = []
    
    # Organize by track_id for time-series analysis
    tracks = {}

    for item in data:
        # Filter unwanted data (e.g. huge depth measurement errors if any, or NaN)
        d = item.get('diameter_cm', 0)
        h = item.get('depth_cm', 0)
        tid = item.get('track_id')
        frame = item.get('frame')
        conf = item.get('confidence', 0)
        
        if d is None or h is None or np.isnan(d) or np.isnan(h):
            continue
            
        # Basic filtering (optional)
        if conf < 0.25: 
            continue

        frames.append(frame)
        diameters.append(d)
        depths.append(h)
        track_ids.append(tid)
        confidences.append(conf)

        if tid is not None:
            if tid not in tracks:
                tracks[tid] = {'frame': [], 'diameter': [], 'depth': [], 'conf': []}
            tracks[tid]['frame'].append(frame)
            tracks[tid]['diameter'].append(d)
            tracks[tid]['depth'].append(h)
            tracks[tid]['conf'].append(conf)

    print(f"✅ Loaded {len(diameters)} measurements from {len(tracks)} unique tracks.")

    # Apply style
    plt.style.use('ggplot')
    
    # 1. Distribution of Diameter (Histogram)
    plt.figure(figsize=(10, 6))
    plt.hist(diameters, bins=20, color='skyblue', edgecolor='black', alpha=0.7)
    plt.title('Distribusi Diameter Lubang Jalan Terdeteksi')
    plt.xlabel('Diameter (cm)')
    plt.ylabel('Frekuensi')
    plt.grid(True, alpha=0.3)
    plt.savefig(output_dir / 'distribusi_diameter.png', dpi=300)
    print("   Saved distribusi_diameter.png")
    
    # 2. Distribution of Depth (Histogram)
    plt.figure(figsize=(10, 6))
    plt.hist(depths, bins=20, color='salmon', edgecolor='black', alpha=0.7)
    plt.title('Distribusi Kedalaman Lubang Jalan Terdeteksi')
    plt.xlabel('Kedalaman (cm)')
    plt.ylabel('Frekuensi')
    plt.grid(True, alpha=0.3)
    plt.savefig(output_dir / 'distribusi_depth.png', dpi=300)
    print("   Saved distribusi_depth.png")

    # 3. Scatter Plot: Diameter vs Depth
    plt.figure(figsize=(10, 6))
    scatter = plt.scatter(diameters, depths, c=confidences, cmap='viridis', alpha=0.6)
    plt.colorbar(scatter, label='Confidence Score')
    plt.title('Hubungan Diameter vs Kedalaman')
    plt.xlabel('Diameter (cm)')
    plt.ylabel('Kedalaman (cm)')
    plt.grid(True, alpha=0.3)
    plt.savefig(output_dir / 'scatter_diameter_depth.png', dpi=300)
    print("   Saved scatter_diameter_depth.png")

    # 4. Time Series Analysis for Top Tracks (Longest duration)
    # Sort tracks by duration (number of frames)
    sorted_tracks = sorted(tracks.items(), key=lambda x: len(x[1]['frame']), reverse=True)
    
    top_n = min(3, len(sorted_tracks))

    if top_n > 0:
        plt.figure(figsize=(12, 6))
        for i in range(top_n):
            tid, tdata = sorted_tracks[i]
            # Plot Diameter Evolution
            plt.plot(tdata['frame'], tdata['diameter'], marker='o', markersize=4, label=f'Track ID {tid}')
        
        plt.title(f'Evolusi Estimasi Diameter untuk {top_n} Objek Terlama (Tracking Stability)')
        plt.xlabel('Frame Number')
        plt.ylabel('Diameter (cm)')
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.savefig(output_dir / 'track_stability_diameter.png', dpi=300)
        print("   Saved track_stability_diameter.png")

        # Plot Depth Evolution
        plt.figure(figsize=(12, 6))
        for i in range(top_n):
            tid, tdata = sorted_tracks[i]
            plt.plot(tdata['frame'], tdata['depth'], marker='s', markersize=4, linestyle='--', label=f'Track ID {tid}')
        
        plt.title(f'Evolusi Estimasi Kedalaman untuk {top_n} Objek Terlama')
        plt.xlabel('Frame Number')
        plt.ylabel('Kedalaman (cm)')
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.savefig(output_dir / 'track_stability_depth.png', dpi=300)
        print("   Saved track_stability_depth.png")

if __name__ == "__main__":
    # Adjust paths    # Configuration
    JSON_FILE = "output/final_test_results/video4_measurements.json"
    OUTPUT_DIR = "output/final_analysis_plots"
    
    analyze_results(JSON_FILE, OUTPUT_DIR)
