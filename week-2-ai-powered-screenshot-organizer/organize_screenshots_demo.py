#!/usr/bin/env python3
"""
Demo version of Screenshot Organizer - Works WITHOUT AI models
Uses simple filename pattern matching for quick testing
"""

import os
import shutil
from pathlib import Path
from datetime import datetime
import json

class DemoOrganizer:
    def __init__(self):
        self.config = {
            'source_folder': '.',
            'destination_folder': './Demo_Organized',
            'organize_by_date': True
        }
        self.stats = {'total': 0, 'categories': {}}

    def classify_by_filename(self, filename):
        """Simple classification based on filename patterns"""
        filename_lower = filename.lower()

        # Check for keywords in filename
        if any(word in filename_lower for word in ['code', 'terminal', 'python', 'javascript', 'algorithm', 'programming']):
            return 'Code'
        elif any(word in filename_lower for word in ['meme', 'funny', 'comic']):
            return 'Memes'
        elif any(word in filename_lower for word in ['chat', 'message', 'whatsapp']):
            return 'Chats'
        elif any(word in filename_lower for word in ['diagram', 'chart', 'vector', 'retriever', 'architecture']):
            return 'Diagrams'
        elif any(word in filename_lower for word in ['document', 'pdf', 'article']):
            return 'Documents'
        elif 'screenshot' in filename_lower:
            return 'General_Screenshots'
        else:
            return 'Uncategorized'

    def organize_file(self, image_path):
        """Organize a single file"""
        filename = os.path.basename(image_path)
        print(f"\n📸 Processing: {filename}")

        # Classify
        category = self.classify_by_filename(filename)
        print(f"  📁 Category: {category}")

        # Update stats
        self.stats['total'] += 1
        self.stats['categories'][category] = self.stats['categories'].get(category, 0) + 1

        # Create destination
        dest_base = Path(self.config['destination_folder']) / category

        if self.config['organize_by_date']:
            mod_time = os.path.getmtime(image_path)
            date_folder = datetime.fromtimestamp(mod_time).strftime('%Y-%m')
            dest_base = dest_base / date_folder

        dest_base.mkdir(parents=True, exist_ok=True)

        # Copy file (keeping original name for demo)
        dest_path = dest_base / filename

        # Handle duplicates
        counter = 1
        while dest_path.exists():
            name, ext = os.path.splitext(filename)
            dest_path = dest_base / f"{name}_{counter}{ext}"
            counter += 1

        shutil.copy2(image_path, dest_path)
        print(f"  ✅ Copied to: {dest_path}")

    def run(self):
        """Run demo organization"""
        print("🎬 DEMO MODE - Simple filename-based organization")
        print("="*60)
        print("This demo works WITHOUT AI models for quick testing")
        print("="*60 + "\n")

        # Find images
        image_extensions = ['.png', '.jpg', '.jpeg', '.gif', '.bmp']
        images = []
        for ext in image_extensions:
            images.extend(Path('.').glob(f"*{ext}"))
            images.extend(Path('.').glob(f"*{ext.upper()}"))

        # Filter out files in organized folders
        images = [img for img in images if 'Organized' not in str(img)]

        if not images:
            print("❌ No images found!")
            return

        print(f"📸 Found {len(images)} images\n")

        # Process each
        for image in images:
            self.organize_file(str(image))

        # Summary
        print("\n" + "="*60)
        print("📊 DEMO ORGANIZATION SUMMARY")
        print("="*60)
        print(f"Total images: {self.stats['total']}")
        print("\n📁 Categories:")
        for category, count in sorted(self.stats['categories'].items()):
            print(f"  {category}: {count}")
        print("="*60)
        print(f"\n✅ Check the '{self.config['destination_folder']}' folder!")
        print("\n💡 For AI-powered organization, install dependencies and run:")
        print("   pip install -r requirements.txt")
        print("   python organize_screenshots.py")

if __name__ == '__main__':
    organizer = DemoOrganizer()
    organizer.run()
