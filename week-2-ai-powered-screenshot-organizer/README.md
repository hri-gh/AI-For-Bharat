# 🤖 AI-Powered Screenshot Organizer

Automatically classify and organize your screenshots using AI (OCR + CLIP vision model).

**Built for**: AI for Bharat Hackathon by Hack2Skill & AWS
**Week 2 Challenge**: Lazy Automation
**Theme**: "I hate organizing screenshots, so I built this."

---

## ✨ Features

- **Smart Classification**: Uses OCR + CLIP to understand screenshot content (not just filenames!)
- **Auto-Organization**: Sorts into categories (Code, Memes, Documents, etc.)
- **Intelligent Naming**: Generates descriptive filenames based on content
- **Date Organization**: Optional folder structure by year-month
- **Two Modes**: One-time batch processing or continuous watch mode
- **Fully Customizable**: Add your own categories with simple keywords
- **Offline & Free**: No API costs, runs completely locally

---

## 📋 Default Categories

- **Code**: Programming screenshots, terminal, IDE
- **Documents**: Text documents, PDFs, articles
- **Memes**: Funny images, comics
- **Chats**: WhatsApp, Telegram, Discord screenshots
- **Design**: UI mockups, Figma, design tools
- **Diagrams**: Flowcharts, architecture diagrams
- **Receipts**: Bills, invoices, payments
- **Errors**: Error messages, exceptions, tracebacks

**All categories are customizable!** See [Configuration Guide](docs/CONFIG_EXPLAINED.md)

---

## 🚀 Quick Start

### ⭐ Recommended: Try on Google Colab First

**Why Colab?**

- ✅ Free GPU (10-50x faster than CPU)
- ✅ No installation needed
- ✅ Test before installing locally
- ✅ Works on any device

**Steps:**

1. Open the [Colab Notebook](Screenshot_Organizer_Colab.ipynb)
2. Enable GPU: Runtime → Change runtime type → GPU
3. Run the cells in order
4. Upload 5-10 test screenshots
5. See the results!

📖 **Detailed Guide**: [Google Colab Setup](docs/COLAB_GUIDE.md)

---

### Local Installation (After Testing on Colab)

⚠️ **System Requirements:**

- Python 3.8+
- 8 GB RAM minimum (16 GB recommended)
- 3 GB free disk space (for AI models)
- CPU: Any modern processor (GPU optional but 10-50x faster)

⚠️ **Performance Warning:**

- **With GPU**: 0.5-1 second per image
- **CPU only**: 2-5 seconds per image (slower but works!)
- For 100 screenshots: ~2 minutes (GPU) or ~10 minutes (CPU)

**Installation Steps:**

1. **Clone this repository:**

   ```bash
   git clone https://github.com/yourusername/screenshot-organizer.git
   cd screenshot-organizer
   ```

2. **Install dependencies** (downloads ~2-3 GB of AI models):

   ```bash
   pip install -r requirements.txt
   ```

   First run will take 5-10 minutes to download models.

3. **Run the organizer:**

   ```bash
   # Organize current folder
   python organize_screenshots.py

   # Organize specific folder
   python organize_screenshots.py --source ~/Downloads

   # Watch mode (continuous monitoring)
   python organize_screenshots.py --watch --source ~/Downloads
   ```

📖 **Detailed Guide**: [Quick Start Guide](docs/QUICK_START.md)

---

### Demo Mode (No AI Models Required)

Want to see how it works without installing AI models?

```bash
python organize_screenshots_demo.py
```

This uses simple filename pattern matching for instant testing.

## 📖 Usage Examples

### Basic Usage

```bash
# Organize screenshots in current folder
python organize_screenshots.py
```

### Custom Folders

```bash
# Specify source and destination
python organize_screenshots.py --source ~/Downloads --dest ~/Pictures/Screenshots
```

### Watch Mode

```bash
# Monitor folder and auto-organize new screenshots
python organize_screenshots.py --watch --source ~/Downloads
```

### Custom Config

```bash
# Use custom configuration file
python organize_screenshots.py --config my_config.json
```

## ⚙️ Configuration

Edit `config.json` to customize categories and behavior:

```json
{
  "source_folder": ".",
  "destination_folder": "./Organized_Screenshots",
  "categories": {
    "Code": ["code", "python", "javascript", "function"],
    "Gaming": ["game", "steam", "xbox", "score"],
    "Shopping": ["cart", "order", "price", "amazon"]
  },
  "organize_by_date": true,
  "rename_files": true,
  "move_or_copy": "move",
  "min_confidence": 0.3
}
```

### Configuration Options

