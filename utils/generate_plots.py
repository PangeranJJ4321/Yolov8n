import pandas as pd
import matplotlib.pyplot as plt
import os

# Paths
csv_path = r"d:\PANGERAN\rsic\Yolov8n\runs\segment\yolov8m-seg-custom\results.csv"
output_dir = r"d:\PANGERAN\rsic\Yolov8n\dokumentasi_untuk_paper\images"
output_path = os.path.join(output_dir, "training_loss_custom.png")

# Ensure output dir exists
os.makedirs(output_dir, exist_ok=True)

# Read Data
try:
    df = pd.read_csv(csv_path)
    # Strip whitespace from column names just in case
    df.columns = [c.strip() for c in df.columns]
    
    # Plotting
    # Use a clean style
    try:
        plt.style.use('seaborn-v0_8-whitegrid')
    except:
        plt.style.use('ggplot') # Fallback if seaborn style not available

    fig, ax = plt.subplots(1, 3, figsize=(18, 5))

    # Common settings
    epochs = df['epoch']

    # 1. Box Loss
    ax[0].plot(epochs, df['train/box_loss'], label='Pelatihan (Train)', color='#1f77b4', linewidth=2)
    ax[0].plot(epochs, df['val/box_loss'], label='Validasi (Val)', color='#ff7f0e', linestyle='--', linewidth=2)
    ax[0].set_title('Box Loss (Regresi Kotak)', fontsize=12, fontweight='bold')
    ax[0].set_xlabel('Epoch', fontsize=10)
    ax[0].set_ylabel('Loss', fontsize=10)
    ax[0].legend()
    ax[0].grid(True, linestyle=':', alpha=0.6)

    # 2. Segmentation Loss
    ax[1].plot(epochs, df['train/seg_loss'], label='Pelatihan (Train)', color='#1f77b4', linewidth=2)
    ax[1].plot(epochs, df['val/seg_loss'], label='Validasi (Val)', color='#ff7f0e', linestyle='--', linewidth=2)
    ax[1].set_title('Segmentation Loss (Segmentasi)', fontsize=12, fontweight='bold')
    ax[1].set_xlabel('Epoch', fontsize=10)
    ax[1].legend()
    ax[1].grid(True, linestyle=':', alpha=0.6)

    # 3. Classification Loss
    ax[2].plot(epochs, df['train/cls_loss'], label='Pelatihan (Train)', color='#1f77b4', linewidth=2)
    ax[2].plot(epochs, df['val/cls_loss'], label='Validasi (Val)', color='#ff7f0e', linestyle='--', linewidth=2)
    ax[2].set_title('Classification Loss (Klasifikasi)', fontsize=12, fontweight='bold')
    ax[2].set_xlabel('Epoch', fontsize=10)
    ax[2].legend()
    ax[2].grid(True, linestyle=':', alpha=0.6)

    plt.suptitle('Dinamika Penurunan Loss Selama Pelatihan YOLOv8m-seg', fontsize=16, y=1.05)
    plt.tight_layout()
    
    # Save
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"Graph successfully saved to: {output_path}")

except Exception as e:
    print(f"Error generating plot: {e}")
