#!/usr/bin/env python3
"""
Quick test script to verify setup without loading AI models
"""

import os
import sys
from pathlib import Path

def test_setup():
    print("🧪 Testing Screenshot Organizer Setup\n")
    print("="*50)

    # Check Python version
    print(f"✅ Python version: {sys.version.split()[0]}")

    # Check required files
    required_files = ['organize_screenshots.py', 'config.json', 'requirements.txt']
    for file in required_files:
        if os.path.exists(file):
            print(f"✅ Found: {file}")
        else:
            print(f"❌ Missing: {file}")

    # Check for sample images
    print("\n📸 Sample Images:")
    image_extensions = ['.png', '.jpg', '.jpeg', '.gif', '.bmp']
    images = []
    for ext in image_extensions:
        images.extend(Path('.').glob(f"*{ext}"))
        images.extend(Path('.').glob(f"*{ext.upper()}"))

    print(f"Found {len(images)} images:")
    for img in images:
        size_mb = os.path.getsize(img) / (1024 * 1024)
        print(f"  - {img.name} ({size_mb:.2f} MB)")

    # Check dependencies
    print("\n📦 Checking Dependencies:")
    dependencies = {
        'torch': 'PyTorch',
        'transformers': 'Transformers (CLIP)',
        'PIL': 'Pillow (Image processing)',
        'easyocr': 'EasyOCR'
    }

    for module, name in dependencies.items():
        try:
            __import__(module)
            print(f"✅ {name} installed")
        except ImportError:
            print(f"❌ {name} NOT installed")

    print("\n" + "="*50)
    print("\n💡 Next Steps:")
    print("1. Install dependencies: pip install -r requirements.txt")
    print("2. Run organizer: python organize_screenshots.py")
    print("3. Or watch mode: python organize_screenshots.py --watch")
    print("\n⚠️  First run will download ~2-3 GB of AI models")
    print("="*50)

if __name__ == '__main__':
    test_setup()
