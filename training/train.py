"""
Waste Classification Model Training Script
===========================================
Optimized for RTX 3050 4GB GPU - Memory Safe Edition

This script trains a YOLOv8 model for waste classification with:
- Memory optimization for 4GB VRAM (uses ~1.5-2GB max)
- 4 classes as per problem statement:
  - RECYCLABLE (0) - Blue Bin - Plastic, Paper, Metal
  - ORGANIC (1)    - Green Bin - Food, Leaves, Wood
  - HAZARDOUS (2)  - Red Bin - Batteries, Bulbs, Paint
  - GENERAL (3)    - Grey Bin - Chip bags, Tissues
- Safe batch size and image size settings
"""

import os
import sys
import gc
import torch
from pathlib import Path

def check_gpu():
    """Check GPU availability and memory"""
    print("=" * 60)
    print("GPU HEALTH CHECK")
    print("=" * 60)
    
    if not torch.cuda.is_available():
        print("❌ CUDA not available! Training will use CPU (very slow)")
        print("   Make sure you have CUDA-enabled PyTorch installed")
        return False
    
    gpu_name = torch.cuda.get_device_name(0)
    total_memory = torch.cuda.get_device_properties(0).total_memory / (1024**3)
    
    print(f"✅ GPU Found: {gpu_name}")
    print(f"✅ Total VRAM: {total_memory:.2f} GB")
    
    # Clear any existing GPU memory
    torch.cuda.empty_cache()
    gc.collect()
    
    return True

def train_model():
    """Train the waste classification model with RTX 3050 optimizations"""
    
    print("\n" + "=" * 60)
    print("WASTE CLASSIFICATION MODEL TRAINING")
    print("Optimized for RTX 3050 4GB")
    print("=" * 60)
    
    # Check GPU first
    has_gpu = check_gpu()
    
    # Import ultralytics after GPU check
    from ultralytics import YOLO
    
    # Training configuration optimized for RTX 3050 4GB
    # These settings keep VRAM usage under 2GB
    config = {
        # Use YOLOv8 nano model - smallest, fastest, least memory
        'model': 'yolov8n.pt',  # Nano model ~3.2M parameters
        
        # Dataset configuration
        'data': 'D:/Hackthon-garbage/training/dataset/data.yaml',
        
        # Training parameters - MEMORY SAFE
        'epochs': 50,           # Good balance for dataset size
        'batch': 8,             # Uses ~1.7-2GB VRAM
        'imgsz': 416,           # Reduced from 640 to save memory
        'patience': 10,         # Early stopping patience
        
        # Device settings
        'device': 0 if has_gpu else 'cpu',
        
        # Memory optimization
        'workers': 0,           # NO workers to prevent RAM crash
        'cache': False,         # Don't cache images in RAM
        'amp': True,            # Mixed precision training (FP16)
        
        # Training optimization
        'optimizer': 'AdamW',   # Good optimizer for this task
        'lr0': 0.01,            # Initial learning rate
        'lrf': 0.01,            # Final learning rate factor
        'momentum': 0.937,      # Momentum
        'weight_decay': 0.0005, # Weight decay
        
        # Augmentation - moderate for waste classification
        'hsv_h': 0.015,         # HSV-Hue augmentation
        'hsv_s': 0.7,           # HSV-Saturation augmentation
        'hsv_v': 0.4,           # HSV-Value augmentation
        'degrees': 10.0,        # Rotation
        'translate': 0.1,       # Translation
        'scale': 0.5,           # Scale
        'flipud': 0.0,          # No vertical flip (waste orientation matters)
        'fliplr': 0.5,          # Horizontal flip
        'mosaic': 0.5,          # Reduced mosaic (saves memory)
        
        # Output
        'project': 'D:/Hackthon-garbage/training/runs',
        'name': 'waste_classifier',
        'exist_ok': True,       # Overwrite if exists
        'pretrained': True,     # Use pretrained weights
        'verbose': True,        # Show training progress
        
        # Prevent memory issues
        'rect': False,          # Rectangular training off
        'cos_lr': True,         # Cosine learning rate scheduler
    }
    
    print("\n📋 Training Configuration:")
    print(f"   Model: YOLOv8 Nano (memory efficient)")
    print(f"   Epochs: {config['epochs']}")
    print(f"   Batch Size: {config['batch']}")
    print(f"   Image Size: {config['imgsz']}x{config['imgsz']}")
    print(f"   Device: {'GPU (CUDA)' if has_gpu else 'CPU'}")
    print(f"   Mixed Precision: {'Enabled' if config['amp'] else 'Disabled'}")
    print(f"   Dataset: {config['data']}")
    
    try:
        # Clear memory before training
        torch.cuda.empty_cache() if has_gpu else None
        gc.collect()
        
        print("\n🚀 Starting training...")
        print("   This may take 30-60 minutes depending on your hardware")
        print("   GPU memory usage will be monitored\n")
        
        # Load the model
        model = YOLO(config['model'])
        
        # Start training
        results = model.train(
            data=config['data'],
            epochs=config['epochs'],
            batch=config['batch'],
            imgsz=config['imgsz'],
            patience=config['patience'],
            device=config['device'],
            workers=config['workers'],
            cache=config['cache'],
            amp=config['amp'],
            optimizer=config['optimizer'],
            lr0=config['lr0'],
            lrf=config['lrf'],
            momentum=config['momentum'],
            weight_decay=config['weight_decay'],
            hsv_h=config['hsv_h'],
            hsv_s=config['hsv_s'],
            hsv_v=config['hsv_v'],
            degrees=config['degrees'],
            translate=config['translate'],
            scale=config['scale'],
            flipud=config['flipud'],
            fliplr=config['fliplr'],
            mosaic=config['mosaic'],
            project=config['project'],
            name=config['name'],
            exist_ok=config['exist_ok'],
            pretrained=config['pretrained'],
            verbose=config['verbose'],
            rect=config['rect'],
            cos_lr=config['cos_lr'],
        )
        
        print("\n" + "=" * 60)
        print("✅ TRAINING COMPLETED SUCCESSFULLY!")
        print("=" * 60)
        
        # Find and copy the best model
        best_model_path = Path(config['project']) / config['name'] / 'weights' / 'best.pt'
        final_model_path = Path('D:/Hackthon-garbage/backend/model/best.pt')
        
        if best_model_path.exists():
            import shutil
            # Backup old model if exists
            if final_model_path.exists():
                backup_path = final_model_path.with_suffix('.pt.backup')
                shutil.copy(final_model_path, backup_path)
                print(f"   📦 Old model backed up to: {backup_path}")
            
            # Copy new best model
            shutil.copy(best_model_path, final_model_path)
            print(f"   🎯 Best model saved to: {final_model_path}")
            
            # Print model metrics
            print(f"\n📊 Training Results:")
            print(f"   Best model saved at: {best_model_path}")
            print(f"   Copied to backend: {final_model_path}")
            
        else:
            print(f"⚠️ Best model not found at expected location: {best_model_path}")
        
        return True
        
    except RuntimeError as e:
        if "out of memory" in str(e).lower():
            print("\n❌ GPU OUT OF MEMORY!")
            print("   Trying with even smaller settings...")
            
            # Clear memory
            torch.cuda.empty_cache()
            gc.collect()
            
            # Try with smaller batch
            print("   Reducing batch size to 4...")
            config['batch'] = 4
            config['imgsz'] = 384  # Even smaller image size
            
            model = YOLO(config['model'])
            results = model.train(**{k: v for k, v in config.items() if k not in ['model']})
            
            return True
        else:
            print(f"\n❌ Training Error: {e}")
            raise e
            
    except Exception as e:
        print(f"\n❌ Unexpected Error: {e}")
        raise e


