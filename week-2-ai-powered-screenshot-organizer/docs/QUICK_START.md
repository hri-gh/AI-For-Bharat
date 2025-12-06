# 🚀 Quick Start Guide

## Option 1: Test on Google Colab (RECOMMENDED FIRST)

### Why Colab First?
- ✅ Free GPU (10-50x faster)
- ✅ No installation on your PC
- ✅ Test before committing
- ✅ See if it works for your needs

### Steps:
1. **Open Google Colab**: https://colab.research.google.com/

2. **Upload the notebook**:
   - Click "File" → "Upload notebook"
   - Upload `Screenshot_Organizer_Colab.ipynb`

3. **Enable GPU** (Important!):
   - Click "Runtime" → "Change runtime type"
   - Select "GPU" → Save

4. **Follow the notebook cells**:
   - Run each cell in order
   - Upload the script files when prompted
   - Upload 5-10 test screenshots
   - Watch the magic happen! ✨

5. **Check results**:
   - See how screenshots are organized
   - Download the organized folder
   - Check processing speed

### Expected Performance on Colab:
- With GPU: ~0.5-1 second per image
- 10 images: ~10-15 seconds total
- 100 images: ~1-2 minutes total

---

## Option 2: Run on Your PC (After Colab Test)

### Your System (i3 7th Gen + 8GB RAM):
- ✅ Will work fine!
- ⏱️ Slower than Colab (2-5 sec per image)
- 💾 Uses ~2-3 GB RAM while running

### Installation:

1. **Install Python 3.8+** (if not installed)
   ```bash
   python3 --version
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

   This downloads ~2-3 GB of AI models (one-time, takes 5-10 minutes)

3. **Test with sample images**:
   ```bash
   python organize_screenshots.py
   ```

4. **Organize your Downloads folder**:
   ```bash
   python organize_screenshots.py --source ~/Downloads --dest ~/Pictures/Organized
   ```

### Expected Performance on Your PC:
- CPU only: ~2-5 seconds per image
- 10 images: ~30-60 seconds
- 100 images: ~5-10 minutes
- **Totally acceptable for batch processing!**

---

## Quick Demo (No AI Models)

Want to see how it works WITHOUT installing AI models?

```bash
python organize_screenshots_demo.py
```

This uses simple filename matching (no AI) for instant testing.

---

## Comparison

| Feature | Google Colab | Your PC |
|---------|-------------|---------|
| Speed | ⚡ Very Fast (GPU) | 🐢 Slower (CPU) |
| Setup | 🎯 Easy | 📦 Requires install |
| Cost | 💰 Free | 💰 Free |
| Access to files | ☁️ Upload needed | 💻 Direct access |
| Best for | Testing, demos | Daily use |

---

## My Recommendation

### For the Hackathon:
1. **Test on Colab first** (5 minutes)
2. **If it works well**, install on your PC
3. **Demo both** in your presentation:
   - "Works on cloud with GPU"
   - "Also works locally on any PC"
4. **Show flexibility** = bonus points!

### For Daily Use:
- **Colab**: Quick one-time cleanups
- **Your PC**: Automated daily organization with watch mode

---

## Troubleshooting

### Colab Issues:
- **"No GPU"**: Runtime → Change runtime type → GPU
- **"Session expired"**: Colab sessions last ~12 hours, just restart
- **"Out of memory"**: Process fewer images at once

### PC Issues:
- **"Out of memory"**: Close other apps, or use Colab
- **"Too slow"**: Normal on CPU, be patient or use Colab
- **"Models not downloading"**: Check internet connection

---

## What to Do Now?

1. ✅ **Upload to Colab** - Test with your 10 sample images
2. ✅ **See the results** - Check if categorization is good
3. ✅ **Decide** - Install on PC or keep using Colab?
4. ✅ **Customize** - Edit `config.json` for your needs

---

**Ready to test on Colab? Upload the notebook and let's go! 🚀**
