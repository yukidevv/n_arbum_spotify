#!/usr/bin/env python3

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy.util as util
import datetime

def main():
  value = Read_Auth_Info() # Read clientID,Client Secret
  username = value[0]
  client_id = value[1]
  client_secret = value[2]
  redirect_uri = 'http://localhost'
  client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
  spotify = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
  scope = 'playlist-modify-public playlist-modify-private'
  token = util.prompt_for_user_token(username,scope, client_id=client_id,client_secret=client_secret,redirect_uri=redirect_uri)
  spotify = spotipy.Spotify(auth = token)

  date = datetime.date.today()
  date = date.strftime('%Y%m%d')
  
  #TrackID(1曲分のみ)→AlbumID→TrackID→プレイリスト

  #TrackIDからAlbumIDを特定。特定したAlbumIDからTrackID(複数)を取得してその数分プレイリストに突っ込む
  track_list_from_file = Get_Trackid() #インプットファイルからTrackIDのみをListで取得
  album_list_from_trackid = Get_Albumid(track_list_from_file,spotify) #TrackIDからAlbumIDを取得
  track_list_from_albumid = Get_Trackid_from_albumid(album_list_from_trackid,spotify)#AlbumIDからAlbum内の全トラックを取得
  #TODO 全トラックを新規プレイリストとして保存する
  make_play_list(username,spotify,date)

def Get_Trackid():
  get_list = []
  with open('./yyyymmdd.txt') as f:
    for line in f:
      get_list.append(line.replace("spotify:track:",'').strip())
  return get_list

def Get_Albumid(track_list,spotify):
  album_list = []
  for trackid in track_list:
    album_info = spotify.track(trackid)
    #print(album_info)
    album_list.append(album_info['album']['id'])
  return album_list

def Get_Trackid_from_albumid(album_list_from_trackid,spotify):
  track_list = []
  for albumid_items in album_list_from_trackid:
    track_info = spotify.album_tracks(albumid_items)
    for item in track_info['items']:
      track_list.append(item['id'])
  return track_list

def make_play_list(username,spotify,date):
  play_list_dict = spotify.user_playlist_create(username,date)
  print(play_list_dict)
  play_list_url = play_list_dict['external_urls']
  play_list_url = json.dumps(play_list_url)
  str_url = play_list_url.replace('{\"spotify\": "','')

def Read_Auth_Info():
  with open('./secret') as f:
    for line in f:
      value = line.split(":")
  return value

if __name__ == '__main__':
  main()