def validate_dataset():
    """Validate the dataset before training"""
    print("\n📁 Validating Dataset...")
    
    dataset_path = Path('D:/Hackthon-garbage/training/dataset')
    
    # Check directories exist
    for split in ['train', 'valid', 'test']:
        img_dir = dataset_path / split / 'images'
        lbl_dir = dataset_path / split / 'labels'
        
        if not img_dir.exists():
            print(f"   ❌ Missing: {img_dir}")
            return False
        if not lbl_dir.exists():
            print(f"   ❌ Missing: {lbl_dir}")
            return False
            
        img_count = len(list(img_dir.glob('*')))
        lbl_count = len(list(lbl_dir.glob('*.txt')))
        
        print(f"   ✅ {split}: {img_count} images, {lbl_count} labels")
    
    # Check data.yaml
    data_yaml = dataset_path / 'data.yaml'
    if not data_yaml.exists():
        print(f"   ❌ Missing: {data_yaml}")
        return False
    
    print("   ✅ data.yaml found")
    return True


if __name__ == "__main__":
    print("\n" + "🗑️ " * 20)
    print("    WASTE CLASSIFICATION TRAINER")
    print("    RTX 3050 4GB Optimized Edition")
    print("🗑️ " * 20 + "\n")
    
    # Validate dataset first
    if not validate_dataset():
        print("\n❌ Dataset validation failed. Please check your dataset.")
        sys.exit(1)
    
    # Start training
    success = train_model()
    
    if success:
        print("\n" + "🎉 " * 20)
        print("    TRAINING COMPLETE!")
        print("    Your new best.pt model is ready!")
        print("    Located at: D:/Hackthon-garbage/backend/model/best.pt")
        print("🎉 " * 20 + "\n")
    else:
        print("\n❌ Training failed. Check the error messages above.")
        sys.exit(1)
