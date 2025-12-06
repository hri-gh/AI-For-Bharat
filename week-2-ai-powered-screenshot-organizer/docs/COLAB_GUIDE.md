# 🚀 Google Colab Setup Guide

Quick guide to test the Screenshot Organizer on Google Colab.

## 🎯 Recommended: Use the Jupyter Notebook

**Easiest way**: Upload `Screenshot_Organizer_Colab.ipynb` to Colab and follow the cells!

1. Go to: https://colab.research.google.com/
2. Click "File" → "Upload notebook"
3. Upload `Screenshot_Organizer_Colab.ipynb`
4. Enable GPU: Runtime → Change runtime type → GPU
5. Run each cell in order

---

## Alternative: Manual Setup (Step by Step)

If you prefer to set up manually without the notebook:

### Step 1: Open Google Colab

Go to: https://colab.research.google.com/

Create a new notebook.

### Step 2: Enable GPU (Important!)

- Click "Runtime" → "Change runtime type"
- Select "GPU" → Save
- This makes processing 10-50x faster!

### Step 3: Install Dependencies

```python
# This takes 2-3 minutes, downloads ~2-3 GB
!pip install -q transformers torch pillow easyocr
print("✅ Dependencies installed!")
```

### Step 4: Upload Script Files

```python
from google.colab import files

print("📤 Upload organize_screenshots.py and config.json")
uploaded = files.upload()

# Verify
if 'organize_screenshots.py' in uploaded and 'config.json' in uploaded:
    print("✅ Files uploaded successfully!")
```

### Step 5: Upload Test Images

```python
print("📸 Upload your test screenshots")
test_images = files.upload()
print(f"✅ Uploaded {len(test_images)} images")
```

**Or mount Google Drive:**
```python
from google.colab import drive
drive.mount('/content/drive')
```

### Step 6: Check GPU

```python
import torch
if torch.cuda.is_available():
    print(f"✅ GPU: {torch.cuda.get_device_name(0)}")
else:
    print("⚠️ No GPU - enable it in Runtime settings")
```

### Step 7: Run the Organizer

```python
# Organize uploaded images
!python organize_screenshots.py
```

**Or with custom paths:**
```python
# If using Google Drive
!python organize_screenshots.py --source /content/drive/MyDrive/Screenshots
```

### Step 8: View Results

```python
# See the organized structure
!tree Organized_Screenshots/ -L 3

# Or simple list
!ls -la Organized_Screenshots/
```

### Step 9: Download Results

```python
# Zip and download
!zip -r organized_screenshots.zip Organized_Screenshots/
files.download('organized_screenshots.zip')
```

## Tips

- **Free GPU**: Runtime → Change runtime type → GPU
- **Faster processing**: GPU makes it 10-50x faster
- **Session timeout**: Colab sessions expire after ~12 hours
- **Storage**: Free tier has limited storage

## Troubleshooting

### "No module named 'transformers'"
Run the install cell again:
```python
!pip install transformers torch pillow easyocr
```

### "CUDA out of memory"
Switch to CPU or process fewer images:
```python
# Force CPU usage
import os
os.environ['CUDA_VISIBLE_DEVICES'] = ''
```

### Models downloading slowly
First run downloads ~2GB of models. Be patient!

---

**Pro Tip**: Develop and test on Colab (free GPU), then deploy on your local PC!
