import requests
import json
import time

#reads artist ids
with open('artists_data.json', 'r') as file:
    artists_data = json.load(file)

#stores artist details
all_artist_details = []

#fetch each details for each artists
for artist in artists_data:
    artist_id = artist["idArtist"]
    url = f"https://theaudiodb.com/api/v1/json/2/artist.php?i={artist_id}"
    
    #makes an api request 
    response = requests.get(url)
    
    try:
        #parses the json response 
        data = response.json()

        #extracts the required details needed for the app 
        artist_details = data.get('artists', [])[0]  #accesses the first artist in the array 
        str_artist = artist_details.get('strArtist', '')
        str_genre = artist_details.get('strGenre', '')
        int_formed_year = artist_details.get('intFormedYear', '')
        str_biography_en = artist_details.get('strBiographyEN', '')
        str_artist_fanart = artist_details.get('strArtistFanart', '')
        id_artist = artist_details.get('idArtist', '')

        #stores the details in a list 
        artist_info = {
            "strArtist": str_artist,
            "strGenre": str_genre,
            "intFormedYear": int_formed_year,
            "strBiographyEN": str_biography_en,
            "strArtistFanart": str_artist_fanart,
            "idArtist": id_artist
        }
        all_artist_details.append(artist_info)

        #time.sleep is simply just here to comply with the rate limit of theaudiodb.com
        time.sleep(1) 

    except json.decoder.JSONDecodeError as e:
        print(f"Error decoding JSON response for Artist {artist_id}: {e}")

#saves the results in artists_data.py
with open('artists_data.py', 'w', encoding='utf-8') as python_file:
    python_file.write(f"artists_data = {all_artist_details}")
