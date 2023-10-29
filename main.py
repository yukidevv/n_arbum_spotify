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
  
  #TrackID(1曲分のみ)→AlbumID→TrackID→プレイリスト
  #TrackIDからAlbumIDを特定。特定したAlbumIDからTrackID(複数)を取得してその数分プレイリストに突っ込む
  track_list = Get_Track_id() #インプットファイルからTrackIDのみをListで取得
  Album_List = Get_Album_id(track_list,spotify) #TrackIDからAlbumIDを取得

  #print(track_list)

def Get_Track_id():
  get_list = []
  with open('./yyyymmdd.txt') as f:
    for line in f:
      get_list.append(line.replace("spotify:track:",'').strip())
  return get_list

def Get_Album_id(track_list,spotify):
  for trackid in track_list:
    track = spotify.track(trackid)
    print(track)
    #print("\r\n")

def Read_Auth_Info():
  with open('./secret') as f:
    for line in f:
      value = line.split(":")
  return value

if __name__ == '__main__':
  main()