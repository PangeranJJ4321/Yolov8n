import os
import glob
from tqdm import tqdm

# --- KONFIGURASI ---
# Sesuaikan path ini dengan lokasi dataset kamu
dataset_path = "D:/PANGERAN/rsic/Yolov8n/datasets/segmentation"
folders = ['train/labels', 'valid/labels', 'test/labels'] # Folder yang mau dibersihkan
class_to_remove = 2  # ID untuk 'Unmarked Bump' (sesuai urutan lama: 0, 1, 2)

def clean_labels():
    print(f"🧹 Memulai pembersihan kelas {class_to_remove}...")
    removed_count = 0
    
    for folder in folders:
        search_dir = os.path.join(dataset_path, folder)
        files = glob.glob(os.path.join(search_dir, "*.txt"))
        
        print(f"📂 Mengecek folder: {folder} ({len(files)} file)")
        
        for file_path in tqdm(files):
            with open(file_path, 'r') as f:
                lines = f.readlines()
            
            new_lines = []
            file_changed = False
            
            for line in lines:
                parts = line.strip().split()
                if len(parts) > 0:
                    class_id = int(parts[0])
                    # Jika ID label bukan yang mau dihapus, simpan
                    if class_id != class_to_remove:
                        new_lines.append(line)
                    else:
                        file_changed = True
                        removed_count += 1
            
            # Jika ada yang dihapus, tulis ulang file-nya
            if file_changed:
                with open(file_path, 'w') as f:
                    f.writelines(new_lines)
                    
    print(f"\n✅ Selesai! Total {removed_count} label 'Unmarked Bump' (ID {class_to_remove}) telah dihapus.")
    print("⚠️ JANGAN LUPA: Hapus file 'labels.cache' di folder train dan valid agar YOLO membaca ulang data.")

# Jalankan fungsi
clean_labels()