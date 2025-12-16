import cv2
import os
import random
import numpy as np
from pathlib import Path

def resize_and_crop(img, target_size=(400, 300)):
    """
    Resize and center crop image to target size to preserve aspect ratio.
    """
    h, w = img.shape[:2]
    target_w, target_h = target_size
    
    # Calculate scale needed
    scale = max(target_w / w, target_h / h)
    new_w = int(w * scale)
    new_h = int(h * scale)
    
    # Resize
    img_resized = cv2.resize(img, (new_w, new_h), interpolation=cv2.INTER_AREA)
    
    # Center crop
    start_x = (new_w - target_w) // 2
    start_y = (new_h - target_h) // 2
    
    cropped = img_resized[start_y:start_y+target_h, start_x:start_x+target_w]
    return cropped

def add_label(img, text, position="bottom-left"):
    """
    Add a professional looking label with background.
    """
    h, w = img.shape[:2]
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 0.7
    thickness = 2
    color = (255, 255, 255)
    bg_color = (0, 0, 0)
    
    (text_w, text_h), baseline = cv2.getTextSize(text, font, font_scale, thickness)
    
    if position == "bottom-left":
        coords = (10, h - 10)
    else:
        coords = (10, 30) # Top-left
        
    x, y = coords
    
    # Draw background rectangle
    padding = 5
    cv2.rectangle(img, 
                  (x - padding, y + baseline + padding), 
                  (x + text_w + padding, y - text_h - padding), 
                  bg_color, -1)
    
    # Draw text
    cv2.putText(img, text, coords, font, font_scale, color, thickness, cv2.LINE_AA)
    return img

def create_collage(output_path):
    # Paths
    public_dataset_path = Path(r"d:\PANGERAN\rsic\Yolov8n\datasets\segmentation\train\images")
    local_test_path = Path(r"d:\PANGERAN\rsic\Yolov8n\final-test")
    
    # Get image files
    public_images = list(public_dataset_path.glob("*.jpg")) + list(public_dataset_path.glob("*.png"))
    local_images = list(local_test_path.glob("*.jpg")) + list(local_test_path.glob("*.png")) + list(local_test_path.glob("*.jpeg"))
    
    if not public_images or not local_images:
        print("Error: Could not find images.")
        return

    # Select samples (Ensure we get some variety if possible, otherwise random)
    # Try to pick files that are likely distinct
    selected_public = random.sample(public_images, 4)
    selected_local = random.sample(local_images, 4)
    
    target_size = (400, 300) # Width, Height
    
    # Process Public Images
    row1_imgs = []
    for i, img_path in enumerate(selected_public):
        img = cv2.imread(str(img_path))
        if img is not None:
            processed = resize_and_crop(img, target_size)
            processed = add_label(processed, "Dataset Publik (Roboflow)")
            row1_imgs.append(processed)
            
    # Process Local Images
    row2_imgs = []
    for i, img_path in enumerate(selected_local):
        img = cv2.imread(str(img_path))
        if img is not None:
            processed = resize_and_crop(img, target_size)
            processed = add_label(processed, "Data Lokal (Indonesia)")
            row2_imgs.append(processed)
            
    # Ensure equal length
    min_len = min(len(row1_imgs), len(row2_imgs))
    row1_imgs = row1_imgs[:min_len]
    row2_imgs = row2_imgs[:min_len]
    
    if min_len == 0:
        print("No valid images.")
        return

    # Stack with borders
    border_size = 10
    border_color = [255, 255, 255] # White
    
    def add_border(imgs):
        bordered = []
        for img in imgs:
            img_b = cv2.copyMakeBorder(img, border_size, border_size, border_size, border_size, 
                                       cv2.BORDER_CONSTANT, value=border_color)
            bordered.append(img_b)
        return np.hstack(bordered)

    grid_row1 = add_border(row1_imgs)
    grid_row2 = add_border(row2_imgs)
    
    final_collage = np.vstack([grid_row1, grid_row2])
    
    # Save
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    cv2.imwrite(output_path, final_collage)
    print(f"Collage saved to {output_path}")

if __name__ == "__main__":
    create_collage(r"d:\PANGERAN\rsic\Yolov8n\images\dataset_collage.png")
