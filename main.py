from bs4 import BeautifulSoup
import requests
import argparse
import datetime as dt
import spotipy
from spotipy.oauth2 import SpotifyOAuth

import logging
# logger = logging.getLogger('examples.create_playlist')
# logging.basicConfig(level='DEBUG')


def get_top_songs(date):
    print(f"Getting Billboard Top 100 Songs from {date}")
    response = requests.get(f"https://www.billboard.com/charts/hot-100/{date}")
    soup = BeautifulSoup(response.text, "html.parser")

    rank_list = [tag.get_text() for tag in soup.find_all("span", class_="chart-element__rank__number")]
    song_list = [tag.get_text() for tag in
                 soup.find_all("span", class_="chart-element__information__song text--truncate color--primary")]
    artist_list = [tag.get_text() for tag in
                   soup.find_all("span", class_="chart-element__information__artist text--truncate color--secondary")]

    top_songs_dict = {}
    for index in range(len(rank_list)):
        top_songs_dict[rank_list[index]] = {'artist': artist_list[index], 'song': song_list[index]}

    return top_songs_dict


def create_connection():
    scope = "playlist-modify-public"
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))
    return sp


def find_uri(connection, year, artist, track):
    sp = connection
    result = sp.search(q=f"track: {track} artist: {artist} year: {year}", type="track")

    # Check to see if result has a URI attached, if not, the song could not be found in the spotify database
    try:
        uri = result['tracks']['items'][1]['uri']
    except IndexError:
        uri = None

    return uri


def create_playlist(connection, title, description, song_dict):
    print("Creating Playlist")
    sp = connection

    user_id = sp.me()['id']
    result = sp.user_playlist_create(user=user_id, name=title, description=description)
    playlist_id = result['id']
    playlist_link = result['external_urls']['spotify']

    track_list = [song_dict[song]['uri'] for song in song_dict if song_dict[song]['uri'] is not None]

    sp.user_playlist_add_tracks(user=user_id, playlist_id=playlist_id, tracks=track_list, position=None)
    print(f"Playlist Created: {playlist_link}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("date", help="date to use in the format YYYY-MM-DD")
    args = parser.parse_args()

    date = dt.datetime.strptime(args.date, "%Y-%m-%d")
    formatted_date = date.strftime("%Y-%m-%d")
    year = date.year

    song_dict = get_top_songs(date=formatted_date)
    print("Connecting to Spotify...")
    sp = create_connection()
    print("Connected.")
    print("Finding Songs...")
    for key in song_dict:
        song_dict[key]['uri'] = find_uri(connection=sp, year=year, artist=song_dict[key]['artist'],
                                         track=song_dict[key]['song'])

    num_found = sum(song_dict[key]['uri'] is not None for key in song_dict)
    print(f"{num_found} songs found.")

    create_playlist(connection=sp, title=f"Billboard 100 from {formatted_date}",
                    description=f"{formatted_date} Billboard 100",
                    song_dict=song_dict)


if __name__ == '__main__':
    main()
