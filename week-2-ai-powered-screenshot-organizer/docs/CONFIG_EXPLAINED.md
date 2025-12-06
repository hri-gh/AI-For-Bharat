# 📝 Config.json Explained

The `config.json` file controls how the Screenshot Organizer works. Here's what each setting does:

## 🎯 How Categories Work

```json
"categories": {
  "Code": ["code", "terminal", "programming", "script", ...],
  "Documents": ["document", "text", "pdf", ...],
  ...
}
```

### How it works:
1. **OCR extracts text** from your screenshot
2. **Searches for keywords** in the extracted text
3. **Matches to category** if any keyword is found

### Example:
```
Screenshot contains text: "def hello_world(): print('Hello')"
                          ↓
OCR extracts: "def hello world print hello"
                          ↓
Finds keyword: "def" (in Code category)
                          ↓
Result: Categorized as "Code"
```

## ✏️ How to Add Your Own Categories

### Example 1: Add "Gaming" Category
```json
"categories": {
  "Code": ["code", "terminal", "programming"],
  "Gaming": ["game", "steam", "xbox", "playstation", "score", "level"],
  "Documents": ["document", "text", "pdf"]
}
```

### Example 2: Add "Shopping" Category
```json
"categories": {
  "Shopping": ["cart", "checkout", "order", "price", "buy", "amazon", "flipkart"],
  "Receipts": ["receipt", "bill", "invoice"]
}
```

### Example 3: Add "Social Media" Category
```json
"categories": {
  "Social_Media": ["twitter", "facebook", "instagram", "linkedin", "post", "tweet", "like", "share"]
}
```

## 📋 Complete Config Options

```json
{
  // Where to find screenshots
  "source_folder": ".",

  // Where to organize them
  "destination_folder": "./Organized_Screenshots",

  // Your custom categories with keywords
  "categories": {
    "CategoryName": ["keyword1", "keyword2", "keyword3"]
  },

  // Create year-month subfolders? (true/false)
  "organize_by_date": true,

  // Generate descriptive filenames? (true/false)
  "rename_files": true,

  // "move" files or "copy" them?
  "move_or_copy": "move",

  // Which file types to process
  "image_extensions": [".png", ".jpg", ".jpeg", ".gif", ".bmp"],

  // Minimum CLIP confidence (0.0 to 1.0)
  // Lower = more lenient, Higher = more strict
  "min_confidence": 0.3
}
```

## 🎨 Customization Examples

### For Students:
```json
"categories": {
  "Assignments": ["assignment", "homework", "due", "submit"],
  "Lectures": ["lecture", "slide", "professor", "notes"],
  "Code": ["python", "java", "code", "programming"],
  "Research": ["paper", "research", "study", "journal"]
}
```

### For Developers:
```json
"categories": {
  "Code": ["code", "function", "class", "import", "def", "const"],
  "Errors": ["error", "exception", "traceback", "failed", "bug"],
  "Documentation": ["docs", "readme", "api", "documentation"],
  "Design": ["figma", "ui", "mockup", "design", "prototype"],
  "Terminal": ["terminal", "bash", "command", "shell", "npm"]
}
```

### For Content Creators:
```json
"categories": {
  "YouTube": ["youtube", "video", "subscribe", "views"],
  "Instagram": ["instagram", "post", "story", "reel"],
  "Analytics": ["analytics", "views", "engagement", "stats"],
  "Ideas": ["idea", "concept", "brainstorm", "draft"]
}
```

## 🔧 Tips for Keywords

### Good Keywords:
- ✅ Specific and unique: "traceback", "exception"
- ✅ Common terms: "error", "code", "chat"
- ✅ Brand names: "whatsapp", "figma", "github"
- ✅ Technical terms: "function", "import", "class"

### Avoid:
- ❌ Too generic: "the", "and", "is"
- ❌ Too rare: very specific words that rarely appear
- ❌ Overlapping: same keyword in multiple categories

## 🎯 Testing Your Keywords

After adding new categories:

1. **Test with a few images first**:
   ```bash
   python organize_screenshots.py
   ```

2. **Check the output** - does it categorize correctly?

3. **Adjust keywords** if needed:
   - Add more keywords if screenshots are missed
   - Remove keywords if wrong categorization

4. **Iterate** until you're happy!

## 📊 Folder Structure Examples

### With `organize_by_date: true`:
```
Organized_Screenshots/
├── Code/
│   ├── 2025-11/
│   └── 2025-12/
├── Memes/
│   └── 2025-12/
```

### With `organize_by_date: false`:
```
Organized_Screenshots/
├── Code/
├── Memes/
└── Documents/
```

## 💡 Pro Tips

1. **Start simple**: Begin with 3-5 categories
2. **Add gradually**: Add more as you see patterns
3. **Use lowercase**: Keywords are case-insensitive
4. **Be specific**: More specific keywords = better accuracy
5. **Test often**: Run on small batches to verify

## 🔄 Reloading Config

The script reads config.json every time you run it, so:
- Edit config.json
- Save it
- Run the script again
- No restart needed!

---

**Need help?** Check the examples above or experiment with your own categories!
