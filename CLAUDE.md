# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Steam game manifest downloader tool that fetches game manifests from Steam's API using multiple proxy servers. The tool supports Chinese game search with automatic English translation, intelligent file naming, and download history tracking.

## Key Architecture

### Core Components

1. **SteamManifestDownloader** (src/steam.py)
   - Main class handling the complete workflow
   - Integrates search, selection, and download functionality
   - Manages multiple API servers with automatic failover
   - Handles AppID encoding for API requests

2. **Utility Functions** (src/utils.py)
   - AppID encoding/decoding with custom algorithm
   - File name sanitization and generation
   - History management (JSON-based)
   - Directory management

3. **Configuration** (config.py)
   - Centralized configuration for API servers
   - Download timeouts and retry settings
   - Default language and country settings
   - Path configurations for outputs

### Data Flow

1. User inputs game name via command line
2. Tool searches Steam API (with auto-translation for Chinese)
3. User selects from search results
4. Tool downloads manifest using encoded AppID
5. File saved as "GameName_AppID.zip"
6. Download record added to history

## Development Commands

### Running the Tool

```bash
# Basic usage
python main.py "游戏名称"

# With options
python main.py "游戏名称" -n 5 --no-translate

# Show help
python main.py -h
```

### Testing

```bash
# Test imports and basic functionality
python -c "from src.steam import SteamManifestDownloader; print('OK')"

# Test configuration
python -c "from config import API_SERVERS; print(f'Servers: {len(API_SERVERS)}')"
```

## Important Implementation Details

### AppID Encoding
The AppID is encoded using a custom algorithm in `utils.py`:
- Uses a shuffled digit table generated from SECRET_KEY
- Adds length prefix and checksum for validation
- Required for API requests to proxy servers

### File Naming Strategy
- Format: `{GameName}_{AppID}.zip`
- Special characters replaced with underscores
- Duplicate files not overwritten (check before download)

### Multi-Source Download
- Tries up to MAX_RETRIES (default: 6) different sources
- Random server selection from API_SERVERS list
- Progress bar with tqdm for each attempt

### History Tracking
- JSON format in `data/history.json`
- Stores: game info, timestamp, file path, size
- Last 100 records retained automatically

## Configuration Notes

- API_SERVERS: List of proxy URLs (change if some are blocked)
- SECRET_KEY: Used for AppID encoding (from SteamTools project)
- DEFAULT_LANGUAGE: "schinese" for Chinese, "english" for English
- DOWNLOAD_TIMEOUT: 15 seconds per request
- MAX_RETRIES: 6 download attempts per game

## Legacy Files

The original flat files (`get_appid.py`, `download_manifest.py`) are preserved for reference but the new modular structure in `src/` should be used for all development.