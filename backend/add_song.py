import requests
import json
import time

# The URL of your API endpoint
BASE_URL = "http://127.0.0.1:5000/api/songs/"

def add_song(title, artist, genre):
    """
    Sends a POST request to the API to add a new song.
    """
    song_data = {
        "title": title,
        "artist": artist,
        "genre": genre
    }

    try:
        response = requests.post(BASE_URL, json=song_data)
        response.raise_for_status()  # This will raise an exception for HTTP errors
        
        # Parse the JSON response
        data = response.json()
        print(f"Successfully added '{title}' by {artist} ({genre})!")
        print(f"Response from API: {data}")
        print("-" * 20)

    except requests.exceptions.RequestException as e:
        print(f"Error adding song '{title}' by {artist}: {e}")
        
if __name__ == "__main__":
    # A list of 20 songs from different genres
    songs_to_add = [
        # Pop
        {"title": "Shape of You", "artist": "Ed Sheeran", "genre": "Pop"},
        {"title": "Blinding Lights", "artist": "The Weeknd", "genre": "Pop"},
        {"title": "Uptown Funk", "artist": "Mark Ronson ft. Bruno Mars", "genre": "Pop"},
        {"title": "Rolling in the Deep", "artist": "Adele", "genre": "Pop"},
        {"title": "Happy", "artist": "Pharrell Williams", "genre": "Pop"},
        
        # Rock
        {"title": "Bohemian Rhapsody", "artist": "Queen", "genre": "Rock"},
        {"title": "Hotel California", "artist": "Eagles", "genre": "Rock"},
        {"title": "Smells Like Teen Spirit", "artist": "Nirvana", "genre": "Rock"},
        {"title": "Back in Black", "artist": "AC/DC", "genre": "Rock"},
        {"title": "Stairway to Heaven", "artist": "Led Zeppelin", "genre": "Rock"},
        
        # Hip-Hop
        {"title": "Lose Yourself", "artist": "Eminem", "genre": "Hip-Hop"},
        {"title": "God's Plan", "artist": "Drake", "genre": "Hip-Hop"},
        {"title": "HUMBLE.", "artist": "Kendrick Lamar", "genre": "Hip-Hop"},
        {"title": "In Da Club", "artist": "50 Cent", "genre": "Hip-Hop"},
        {"title": "Hey Ya!", "artist": "OutKast", "genre": "Hip-Hop"},
        
        # R&B
        {"title": "Crazy in Love", "artist": "Beyoncé ft. Jay-Z", "genre": "R&B"},
        {"title": "No Scrubs", "artist": "TLC", "genre": "R&B"},
        {"title": "Waterfalls", "artist": "TLC", "genre": "R&B"},
        {"title": "One Dance", "artist": "Drake ft. Wizkid & Kyla", "genre": "R&B"},
        {"title": "Adore You", "artist": "Harry Styles", "genre": "R&B"},
    ]
    
    # Loop through the list and add each song
    for song in songs_to_add:
        add_song(song["title"], song["artist"], song["genre"])
        time.sleep(1) # Add a small delay between requests
