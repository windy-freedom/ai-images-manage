# AI Images Management System

An intelligent image management system powered by Google's Gemini AI that automatically renames and organizes your images based on their content.

## 🌟 Features

### Core Capabilities
- **AI-Powered Analysis**: Uses Google Gemini API to analyze image content
- **Smart Renaming**: Generates descriptive filenames based on image content
- **Intelligent Classification**: Automatically categorizes images into appropriate folders
- **Multiple Processing Modes**: Choose between classification-only, rename+classify, or legacy modes
- **Batch Processing**: Handle multiple images at once
- **Conflict Resolution**: Automatically handles filename and folder conflicts

### Processing Modes
1. **`rename-classify`** (Default): AI renames files with descriptive names AND intelligently categorizes them
2. **`classify-only`**: Smart categorization without renaming files
3. **`classify`** (Legacy): Uses predefined categories for classification

## 🚀 Quick Start

### 1. Installation
```bash
# Clone the repository
git clone https://github.com/windy-freedom/ai-images-manage.git
cd ai-images-manage

# Install dependencies
pip install -r requirements.txt
```

### 2. Configuration
```bash
# Copy the example config file
cp config.example.json config.json

# Edit config.json and add your Gemini API key
# Get your API key from: https://makersuite.google.com/app/apikey
```

### 3. Usage
```bash
# Default mode: Rename + Smart Classification
python demo_classification.py

# Classification only (keep original filenames)
python demo_classification.py --mode classify-only

# Legacy classification mode
python demo_classification.py --mode classify

# Process images in a different directory
python demo_classification.py --directory /path/to/images
```

## 📖 Detailed Usage

### Command Line Options
```bash
python demo_classification.py [OPTIONS]

Options:
  --mode {classify,rename-classify,classify-only}
                        Processing mode (default: rename-classify)
  --directory DIRECTORY
                        Directory containing images (default: pics)
  -h, --help           Show help message
```

### Example Workflows

#### Smart Rename + Classification (Default)
```bash
python demo_classification.py --mode rename-classify
```
- **Input**: `IMG_20240115_143022.jpg`
- **AI Analysis**: Detects a grey tabby cat
- **Output**: `cats/grey_tabby_cat.jpg`

#### Classification Only
```bash
python demo_classification.py --mode classify-only
```
- **Input**: `vacation_photo.jpg`
- **AI Analysis**: Detects beach landscape
- **Output**: `nature/vacation_photo.jpg`

## 🎯 How It Works

1. **Image Analysis**: The system uses Google's Gemini AI to analyze each image
2. **Content Understanding**: AI identifies main subjects, scenes, and context
3. **Smart Naming**: Generates descriptive, meaningful filenames (if rename mode is enabled)
4. **Intelligent Categorization**: Creates appropriate folder categories based on content
5. **Organization**: Moves images to their categorized folders with proper naming

## 📁 Example Results

### Before Processing
```
pics/
├── IMG_001.jpg (cat photo)
├── DSC_002.jpg (dog photo)
├── photo_123.jpg (food photo)
└── image_456.jpg (landscape)
```

### After Processing (rename-classify mode)
```
pics/
├── cats/
│   └── orange_tabby_sleeping.jpg
├── dogs/
│   └── golden_retriever_park.jpg
├── food/
│   └── chocolate_cake_birthday.jpg
└── nature/
    └── mountain_sunset_landscape.jpg
```

## 🔧 Configuration

### config.json
```json
{
  "gemini_api_key": "YOUR_GEMINI_API_KEY_HERE",
  "default_directory": "pics",
  "supported_formats": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp"]
}
```

### Environment Variables
Alternatively, you can set your API key as an environment variable:
```bash
export GEMINI_API_KEY='your-api-key-here'
```

## 📋 Requirements

- Python 3.7+
- Google Generative AI library
- Pillow (PIL)
- Internet connection for AI analysis

### Dependencies
```
google-generativeai>=0.3.0
Pillow>=9.0.0
```

## 🛠️ Advanced Features

### Legacy Image Renamer Integration
The system also includes the original `image_renamer.py` with traditional classification:

```bash
# Traditional renaming only
python image_renamer.py --mode rename

# Traditional classification
python image_renamer.py --mode classify

# Traditional rename + classify
python image_renamer.py --mode both
```

### Supported Image Formats
- JPEG (.jpg, .jpeg)
- PNG (.png)
- GIF (.gif)
- BMP (.bmp)
- WebP (.webp)

## 🔒 Privacy & Security

- Images are analyzed using Google's Gemini API
- No images are stored on external servers permanently
- API key should be kept secure and not shared
- Consider using environment variables for API keys in production

## 🐛 Troubleshooting

### Common Issues

1. **API Key Error**
   ```
   Error: Please provide Gemini API key
   ```
   - Solution: Set up your API key in `config.json` or environment variable

2. **No Images Found**
   ```
   No image files found in pics directory to classify
   ```
   - Solution: Ensure images are in the correct directory and have supported formats

3. **Network Issues**
   - Solution: Check internet connection for AI analysis

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is open source. Please check the license file for details.

## 🙏 Acknowledgments

- Google Gemini AI for powerful image analysis
- Python community for excellent libraries
- Contributors and users for feedback and improvements

---

**Made with ❤️ for better image organization**
