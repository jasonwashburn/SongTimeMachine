# Song Time Machine

Usage: `python3 ./main.py YYYY-DD-MM`

A python script that finds the [Billboard Top 100 Songs](https://www.billboard.com/charts/hot-100) from the requested 
date and creates a [Spotify](https://www.spotify.com) playlist.

Uses Beautiful Soup to scrape the [Billboard Top 100](https://www.billboard.com/charts/hot-100) page and 
the [Spotipy](https://pypi.org/project/spotipy/) library with 
the [Spotify API](https://developer.spotify.com/documentation/web-api/)

Requires the following environment variables
- `SPOTIPY_CLIENT_ID`
- `SPOTIPY_CLIENT_SECRET`
- `SPOTIPY_REDIRECT_URI`
