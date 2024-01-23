import requests
import json
import time

# Read artist IDs from the file
with open('artists_data.json', 'r') as file:
    artists_data = json.load(file)

# List to store artist details
all_artist_details = []

# Fetch details for each artist
for artist in artists_data:
    artist_id = artist["idArtist"]
    url = f"https://theaudiodb.com/api/v1/json/2/artist.php?i={artist_id}"
    
    # Make API request
    response = requests.get(url)
    
    try:
        # Parse the JSON response
        data = response.json()

        # Extract the required details
        artist_details = data.get('artists', [])[0]  # Access the first artist in the array
        str_artist = artist_details.get('strArtist', '')
        str_genre = artist_details.get('strGenre', '')
        int_formed_year = artist_details.get('intFormedYear', '')
        str_biography_en = artist_details.get('strBiographyEN', '')
        str_artist_fanart = artist_details.get('strArtistFanart', '')
        id_artist = artist_details.get('idArtist', '')

        # Store the details in the list
        artist_info = {
            "strArtist": str_artist,
            "strGenre": str_genre,
            "intFormedYear": int_formed_year,
            "strBiographyEN": str_biography_en,
            "strArtistFanart": str_artist_fanart,
            "idArtist": id_artist
        }
        all_artist_details.append(artist_info)

        # Introduce a delay to comply with the rate limit
        time.sleep(1)  # Sleep for half a second between API calls

    except json.decoder.JSONDecodeError as e:
        print(f"Error decoding JSON response for Artist {artist_id}: {e}")

# Save the artist details to a Python file
with open('artists_data.py', 'w', encoding='utf-8') as python_file:
    python_file.write(f"artists_data = {all_artist_details}")
