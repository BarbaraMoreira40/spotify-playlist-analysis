# Spotify Playlist Analysis

Analyze Spotify playlist metadata (release year vs average duration) using Spotipy, pandas and matplotlib.

## Description
This project fetches tracks from a Spotify playlist and analyzes the relationship between release year and average song duration. It demonstrates authentication with Spotify Web API via Spotipy and basic data analysis/visualization in Python.

## Features
- Authenticate with Spotify using OAuth
- Download all tracks from a playlist (handles pagination)
- Compute average duration per release year
- Plot a trendline and compute correlation coefficient

## Setup

1. Clone the repo:
```bash
git clone https://github.com/<your-username>/spotify-playlist-analysis.git
cd spotify-playlist-analysis
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS / Linux:
source .venv/bin/activate
pip install -r requirements.txt
CLIENT_ID=your_spotify_client_id
CLIENT_SECRET=your_spotify_client_secret
Add your playlist ID in analysis_script.py (or use test_spotify.py to test connection).
