<p align="right">
  English | <a href="README.md">中文</a>
</p>

# Steam Game Manifest Downloader

A command-line tool for downloading Steam game manifest files, supporting Chinese game search, automatic translation, and optimized file naming.

## Features

- 🎮 **Game Search**: Supports both Chinese and English game names
- 🔄 **Auto Translation**: Automatically translates Chinese game names to English for better search accuracy
- 📁 **Smart Naming**: Download files include game name and AppID, e.g., "Elden Ring_1423870.zip"
- 📊 **Progress Display**: Real-time download progress visualization
- 🔄 **Multi-source Download**: Supports multiple download sources with automatic failover
- 📝 **Download History**: Automatically saves download history for tracking

## Installation

### Requirements

- Python 3.10+
- Internet connection

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Usage

#### Basic Usage

```bash
# Search and download games
python main.py "Elden Ring"
```

#### Advanced Options

```bash
# Limit search results
python main.py "Genshin Impact" -n 5

# Search Chinese games
python main.py "原神"

# Specify language and country
python main.py "Game Name" -l english -c US

# Disable auto translation
python main.py "Game Name" --no-translate

# Show help
python main.py -h
```

## Project Structure

```
ManifestDownloadHelper/
├── main.py              # Entry point
├── config.py            # Configuration
├── requirements.txt     # Dependencies
├── src/                 # Source code
│   ├── __init__.py
│   ├── steam.py         # Core functionality
│   └── utils.py         # Utility functions
├── manifests/           # Downloaded manifest files
├── data/                # Data directory
│   └── history.json     # Download history
└── README.md            # Chinese documentation
└── README_EN.md         # English documentation
```

## Configuration

The `config.py` file contains the following configurable items:

- `API_SERVERS`: List of API servers
- `STEAM_SEARCH_API`: Steam search API URL
- `SECRET_KEY`: Encoding key
- `SRCS`: Number of download sources
- `DEFAULT_LANGUAGE`: Default language
- `DEFAULT_COUNTRY`: Default country

## Download History

Download history is saved in `data/history.json` and includes:
- Game name and AppID
- Download timestamp
- File path and size

## Notes

1. This tool is for educational purposes only, not for commercial use
2. Downloaded manifest files are for research purposes only
3. Please comply with Steam's Terms of Service
4. In case of network issues, the tool will automatically try other download sources

## Changelog

### v0.3.0 (2026-05-26)
- Refactored project structure with modular design
- Added download history functionality
- Optimized file naming strategy
- Improved user interface

### v0.2.0 (2026-03-09)
- Added multi-source download support
- Implemented AppID encoding
- Added progress display

### v0.1.0 (2026-03-09)
- Initial version with basic search and download functionality
