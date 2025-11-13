"""
Depth Estimation Module menggunakan DepthAnything V2
Class-based implementation untuk estimasi kedalaman per-frame

Author: Skripsi Project
Date: 2025
"""

import cv2
import numpy as np
import json
import torch
from pathlib import Path
from typing import Tuple, Optional, Union
import warnings
warnings.filterwarnings('ignore')


class DepthEstimator:
    """
    Class untuk estimasi kedalaman menggunakan DepthAnything V2
    
    Fitur:
    - Load kalibrasi kamera dari JSON
    - Depth estimation menggunakan DepthAnything V2
    - Scale recovery untuk konversi ke metrik absolut
    - Visualisasi depth map
    - Processing per-frame (image/video)
    """
    
    def __init__(self,
                 model_type: str = "small",
                 camera_params: Optional[dict] = None,
                 camera_height: float = 1.5,
                 device: Optional[str] = None,
                 calib_path: Optional[Union[str, Path]] = None):
        """
        Initialize Depth Estimator
        
        Args:
            model_type: Tipe model ('small', 'base', 'large')
                       - small: Cepat, akurasi sedang
                       - base: Seimbang
                       - large: Lambat, akurasi tinggi
            camera_params: Dictionary dari load_camera_calibration() atau None
            camera_height: Tinggi kamera dari permukaan jalan (meter)
            device: 'cuda' atau 'cpu' (auto-detect jika None)
            calib_path: Path ke file kalibrasi JSON (alternatif dari camera_params)
        """
        self.model_type = model_type
        self.camera_height = camera_height
        self.device = device or ('cuda' if torch.cuda.is_available() else 'cpu')
        
        # Load kalibrasi jika path diberikan
        if calib_path is not None:
            self.camera_params = self.load_camera_calibration(calib_path)
        else:
            self.camera_params = camera_params
        
        # Extract camera parameters
        if self.camera_params:
            self.camera_matrix = self.camera_params['camera_matrix']
            self.dist_coeffs = self.camera_params['dist_coeffs']
        else:
            self.camera_matrix = None
            self.dist_coeffs = None
        
        # Initialize model (lazy loading)
        self.model = None
        self._model_loaded = False
        self._using_dummy = False  # Flag untuk dummy depth mode
        
        print(f"✅ DepthEstimator initialized")
        print(f"   Model type: {model_type}")
        print(f"   Device: {self.device}")
        print(f"   Camera calibration: {'✅ Loaded' if self.camera_params else '❌ Not available'}")
        print(f"   Camera height: {camera_height} m")
    
    @staticmethod
    def load_camera_calibration(calib_path: Union[str, Path]) -> dict:
        """
        Load parameter kalibrasi kamera dari file JSON (Static method)
        
        Args:
            calib_path: Path ke file kalibrasi JSON
            
        Returns:
            Dictionary berisi camera_matrix, dist_coeffs, dan metadata lainnya
        """
        calib_path = Path(calib_path)
        
        if not calib_path.exists():
            raise FileNotFoundError(f"File kalibrasi tidak ditemukan: {calib_path}")
        
        with open(calib_path, 'r') as f:
            calib_data = json.load(f)
        
        # Convert ke numpy array
        camera_matrix = np.array(calib_data['camera_matrix'])
        dist_coeffs = np.array(calib_data['distortion_coefficients'])
        
        print(f"✅ Kalibrasi loaded dari: {calib_path}")
        print(f"   Camera matrix shape: {camera_matrix.shape}")
        print(f"   Distortion coeffs shape: {dist_coeffs.shape}")
        print(f"   Focal length: fx={camera_matrix[0,0]:.2f}, fy={camera_matrix[1,1]:.2f}")
        print(f"   Principal point: cx={camera_matrix[0,2]:.2f}, cy={camera_matrix[1,2]:.2f}")
        
        return {
            'camera_matrix': camera_matrix,
            'dist_coeffs': dist_coeffs,
            'image_size': calib_data.get('image_size', None),
            'reprojection_error': calib_data.get('reprojection_error', None),
            **calib_data  # Include all other metadata
        }
    
    def _load_model(self):
        """Load DepthAnything V2 model (internal method)"""
        if self._model_loaded:
            return
        
        print(f"🖥️  Loading DepthAnything V2 ({self.model_type})...")
        print(f"   Using device: {self.device}")
        
        # Try multiple import methods
        model = None
        
        # Method 1: Try official depth-anything-v2 package
        try:
            from depth_anything_v2.dpt import DepthAnythingV2
            model = DepthAnythingV2(device=self.device, ckpt_path=None, model_type=self.model_type)
            model.eval()
            print(f"✅ DepthAnything V2 ({self.model_type}) loaded via depth-anything-v2 package")
            self.model = model
            self._model_loaded = True
            return
        except ImportError:
            pass
        except Exception as e:
            print(f"⚠️  Error dengan depth-anything-v2 package: {e}")
        
        # Method 2: Try direct import from cloned repo
        try:
            import sys
            # Assume repo cloned to depth-anything-v2 folder
            repo_path = Path("../depth-anything-v2")
            if repo_path.exists():
                sys.path.insert(0, str(repo_path))
                from depth_anything_v2.dpt import DepthAnythingV2
                model = DepthAnythingV2(device=self.device, ckpt_path=None, model_type=self.model_type)
                model.eval()
                print(f"✅ DepthAnything V2 ({self.model_type}) loaded from local repo")
                self.model = model
                self._model_loaded = True
                self._using_dummy = False
                return
        except Exception as e:
            print(f"⚠️  Error dengan local repo: {e}")
        
        # Method 3: Fallback
        if model is None:
            print("❌ DepthAnything V2 tidak dapat di-load")
            print("\n💡 Instruksi instalasi:")
            print("   1. Clone repo: git clone https://github.com/DepthAnything/Depth-Anything-V2.git")
            print("   2. Install: cd Depth-Anything-V2 && pip install -e .")
            print("   3. Atau install package: pip install depth-anything-v2")
            print("\n⚠️  [WARNING] Using dummy depth map for fallback mode.")
            self.model = None
            self._model_loaded = False
            self._using_dummy = True
    
    def undistort_image(self, image: np.ndarray) -> np.ndarray:
        """
        Koreksi distorsi gambar menggunakan parameter kalibrasi
        
        Args:
            image: Input image (BGR format)
            
        Returns:
            Undistorted image
        """
        if self.camera_matrix is None or self.dist_coeffs is None:
            return image.copy()
        
        h, w = image.shape[:2]
        
        # Get optimal new camera matrix
        new_camera_matrix, roi = cv2.getOptimalNewCameraMatrix(
            self.camera_matrix, self.dist_coeffs, (w, h), 1, (w, h)
        )
        
        # Undistort
        undistorted = cv2.undistort(
            image, self.camera_matrix, self.dist_coeffs, None, new_camera_matrix
        )
        
        return undistorted
    
    def estimate_depth(self, image: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """
        Estimasi depth map dari single frame
        
        Args:
            image: Input image (BGR format)
            
        Returns:
            Tuple (depth_map, processed_image)
            - depth_map: Depth map relatif (numpy array, same size as image)
            - processed_image: Image yang sudah diundistort (jika kalibrasi tersedia)
        """
        # Load model jika belum
        if not self._model_loaded:
            self._load_model()
        
        # Undistort jika kalibrasi tersedia
        processed_image = self.undistort_image(image)
        
        # Convert BGR to RGB untuk DepthAnything V2
        rgb_image = cv2.cvtColor(processed_image, cv2.COLOR_BGR2RGB)
        h, w = processed_image.shape[:2]
        
        # Estimate depth
        try:
            if self.model is None:
                # Dummy depth map jika model tidak tersedia
                y_coords = np.arange(h).reshape(-1, 1)
                dummy_depth = (y_coords / h).astype(np.float32)  # Depth increases downward
                print("⚠️  Using dummy depth map (model not loaded)")
                return dummy_depth, processed_image
            
            # DepthAnything V2 expects RGB image
            # Try different API methods
            if hasattr(self.model, 'infer_image'):
                depth_map = self.model.infer_image(rgb_image)
            elif hasattr(self.model, 'predict'):
                depth_map = self.model.predict(rgb_image)
            elif hasattr(self.model, '__call__'):
                # Direct call
                with torch.no_grad():
                    # Preprocess image
                    from torchvision import transforms
                    transform = transforms.Compose([
                        transforms.ToPILImage(),
                        transforms.Resize((518, 518)),  # DepthAnything V2 input size
                        transforms.ToTensor(),
                        transforms.Normalize(mean=[0.485, 0.456, 0.406], 
                                           std=[0.229, 0.224, 0.225])
                    ])
                    img_tensor = transform(rgb_image).unsqueeze(0)
                    if hasattr(self.model, 'device'):
                        img_tensor = img_tensor.to(self.model.device)
                    else:
                        img_tensor = img_tensor.to(self.device)
                    
                    depth_map = self.model(img_tensor)
                    # Post-process
                    depth_map = depth_map.squeeze().cpu().numpy()
                    depth_map = cv2.resize(depth_map, (w, h))
            else:
                raise AttributeError("Model tidak memiliki method infer_image, predict, atau __call__")
            
            # JANGAN normalisasi otomatis! Biarkan scale recovery yang menangani konversi relatif → absolut
            # Normalisasi otomatis akan menghancurkan skala absolut jika model sudah menghasilkan nilai dalam meter
            # if depth_map.max() > 1.0:
            #     depth_map = depth_map / depth_map.max()  # Normalize to 0-1
            
            # Ensure same size as input
            if depth_map.shape[:2] != (h, w):
                depth_map = cv2.resize(depth_map, (w, h))
            
            return depth_map, processed_image
            
        except Exception as e:
            print(f"❌ Error dalam depth estimation: {e}")
            print(f"   Error details: {type(e).__name__}")
            # Fallback: return dummy depth map
            y_coords = np.arange(h).reshape(-1, 1)
            dummy_depth = (y_coords / h).astype(np.float32)
            return dummy_depth, processed_image
    
    def scale_recovery(self,
                      depth_map: np.ndarray,
                      road_roi: Optional[Tuple[int, int, int, int]] = None,
                      pitch_angle: float = 0.0) -> Tuple[np.ndarray, float]:
        """
        Scale recovery menggunakan tinggi kamera sebagai referensi
        
        Args:
            depth_map: Depth map relatif dari DepthAnything V2
            road_roi: Optional ROI untuk area jalan (x, y, w, h)
            pitch_angle: Sudut pitch kamera dalam derajat (default: 0 = horizontal)
            
        Returns:
            Tuple (absolute_depth_map, scale_factor)
        """
        if self.camera_matrix is None:
            print("⚠️  Camera matrix tidak tersedia, menggunakan depth relatif")
            return depth_map, 1.0
        
        # Identifikasi area jalan untuk estimasi scale
        h, w = depth_map.shape
        
        if road_roi is not None:
            x, y, roi_w, roi_h = road_roi
            road_region = depth_map[y:y+roi_h, x:x+roi_w]
        else:
            # Default: ambil bagian bawah tengah gambar (area jalan)
            road_region = depth_map[int(h*0.6):int(h*0.9), int(w*0.3):int(w*0.7)]
        
        # Hitung median depth relatif untuk area jalan
        road_depth_rel = np.median(road_region[road_region > 0])
        
        if road_depth_rel <= 0:
            print("⚠️  Warning: Tidak dapat menemukan area jalan yang valid")
            road_depth_rel = np.median(depth_map[depth_map > 0])
        
        # Hitung depth absolut untuk area jalan
        pitch_rad = np.radians(pitch_angle)
        if abs(pitch_angle) < 1.0:  # Jika pitch sangat kecil, gunakan aproksimasi cos
            # Pendekatan lebih realistis: road_depth = camera_height / cos(pitch)
            # Untuk pitch kecil, cos ≈ 1, tapi lebih akurat secara fisika
            road_depth_abs = self.camera_height / np.cos(pitch_rad)
        else:
            # Untuk pitch besar, gunakan sin (jika kamera miring ke bawah)
            road_depth_abs = self.camera_height / np.sin(pitch_rad)
        
        # Hitung scale factor
        scale_factor = road_depth_abs / road_depth_rel
        
        # Konversi seluruh depth map ke absolut
        absolute_depth = depth_map * scale_factor
        
        print(f"📏 Scale recovery:")
        print(f"   Road depth (relative): {road_depth_rel:.4f}")
        print(f"   Road depth (absolute): {road_depth_abs:.2f} m")
        print(f"   Scale factor: {scale_factor:.4f}")
        
        return absolute_depth, scale_factor
    
    def visualize_depth(self,
                       depth_map: np.ndarray,
                       colormap: str = 'jet',
                       min_depth: Optional[float] = None,
                       max_depth: Optional[float] = None) -> np.ndarray:
        """
        Visualisasi depth map dengan colormap
        
        Args:
            depth_map: Depth map (bisa relatif atau absolut)
            colormap: Colormap untuk visualisasi ('jet', 'viridis', 'plasma', dll)
            min_depth: Minimum depth untuk normalization (None = auto)
            max_depth: Maximum depth untuk normalization (None = auto)
            
        Returns:
            Colored depth visualization (BGR format untuk OpenCV)
        """
        # Normalize depth map
        if min_depth is None:
            min_depth = depth_map[depth_map > 0].min() if (depth_map > 0).any() else depth_map.min()
        if max_depth is None:
            max_depth = depth_map.max()
        
        # Normalize to 0-255
        depth_normalized = ((depth_map - min_depth) / (max_depth - min_depth + 1e-8) * 255).astype(np.uint8)
        
        # Apply colormap
        if colormap == 'jet':
            depth_colored = cv2.applyColorMap(depth_normalized, cv2.COLORMAP_JET)
        elif colormap == 'viridis':
            depth_colored = cv2.applyColorMap(depth_normalized, cv2.COLORMAP_VIRIDIS)
        elif colormap == 'plasma':
            depth_colored = cv2.applyColorMap(depth_normalized, cv2.COLORMAP_PLASMA)
        else:
            depth_colored = cv2.applyColorMap(depth_normalized, cv2.COLORMAP_JET)
        
        return depth_colored
    
    def create_depth_overlay(self,
                            image: np.ndarray,
                            depth_colored: np.ndarray,
                            alpha: float = 0.5) -> np.ndarray:
        """
        Overlay depth visualization di atas image original
        
        Args:
            image: Original image (BGR)
            depth_colored: Colored depth map (BGR)
            alpha: Transparency factor (0-1)
            
        Returns:
            Overlayed image
        """
        overlay = cv2.addWeighted(image, 1-alpha, depth_colored, alpha, 0)
        return overlay
    
    def process_frame(self,
                     image_path: Union[str, Path],
                     save_output: bool = True,
                     output_dir: Union[str, Path] = "output") -> dict:
        """
        Pipeline lengkap: Load image -> Undistort -> Depth Estimation -> Scale Recovery -> Visualize
        
        Args:
            image_path: Path ke input image
            save_output: Apakah menyimpan hasil visualisasi
            output_dir: Directory untuk menyimpan output
            
        Returns:
            Dictionary berisi semua hasil processing
        """
        # Load image
        image_path = Path(image_path)
        if not image_path.exists():
            raise FileNotFoundError(f"Image tidak ditemukan: {image_path}")
        
        image = cv2.imread(str(image_path))
        if image is None:
            raise ValueError(f"Gagal load image: {image_path}")
        
        print(f"\n🖼️  Processing: {image_path.name}")
        print(f"   Image size: {image.shape[1]}x{image.shape[0]}")
        
        # Step 1: Depth estimation
        print("📊 Estimating depth...")
        depth_map_rel, image_undistorted = self.estimate_depth(image)
        
        # Step 2: Scale recovery (jika kalibrasi tersedia)
        if self.camera_params is not None:
            print("📏 Recovering scale...")
            depth_map_abs, scale_factor = self.scale_recovery(depth_map_rel)
        else:
            print("⚠️  Kalibrasi tidak tersedia, menggunakan depth relatif")
            depth_map_abs = depth_map_rel
            scale_factor = 1.0
        
        # Step 3: Visualisasi
        print("🎨 Creating visualizations...")
        depth_colored = self.visualize_depth(depth_map_abs, colormap='jet')
        depth_overlay = self.create_depth_overlay(image_undistorted, depth_colored, alpha=0.5)
        
        # Step 4: Save output
        if save_output:
            output_dir = Path(output_dir)
            output_dir.mkdir(exist_ok=True)
            
            stem = image_path.stem
            cv2.imwrite(str(output_dir / f"{stem}_original.jpg"), image)
            cv2.imwrite(str(output_dir / f"{stem}_undistorted.jpg"), image_undistorted)
            cv2.imwrite(str(output_dir / f"{stem}_depth.jpg"), depth_colored)
            cv2.imwrite(str(output_dir / f"{stem}_overlay.jpg"), depth_overlay)
            
            # Save depth map as numpy array
            np.save(str(output_dir / f"{stem}_depth_map.npy"), depth_map_abs)
            
            print(f"💾 Output saved ke: {output_dir}")
        
        results = {
            'original_image': image,
            'undistorted_image': image_undistorted,
            'depth_map_relative': depth_map_rel,
            'depth_map_absolute': depth_map_abs,
            'scale_factor': scale_factor,
            'depth_colored': depth_colored,
            'depth_overlay': depth_overlay,
            'camera_params': self.camera_params
        }
        
        print("✅ Processing selesai!")
        return results
    
    def process_video(self,
                     video_path: Union[str, Path],
                     output_path: Optional[Union[str, Path]] = None,
                     show_preview: bool = False,
                     frame_skip: int = 1) -> None:
        """
        Process video frame-by-frame dengan depth estimation
        
        Args:
            video_path: Path ke input video
            output_path: Path untuk output video (None = auto-generate)
            show_preview: Tampilkan preview saat processing
            frame_skip: Process setiap N frame (1 = semua frame)
        """
        video_path = Path(video_path)
        if not video_path.exists():
            raise FileNotFoundError(f"Video tidak ditemukan: {video_path}")
        
        # Open video
        cap = cv2.VideoCapture(str(video_path))
        if not cap.isOpened():
            raise ValueError(f"Gagal membuka video: {video_path}")
        
        # Get video properties
        fps = int(cap.get(cv2.CAP_PROP_FPS))
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        
        print(f"\n🎬 Processing video: {video_path.name}")
        print(f"   Resolution: {width}x{height}")
        print(f"   FPS: {fps}")
        print(f"   Total frames: {total_frames}")
        print(f"   Frame skip: {frame_skip}")
        
        # Setup output video
        if output_path is None:
            output_path = video_path.parent / f"{video_path.stem}_depth_output.avi"
        else:
            output_path = Path(output_path)
        
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        out = cv2.VideoWriter(str(output_path), fourcc, fps, (width, height))
        
        frame_count = 0
        processed_count = 0
        
        print("\n🔄 Processing frames...")
        try:
            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                
                # Skip frames jika diperlukan
                if frame_count % frame_skip != 0:
                    frame_count += 1
                    continue
                
                # Process frame
                depth_map_rel, frame_undistorted = self.estimate_depth(frame)
                
                # Scale recovery
                if self.camera_params is not None:
                    depth_map_abs, _ = self.scale_recovery(depth_map_rel)
                else:
                    depth_map_abs = depth_map_rel
                
                # Visualisasi
                depth_colored = self.visualize_depth(depth_map_abs, colormap='jet')
                output_frame = self.create_depth_overlay(frame_undistorted, depth_colored, alpha=0.5)
                
                # Write frame
                out.write(output_frame)
                processed_count += 1
                
                # Show preview
                if show_preview:
                    cv2.imshow('Depth Estimation', output_frame)
                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        print("⏹️  Stopped by user")
                        break
                
                # Progress
                if processed_count % 10 == 0:
                    progress = (frame_count / total_frames) * 100
                    print(f"   Progress: {processed_count} frames processed ({progress:.1f}%)")
                
                frame_count += 1
                
        except KeyboardInterrupt:
            print("\n⏹️  Interrupted by user")
        finally:
            cap.release()
            out.release()
            if show_preview:
                cv2.destroyAllWindows()
        
        print(f"\n✅ Video processing selesai!")
        print(f"   Processed: {processed_count} frames")
        print(f"   Output: {output_path}")

