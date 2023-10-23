#!/usr/bin/env python3

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

client_id = '' 
client_secret = '' 
client_credentials_manager = spotipy.oauth2.SpotifyClientCredentials(client_id, client_secret)
spotify = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

def main():
  data = Read_ArtistData()
  print(data)

def Read_ArtistData():
  artist_id = ''
  return artist_id
  
if __name__ == '__main__':
  main()