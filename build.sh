#!/bin/bash
cd "$(dirname "$0")"
zip -j "Open in Windsurf.alfredworkflow" info.plist recent.py
open "Open in Windsurf.alfredworkflow"
