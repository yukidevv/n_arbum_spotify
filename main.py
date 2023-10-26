#!/usr/bin/env python3

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

def main():
  value = Read_Auth_Info() # Read clientID,Client Secret
  client_id = value[0]
  client_secret = value[1]
  client_credentials_manager = spotipy.oauth2.SpotifyClientCredentials(client_id, client_secret)
  spotify = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
  #date =''
  
  track_list = Get_Track_id() #TrackID
  
  #print(track_list)

def Get_Track_id():
  get_list = []
  with open('./yyyymmdd.txt') as f:
    for line in f:
      get_list.append(line.replace("spotify:track:",'').strip())
  return get_list

def Read_Auth_Info():
  with open('./secret') as f:
    for line in f:
      value = line.split(":")
  return value

if __name__ == '__main__':
  main()