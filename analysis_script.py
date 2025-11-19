import spotipy
from spotipy.oauth2 import SpotifyOAuth
import pandas as pd
from dotenv import load_dotenv
import os
import matplotlib.pyplot as plt
import seaborn as sns

# --- 1. CONFIGURATION AND AUTHENTICATION ---

# Load variables from the .env file
load_dotenv() 
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")

# REPLACE THIS WITH YOUR PLAYLIST ID (the long code you copied from the URI)
PLAYLIST_ID = '2HD9QVzdcul71owb7XMLBS'

# IMPORTANT: The corrected URI you configured in Spotify Developers
REDIRECT_URI = 'http://127.0.0.1:8888/callback' 
scope = "playlist-read-private"


# Configure authentication
print("Initiating authentication...")
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    redirect_uri=REDIRECT_URI,
    scope=scope
))

# --- 2. DATA EXTRACTION ---

def get_playlist_tracks(playlist_id):
    """Extracts all tracks from a playlist (handles large playlists)."""
    tracks_data = []
    results = sp.playlist_tracks(playlist_id)
    tracks_data.extend(results['items'])
    
    while results['next']:
        results = sp.next(results)
        tracks_data.extend(results['items'])
        
    return tracks_data

playlist_items = get_playlist_tracks(PLAYLIST_ID)
print(f"Total items collected from the playlist: {len(playlist_items)}")

# Process the data
data = []
for item in playlist_items:
    track = item['track']
    if track and track.get('album'): # Ensure track and album data exist
        try:
            # Extract only the year
            release_date = track['album']['release_date']
            year = release_date.split('-')[0] 
            
            # Convert milliseconds to minutes
            duration_min = track['duration_ms'] / 60000 
            
            data.append({
                'title': track['name'],
                'artist': track['artists'][0]['name'],
                'release_year': int(year),
                'duration_min': duration_min
            })
        except Exception as e:
            # Skip track if data is missing or malformed
            print(f"Skipping track (error: {e}) in: {track['name']}")
            continue

df = pd.DataFrame(data)

# --- 3. ANALYSIS AND EXERCISE ANSWER ---

print("\n--- Starting Data Analysis ---")

# 1. Group data and calculate the average duration per release year
avg_duration_by_year = df.groupby('release_year')['duration_min'].mean().reset_index()

# 2. Visualization to understand the trend
plt.switch_backend('TkAgg')
plt.figure(figsize=(12, 6))
sns.lineplot(x='release_year', y='duration_min', data=avg_duration_by_year)
plt.title('Relationship Between Release Year and Average Song Duration')
plt.xlabel('Release Year')
plt.ylabel('Average Duration (Minutes)')
plt.grid(True)
plt.show() # This will open the graph window

# 3. Statistical Measure (Correlation)
correlation = avg_duration_by_year['release_year'].corr(avg_duration_by_year['duration_min'])

print("\n--- Conclusion for the Exercise ---")
print(f"Correlation Coefficient (Year vs. Average Duration): {correlation:.4f}")

# Interpretation
if abs(correlation) < 0.2:
    print("The correlation is very weak. There is no significant linear relationship between the release year and the average song duration in YOUR playlist.")
elif correlation > 0:
    print(f"There is a POSITIVE correlation (Strength: {abs(correlation):.2f}). Generally, the newer the release year, the LONGER the average duration of songs in YOUR playlist.")
else:
    print(f"There is a NEGATIVE correlation (Strength: {abs(correlation):.2f}). Generally, the newer the release year, the SHORTER the average duration of songs in YOUR playlist.")