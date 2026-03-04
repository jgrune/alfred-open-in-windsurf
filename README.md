# Open in Windsurf — Alfred Workflow

An Alfred workflow that lets you quickly open files and folders in [Windsurf](https://codeium.com/windsurf), the AI-powered IDE by Codeium.

## Features

Trigger with the keyword `surf`:

- **Empty query** — shows your 20 most recently opened files/folders in Windsurf
- **Path starting with `/` or `~`** — autocompletes filesystem paths
- **Any other query** — searches via Spotlight (scoped to your home directory)

Press `Enter` to open the selected item in Windsurf.

## Requirements

- [Alfred](https://www.alfredapp.com/) with the [Powerpack](https://www.alfredapp.com/powerpack/) (required for workflows)
- [Windsurf](https://codeium.com/windsurf) installed at `/Applications/Windsurf.app`
- Python 3 (pre-installed on macOS)

## Installation

### Option A: Download the pre-built workflow

1. Download `Open in Windsurf.alfredworkflow` from the [Releases](https://github.com/jgrune/alfred-open-in-windsurf/releases) page.
2. Double-click the `.alfredworkflow` file — Alfred will import it automatically.

### Option B: Build from source

1. Clone this repository:
   ```bash
   git clone https://github.com/jgrune/alfred-open-in-windsurf.git
   cd alfred-open-in-windsurf
   ```
2. Run the build script:
   ```bash
   ./build.sh
   ```
   This packages `info.plist` and `recent.py` into `Open in Windsurf.alfredworkflow` and opens it in Alfred for import.

## Usage

Open Alfred and type:

```
surf          → shows recent Windsurf items
surf ~/       → browse your home directory
surf /usr/    → browse a system path
surf myproject → Spotlight search for "myproject"
```

## How It Works

The workflow uses a Python script (`recent.py`) that reads Windsurf's recent items directly from its SQLite state database at:

```
~/Library/Application Support/Windsurf/User/globalStorage/state.vscdb
```

The database is opened in read-only mode to avoid any interference with Windsurf.