- `source_folder`: Where to find screenshots
- `destination_folder`: Where to organize them
- `categories`: Your custom categories with keywords
- `organize_by_date`: Create year-month subfolders (true/false)
- `rename_files`: Generate descriptive names (true/false)
- `move_or_copy`: "move" or "copy" files
- `min_confidence`: Minimum CLIP confidence (0.0-1.0)

📖 **Detailed Guide**: [Configuration Explained](docs/CONFIG_EXPLAINED.md)

## 🎯 How It Works

### The AI Pipeline

```
Screenshot
    ↓
┌─────────────────────────────────┐
│  OCR (Extract Text)             │ → Finds keywords like "python", "error"
└─────────────────────────────────┘
    ↓
┌─────────────────────────────────┐
│  CLIP (Analyze Visuals)         │ → Understands image content
└─────────────────────────────────┘
    ↓
┌─────────────────────────────────┐
│  Smart Decision                 │ → Combines both results
└─────────────────────────────────┘
    ↓
Organized & Renamed!
```

**Example:**

```
Input: Screenshot with Python code
  ↓
OCR: "def hello_world print python"
  ↓
CLIP: "This looks like code" (95% confidence)
  ↓
Result: Organized_Screenshots/Code/2025-12/python_function_2025-12-05.png
```

---

## 💻 System Requirements

### Minimum Requirements

- Python 3.8 or higher
- 8 GB RAM
- 3 GB free disk space
- Any modern CPU

### Performance

| Environment | Speed per Image | 100 Screenshots |
|-------------|----------------|-----------------|
| Google Colab (GPU) | 0.5-1 sec | ~2 minutes |
| Local PC (CPU) | 2-5 sec | ~10 minutes |
| Local PC (GPU) | 0.5-1 sec | ~2 minutes |

**Note**: CPU-only processing is slower but perfectly functional!

## 🔧 Troubleshooting

### Models not loading?

```bash
# Reinstall dependencies
pip install --upgrade transformers torch pillow easyocr
```

### Out of memory?

- Process fewer images at once
- Close other applications
- Use Google Colab instead (free GPU!)

### Slow processing?

- Normal on CPU (2-5 sec per image)
- Use Google Colab for faster processing with free GPU
- Or use the demo version for instant testing

### Need help?

Check our documentation:

- [Quick Start Guide](docs/QUICK_START.md)
- [Configuration Guide](docs/CONFIG_EXPLAINED.md)
- [Google Colab Guide](docs/COLAB_GUIDE.md)

## 📊 Output Structure

```text
Organized_Screenshots/
├── Code/
│   ├── 2025-11/
│   │   ├── python_function_hello_2025-11-04.png
│   │   └── javascript_react_component_2025-11-13.png
│   └── 2025-12/
├── Memes/
│   └── 2025-11/
├── Documents/
│   └── 2025-11/
└── Uncategorized/
```

---

## 📚 Documentation

- **[Quick Start Guide](docs/QUICK_START.md)** - Get started in minutes
- **[Configuration Guide](docs/CONFIG_EXPLAINED.md)** - Customize categories and behavior
- **[Google Colab Guide](docs/COLAB_GUIDE.md)** - Test on Colab with free GPU

---

## 🎓 About This Project

**Built for**: AI for Bharat Hackathon by Hack2Skill & AWS
**Week 2 Challenge**: Lazy Automation
**Theme**: "I hate organizing screenshots, so I built this."

### Why This Project?

We all take tons of screenshots daily, but they pile up with generic names like `Screenshot_20251205.png`. Finding that one screenshot from last week becomes impossible. This tool uses AI to understand the actual content of screenshots and organizes them automatically.

### Key Features

- ✅ Solves real problem (screenshot clutter)
- ✅ Uses AI (OCR + CLIP vision models)
- ✅ Practical automation for daily use
- ✅ Works offline (no API costs)
- ✅ Fully customizable and extensible

### Tech Stack

- **OCR**: EasyOCR for text extraction
- **Vision AI**: OpenAI CLIP for visual understanding
- **Framework**: PyTorch + Transformers
- **Deployment**: Local PC or Google Colab

---

## 📝 License

MIT License - Feel free to use and modify!

---

## 🤝 Contributing

Suggestions and improvements welcome! Feel free to:

- Open issues for bugs or feature requests
- Submit pull requests
- Share your customizations
- Star the repo if you find it useful!

---

## 📧 Contact

Built with ❤️ for the AI for Bharat Hackathon

- **GitHub**: [Your GitHub Profile]
- **LinkedIn**: [Your LinkedIn]
- **Blog Post**: [Link to AWS Builder Center post]

---

**Happy organizing! 🚀**
