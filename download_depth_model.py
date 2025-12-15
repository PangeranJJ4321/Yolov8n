import torch
import os
from pathlib import Path

def download_model():
    url = "https://huggingface.co/depth-anything/Depth-Anything-V2-Small/resolve/main/depth_anything_v2_vits.pth"
    save_path = Path("weights/depth_anything_v2_vits.pth")
    
    save_path.parent.mkdir(parents=True, exist_ok=True)
    
    if save_path.exists():
        print(f"✅ Model sudah ada di: {save_path}")
        return

    print(f"⬇️ Downloading model from {url}...")
    try:
        torch.hub.download_url_to_file(url, str(save_path))
        print(f"✅ Download selesai: {save_path}")
    except Exception as e:
        print(f"❌ Gagal download: {e}")

if __name__ == "__main__":
    download_model()
