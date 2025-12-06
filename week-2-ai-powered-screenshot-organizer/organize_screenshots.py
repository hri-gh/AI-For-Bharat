#!/usr/bin/env python3
"""
AI-Powered Screenshot Organizer
Automatically classifies and organizes screenshots using OCR + CLIP
"""

import os
import sys
import json
import argparse
import shutil
from pathlib import Path
from datetime import datetime
import time

# Check if running in Colab
IS_COLAB = 'COLAB_GPU' in os.environ or 'COLAB_TPU_ADDR' in os.environ

class ScreenshotOrganizer:
    def __init__(self, config_path='config.json'):
        self.config = self.load_config(config_path)
        self.stats = {
            'total': 0,
            'processed': 0,
            'failed': 0,
            'categories': {}
        }

        # Initialize models (lazy loading)
        self.clip_model = None
        self.clip_processor = None
        self.ocr_reader = None

    def load_config(self, config_path):
        """
        Load configuration from file or use defaults

        The config file allows you to customize:
        - Categories and their keywords
        - Source/destination folders
        - File naming and organization preferences
        """
        default_config = {
            'source_folder': '.',
            'destination_folder': './Organized_Screenshots',
            'categories': {
                'Code': ['code', 'terminal', 'programming', 'script', 'console', 'editor'],
                'Documents': ['document', 'text', 'pdf', 'article', 'paper'],
                'Memes': ['meme', 'funny', 'comic', 'joke'],
                'Chats': ['chat', 'message', 'conversation', 'whatsapp', 'telegram'],
                'Design': ['design', 'ui', 'mockup', 'figma', 'sketch'],
                'Diagrams': ['diagram', 'chart', 'graph', 'flowchart', 'architecture'],
                'Receipts': ['receipt', 'bill', 'invoice', 'payment'],
                'Errors': ['error', 'exception', 'traceback', 'warning', 'failed']
            },
            'organize_by_date': True,
            'rename_files': True,
            'move_or_copy': 'move',
            'image_extensions': ['.png', '.jpg', '.jpeg', '.gif', '.bmp'],
            'min_confidence': 0.3
        }

        if os.path.exists(config_path):
            with open(config_path, 'r') as f:
                user_config = json.load(f)
                default_config.update(user_config)

        return default_config

    def initialize_models(self):
        """
        Initialize CLIP and OCR models (lazy loading)

        CLIP: Vision-language model that understands image content
        OCR: Optical Character Recognition to extract text from images

        Models are loaded only when needed (lazy loading) to save memory
        """
        print("🔄 Loading AI models...")

        try:
            # Load CLIP
            from transformers import CLIPProcessor, CLIPModel
            import torch

            print("  📦 Loading CLIP model...")
            self.clip_model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
            self.clip_processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")

            # Move to GPU if available
            self.device = "cuda" if torch.cuda.is_available() else "cpu"
            self.clip_model.to(self.device)
            print(f"  ✅ CLIP loaded on {self.device}")

        except Exception as e:
            print(f"  ⚠️  CLIP loading failed: {e}")
            print("  💡 Install with: pip install transformers torch pillow")
            self.clip_model = None

        try:
            # Load OCR
            import easyocr
            print("  📦 Loading OCR model...")
            self.ocr_reader = easyocr.Reader(['en'], gpu=torch.cuda.is_available())
            print("  ✅ OCR loaded")

        except Exception as e:
            print(f"  ⚠️  OCR loading failed: {e}")
            print("  💡 Install with: pip install easyocr")
            self.ocr_reader = None

        if not self.clip_model and not self.ocr_reader:
            print("\n❌ No AI models loaded. Please install dependencies.")
            sys.exit(1)

    def extract_text_ocr(self, image_path):
        """
        Extract text from image using OCR (Optical Character Recognition)

        This helps identify screenshots with text content like:
        - Code snippets
        - Error messages
        - Chat conversations
        - Documents
        """
        if not self.ocr_reader:
            return ""

        try:
            result = self.ocr_reader.readtext(str(image_path), detail=0)
            text = ' '.join(result).lower()
            return text
        except Exception as e:
            print(f"    ⚠️  OCR failed: {e}")
            return ""

    def classify_with_clip(self, image_path):
        """
        Classify image using CLIP (Contrastive Language-Image Pre-training)

        CLIP understands visual content and matches it with text descriptions
        Returns the best matching category and confidence score (0.0 to 1.0)
        """
        if not self.clip_model:
            return None, 0.0

        try:
            from PIL import Image
            import torch

            image = Image.open(image_path).convert('RGB')

            # Create text prompts for each category
            categories = list(self.config['categories'].keys())
            texts = [f"a screenshot of {cat.lower()}" for cat in categories]

            inputs = self.clip_processor(
                text=texts,
                images=image,
                return_tensors="pt",
                padding=True
            )

            # Move to device
            inputs = {k: v.to(self.device) for k, v in inputs.items()}

            with torch.no_grad():
                outputs = self.clip_model(**inputs)
                logits_per_image = outputs.logits_per_image
                probs = logits_per_image.softmax(dim=1)

            # Get best match
            confidence, idx = probs[0].max(0)
            category = categories[idx.item()]

            return category, confidence.item()

        except Exception as e:
            print(f"    ⚠️  CLIP failed: {e}")
            return None, 0.0

    def determine_category(self, image_path):
        """
        Determine category using OCR + CLIP (hybrid approach)

        Strategy:
        1. OCR extracts text and matches keywords from config.json
        2. CLIP analyzes visual content
        3. Combine both results for best accuracy:
           - If both agree → use that category
           - If OCR finds specific keywords → trust OCR (more precise)
           - If CLIP has high confidence → trust CLIP
           - Otherwise → mark as Uncategorized
        """
        print(f"  🔍 Analyzing: {os.path.basename(image_path)}")

        # Step 1: Extract text with OCR
        ocr_text = self.extract_text_ocr(image_path)
        ocr_category = None

        if ocr_text:
            print(f"    📝 OCR text: {ocr_text[:100]}...")
            # Match keywords from config.json categories
            for category, keywords in self.config['categories'].items():
                if any(keyword in ocr_text for keyword in keywords):
                    ocr_category = category
                    print(f"    🎯 OCR suggests: {category}")
                    break

        # Step 2: Classify with CLIP (visual analysis)
        clip_category, confidence = self.classify_with_clip(image_path)

        if clip_category:
            print(f"    🤖 CLIP suggests: {clip_category} (confidence: {confidence:.2f})")

        # Step 3: Combine results intelligently
        if ocr_category and clip_category:
            # Both models have opinions
            if ocr_category == clip_category:
                # Both agree - high confidence!
                final_category = ocr_category
            elif confidence < 0.5:
                # CLIP not confident, trust OCR keywords
                final_category = ocr_category
            else:
                # CLIP is confident, trust it
                final_category = clip_category
        elif ocr_category:
            # Only OCR found something
            final_category = ocr_category
        elif clip_category and confidence > self.config['min_confidence']:
            # Only CLIP found something with good confidence
            final_category = clip_category
        else:
            # Neither model is confident
            final_category = 'Uncategorized'

        print(f"    ✅ Final category: {final_category}")
        return final_category, ocr_text

    def generate_filename(self, original_path, category, ocr_text):
        """
        Generate descriptive filename based on content

        If rename_files is enabled in config:
        - Extracts meaningful words from OCR text
        - Adds date from file metadata
        - Creates readable filename like: python_error_traceback_2025-12-05.png

        Otherwise keeps original filename
        """
        if not self.config['rename_files']:
            return os.path.basename(original_path)

        # Extract date from original filename or use file modification time
        original_name = os.path.basename(original_path)
        file_ext = os.path.splitext(original_name)[1]

        # Get file date
        mod_time = os.path.getmtime(original_path)
        date_str = datetime.fromtimestamp(mod_time).strftime('%Y-%m-%d')

        # Generate descriptive part from OCR text
        if ocr_text:
            # Extract meaningful words (simple approach)
            words = ocr_text.split()[:5]  # First 5 words
            desc = '_'.join(w for w in words if len(w) > 3)[:30]  # Max 30 chars
            desc = ''.join(c if c.isalnum() or c == '_' else '_' for c in desc)
        else:
            desc = category.lower()

        new_name = f"{desc}_{date_str}{file_ext}"

        # Ensure unique filename
        return new_name

    def organize_file(self, image_path):
        """
        Organize a single file through the complete pipeline:
        1. Analyze and categorize
        2. Create destination folder structure
        3. Generate new filename (if enabled)
        4. Move or copy file
        5. Update statistics
        """
        try:
            self.stats['total'] += 1

            # Determine category
            category, ocr_text = self.determine_category(image_path)

            # Update stats
            self.stats['categories'][category] = self.stats['categories'].get(category, 0) + 1

            # Create destination path
            dest_base = Path(self.config['destination_folder']) / category

            if self.config['organize_by_date']:
                mod_time = os.path.getmtime(image_path)
                date_folder = datetime.fromtimestamp(mod_time).strftime('%Y-%m')
                dest_base = dest_base / date_folder

            dest_base.mkdir(parents=True, exist_ok=True)

            # Generate filename
            new_filename = self.generate_filename(image_path, category, ocr_text)
            dest_path = dest_base / new_filename

            # Handle duplicate filenames
            counter = 1
            while dest_path.exists():
                name, ext = os.path.splitext(new_filename)
                dest_path = dest_base / f"{name}_{counter}{ext}"
                counter += 1

            # Move or copy file
            if self.config['move_or_copy'] == 'move':
                shutil.move(str(image_path), str(dest_path))
                print(f"    📦 Moved to: {dest_path}")
            else:
                shutil.copy2(str(image_path), str(dest_path))
                print(f"    📦 Copied to: {dest_path}")

            self.stats['processed'] += 1

        except Exception as e:
            print(f"    ❌ Error: {e}")
            self.stats['failed'] += 1

    def find_images(self, folder):
        """Find all image files in folder"""
        images = []
        folder_path = Path(folder)

        for ext in self.config['image_extensions']:
            images.extend(folder_path.glob(f"*{ext}"))
            images.extend(folder_path.glob(f"*{ext.upper()}"))

        return images

    def organize_once(self, source_folder=None):
        """Organize all images in folder once"""
        source = source_folder or self.config['source_folder']

        print(f"\n🚀 Starting one-time organization...")
        print(f"📂 Source: {source}")
        print(f"📂 Destination: {self.config['destination_folder']}\n")

        # Initialize models
        self.initialize_models()

        # Find images
        images = self.find_images(source)

        if not images:
            print("❌ No images found!")
            return

        print(f"📸 Found {len(images)} images\n")

        # Process each image
        for i, image_path in enumerate(images, 1):
            print(f"\n[{i}/{len(images)}]")
            self.organize_file(str(image_path))

        # Print summary
        self.print_summary()

    def watch_mode(self, source_folder=None):
        """
        Watch folder and organize new images continuously

        Monitors the source folder every 5 seconds for new screenshots
        Automatically organizes them as they appear
        Press Ctrl+C to stop watching
        """
        source = source_folder or self.config['source_folder']

        print(f"\n👀 Starting watch mode...")
        print(f"📂 Watching: {source}")
        print(f"📂 Destination: {self.config['destination_folder']}")
        print("Press Ctrl+C to stop\n")

        # Initialize models
        self.initialize_models()

        # Track processed files
        processed_files = set(str(p) for p in self.find_images(source))

        try:
            while True:
                # Find current images
                current_images = set(str(p) for p in self.find_images(source))

                # Find new images
                new_images = current_images - processed_files

                if new_images:
                    print(f"\n🆕 Found {len(new_images)} new image(s)")
                    for image_path in new_images:
                        self.organize_file(image_path)
                        processed_files.add(image_path)

                # Wait before next check
                time.sleep(5)

        except KeyboardInterrupt:
            print("\n\n⏹️  Stopped watching")
            self.print_summary()

    def print_summary(self):
        """Print organization summary"""
        print("\n" + "="*50)
        print("📊 ORGANIZATION SUMMARY")
        print("="*50)
        print(f"Total images found: {self.stats['total']}")
        print(f"Successfully processed: {self.stats['processed']}")
        print(f"Failed: {self.stats['failed']}")
        print("\n📁 Categories:")
        for category, count in sorted(self.stats['categories'].items()):
            print(f"  {category}: {count}")
        print("="*50 + "\n")


def main():
    parser = argparse.ArgumentParser(
        description='AI-Powered Screenshot Organizer',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Organize current folder once
  python organize_screenshots.py

  # Organize specific folder
  python organize_screenshots.py --source ~/Downloads

  # Watch mode (continuous)
  python organize_screenshots.py --watch

  # Custom source and destination
  python organize_screenshots.py --source ~/Downloads --dest ~/Pictures/Screenshots
        """
    )

    parser.add_argument('--source', '-s',
                       help='Source folder to organize (default: current folder)')
    parser.add_argument('--dest', '-d',
                       help='Destination folder for organized screenshots')
    parser.add_argument('--watch', '-w', action='store_true',
                       help='Watch mode: continuously monitor and organize new screenshots')
    parser.add_argument('--config', '-c', default='config.json',
                       help='Path to config file (default: config.json)')

    args = parser.parse_args()

    # Create organizer
    organizer = ScreenshotOrganizer(args.config)

    # Override config with command-line args
    if args.source:
        organizer.config['source_folder'] = args.source
    if args.dest:
        organizer.config['destination_folder'] = args.dest

    # Run in appropriate mode
    if args.watch:
        organizer.watch_mode()
    else:
        organizer.organize_once()


if __name__ == '__main__':
    main()
