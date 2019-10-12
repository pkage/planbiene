import sys
import spotipy
import json
import spotipy.util as util

with open("secrets.json", "r") as content:
    keys = json.loads(content.read())

CLIENT_ID = keys["client_id"]
CLIENT_SECRET = keys["client_secret"]
REDIRECT_URI = "http://localhost/"

def prompt_get_token(username):
    token = util.prompt_for_user_token(
        username, 
        'user-top-read', 
        client_id=CLIENT_ID, 
        client_secret=CLIENT_SECRET, 
        redirect_uri=REDIRECT_URI
    )
    return token

def get_user_top_artists(number_of_artists, token):
    if token:
        sp = spotipy.Spotify(auth=token)
        sp.trace = False
        artists = sp.current_user_top_artists(time_range='long_term', limit=number_of_artists)
        artists = [artist['name'] for artist in artists['items']]
        return artists
    else:
        # the worst hardcoded-handpicked-eyeballed list
        return ["Ariana Grande", "Rihanna", "Imagine Dragons", "Billie Eilish", "Arcade Fire"]

if __name__ == "__main__":
    print(get_user_top_artists(sys.argv[2], prompt_get_token(sys.argv[1])))