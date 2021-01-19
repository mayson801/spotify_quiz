import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import authorise_keys

#used for testing only
def log_in():
    os.environ['SPOTIPY_CLIENT_ID'] = authorise_keys.CLI_ID
    os.environ['SPOTIPY_CLIENT_SECRET'] = authorise_keys.CLI_SEC
    spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())
    return spotify

def search_for_artist_or_playlist(auth, serch_term,type):
    if (type == 'artists'):
        results = auth.search(q='artist:' + serch_term, type='artist',limit='5')
    else:
        results = auth.search(q='playlist:' + serch_term, type='playlist',limit='5')

    items = results[type]['items']
    list_of_pos = []

    i = 0
    while i < len(items):
        if (type == 'artists'):
            followers_description = items[i]['followers']['total']
        else:
            followers_description = items[i]['description']

        artist_dict = {"artist_id": items[i]['id'],
                       "artist_name": items[i]['name'],
                       "followers/description": followers_description,
                       "artist_image": '/static/img/image_not_found.png'}

        if len(items[i]['images']) > 0:
            artist_dict["artist_image"] = items[i]['images'][0]['url']


        list_of_pos.append(artist_dict)
        i = i+1
    return list_of_pos


def get_tracks(auth,artist_id):
    albums = auth.artist_albums(artist_id, album_type = 'album',limit=50)
    listOfalbum = {}
    lis_of_songs = {}
    json_format = []
    # the first loop,loops through the artists albums, if the album name has already been used the songs are not extract
    # the reason for this is there are often multiple version of albums based on region, weather there explit, ect
    # the second for loop, loops through the songs in the album
    # if the song is already in the list of songs dict it's not added
    # the reason for this is the same song can be in multiple albums often because of re-releses and delux-versions
    for album in albums['items']:
        if album['name'] not in listOfalbum:
            listOfalbum[album['name']]=album
            songs_in_album = auth.album_tracks(album_id=album['id'])
            for song in songs_in_album['items']:
                if song['id'] not in lis_of_songs:
                    lis_of_songs[song['id']] = {"id":song['id'],"name":song['name'],"preview_url":song['preview_url']}

    for key in lis_of_songs.keys():
        json_format.append(lis_of_songs[key])
    return json_format

def get_tracks_for_playlist_or_saved(auth,playlist_id,type):
    json_format = []
    dict_of_songs = {}
    if (type == "playlists"):
        songs = auth.playlist_items(playlist_id=playlist_id, limit=100)
    else:
        songs = auth.current_user_saved_tracks()
    for song in songs['items']:
        if song['track']['id'] not in dict_of_songs:
            dict_of_songs[song['track']['id']] = {"id": song['track']['id'], "name": song['track']['name'], "preview_url": song['track']['preview_url']}

    for key in dict_of_songs.keys():
        json_format.append(dict_of_songs[key])
    return json_format

if __name__ == "__main__":
    auth = log_in()
    #testin = search_for_artist_or_playlist(auth,"kanye west","playlists")
    #testin = get_tracks(auth,'3TVXtAsR1Inumwj472S9r4')
    #testin = get_tracks_for_playlist(auth,'1WOR4r4rGFI5irhVvvbR5m')
    #print(json.dumps(testin, indent=1))
