# AI-Powered Screenshot Organizer - Project Context

## Project Overview

This is an AI-powered screenshot organizer built for the AI for Bharat Hackathon (Week 2: Lazy Automation). The tool automatically classifies and organizes screenshots using OCR and CLIP vision models.

## Key Technologies

- **OCR**: EasyOCR for text extraction from screenshots
- **Vision AI**: OpenAI CLIP (via Transformers) for visual content understanding
- **Framework**: PyTorch for model inference
- **Deployment**: Supports both local PC and Google Colab

## Architecture

### Hybrid AI Approach
The system combines two AI models for best accuracy:
1. **OCR (EasyOCR)**: Extracts text from screenshots and matches keywords
2. **CLIP**: Analyzes visual content and classifies images
3. **Smart Decision**: Combines both results intelligently

### File Structure
- `organize_screenshots.py`: Main script with full AI capabilities
- `organize_screenshots_demo.py`: Demo version without AI (filename-based)
- `config.json`: User-configurable categories and settings
- `docs/`: Comprehensive documentation

## Development Guidelines

### Code Style
- Use clear, descriptive variable names
- Add docstrings to all functions explaining purpose and approach
- Include error handling with helpful user messages
- Prefer readability over cleverness

### AI Model Handling
- Use lazy loading for models (load only when needed)
- Auto-detect GPU availability
- Provide fallback options if models fail to load
- Show clear progress indicators during processing

### Configuration
- All categories are user-configurable via `config.json`
- Keywords should be lowercase for case-insensitive matching
- Support both one-time and watch mode operations
- Allow command-line arguments to override config

### Performance Considerations
- CPU processing: 2-5 seconds per image (acceptable)
- GPU processing: 0.5-1 second per image (optimal)
- Batch processing for efficiency
- Memory-efficient model loading

## User Experience Principles

1. **Clear Feedback**: Show what's happening at each step
2. **Helpful Errors**: If something fails, explain why and how to fix it
3. **Flexible Deployment**: Support both cloud (Colab) and local usage
4. **Easy Customization**: Simple config file for categories
5. **No Surprises**: Warn about system requirements and processing time

## Testing Approach

- Test with diverse screenshot types (code, memes, documents, etc.)
- Verify both OCR and CLIP work independently and together
- Test on both CPU and GPU environments
- Validate config customization works correctly

## Documentation Standards

- README: Quick start with Colab-first approach
- QUICK_START: Detailed getting started guide
- CONFIG_EXPLAINED: How to customize categories
- COLAB_GUIDE: Google Colab setup instructions

## Hackathon Context

**Theme**: "I hate organizing screenshots, so I built this."

**Key Points**:
- Solves real, relatable problem
- Uses AI intelligently (hybrid approach)
- Practical and actually useful
- Works offline (no API costs)
- Fully customizable

**Target Audience**:
- Developers (code screenshots)
- Students (lecture notes, assignments)
- Content creators (social media, analytics)
- Anyone with screenshot clutter

## Future Enhancement Ideas

- Duplicate detection
- Content-based search
- Web UI
- Mobile app integration
- Cloud sync
- Batch editing interface
