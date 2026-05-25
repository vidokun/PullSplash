<p align="center">
  <img src="branding/icon-droplet.svg" alt="PullSplash" width="96" height="96">
</p>

<h1 align="center">PullSplash</h1>
<p align="center"><strong>Pull photos from Unsplash.</strong> A native desktop bulk downloader.</p>

<p align="center">
  <a href="https://github.com/vidokun/PullSplash/releases"><img src="https://img.shields.io/github/v/release/vidokun/PullSplash?color=e44232&label=latest" alt="Release"></a>
  <a href="https://pullsplash.com"><img src="https://img.shields.io/badge/website-pullsplash.com-e44232" alt="Website"></a>
  <img src="https://img.shields.io/badge/platform-macOS%20%7C%20Windows-lightgrey" alt="Platform">
  <img src="https://img.shields.io/badge/license-MIT-blue" alt="License">
</p>

---

## Features

- **Keyword & Collection search** — search by any keyword or paste an Unsplash collection URL
- **Bulk download** — select multiple photos, download them all in one click
- **Image processing** — resize, convert format (JPG / PNG / WebP), adjust quality
- **Native desktop app** — no browser needed, runs as a standalone `.app` window
- **Dark theme** — designed for low-light environments with custom dark scrollbar
- **Auto-update** — checks GitHub Releases on startup, notifies when a new version is available
- **Single-click save** — downloads go straight to `~/Downloads/PullSplash/`

## Download

[**Download the latest release →**](https://github.com/vidokun/PullSplash/releases)

| Platform | Format |
|----------|--------|
| macOS | `PullSplash.app` (Apple Silicon / Intel) |
| Windows | `PullSplash.exe` (coming soon) |

> macOS users: right-click → **Open** on first launch (app is not notarized).

## How to Use

1. Get a free **Unsplash API key** at [unsplash.com/developers](https://unsplash.com/developers)
2. Paste your key into the sidebar and click **Save**
3. Type a keyword (or paste a collection URL) and hit **Search**
4. Click photos to select them, click **View** for a fullscreen preview
5. Choose format, quality, and resize options in the sidebar
6. Click **Download** — files appear in `~/Downloads/PullSplash/`

## Screenshots

<!-- Replace with actual screenshots -->
<p align="center">
  <em>Screenshots coming soon</em>
</p>

## Build from Source

```bash
# Clone
git clone https://github.com/vidokun/PullSplash.git
cd PullSplash

# Install dependencies
pip install -r requirements.txt

# Run in development
python launcher.py

# Build standalone app
python -m PyInstaller packaging/pullsplash.spec
```

## Tech Stack

- **Backend:** Python · FastAPI · Uvicorn · Pillow
- **Frontend:** HTML · Tailwind CSS · vanilla JavaScript
- **Desktop:** PyWebView (native macOS/Windows webview)
- **Packaging:** PyInstaller

## Credits

Built by [Vidokun](https://github.com/vidokun). Powered by the [Unsplash API](https://unsplash.com/developers).

---

<p align="center">
  <a href="https://pullsplash.com">pullsplash.com</a> · 
  <a href="https://github.com/vidokun/PullSplash/releases">Releases</a> · 
  <a href="https://github.com/vidokun/PullSplash/issues">Issues</a>
</p>
