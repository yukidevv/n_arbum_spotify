#!/usr/bin/env python3

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy.util as util
import datetime
import os

def main():
  DEBUG = os.getenv("DEBUG", None) is not None

  value = ReadAuthInfo() # Read clientID,Client Secret
  username = value[0]
  client_id = value[1]
  client_secret = value[2]
  redirect_uri = 'http://localhost'
  client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
  spotify = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
  scope = 'playlist-modify-public'
  token = util.prompt_for_user_token(username,scope, client_id=client_id,client_secret=client_secret,redirect_uri=redirect_uri)
  spotify = spotipy.Spotify(auth = token)

  date = datetime.date.today()
  date = date.strftime('%Y%m%d')
  
  #TrackID(1曲分のみ)→AlbumID→TrackID→プレイリスト
  #TrackIDからAlbumIDを特定。特定したAlbumIDからTrackID(複数)を取得してその数分プレイリストに突っ込む
  
  track_list_from_file = GetTrackId(date)
  album_list_from_trackid = GetAlbumId(track_list_from_file,spotify)
  track_list_from_albumid = GetTrackIdFromAlbumId(album_list_from_trackid,spotify)
  if not DEBUG :
    MakePlayList(username,spotify,date,track_list_from_albumid)

#FileからTrackIDのリストを取得
def GetTrackId(date):
  track_list = []
  with open('data/in/' + date) as f:
    for line in f:
      track_list.append(line.replace("spotify:track:",'').strip())
  return track_list

#TrackIDからAlbumIDを取得
def GetAlbumId(track_list,spotify):
  album_list = []
  for trackid in track_list:
    album_info = spotify.track(trackid)
    album_list.append(album_info['album']['id'])
  return album_list

#AlbumIDからTrackID(Fileから取得したTrackIDが属するAlbumID内の全てのTrackIDを取得)
def GetTrackIdFromAlbumId(album_list_from_trackid,spotify):
  track_list = []
  for albumid_items in album_list_from_trackid:
    track_info = spotify.album_tracks(albumid_items)
    for item in track_info['items']:
      track_list.append(item['id'])
  #CreateLog(track_list)
  return track_list

#取得したTrackID全てを新規作成したプレイリストに突っ込む
def MakePlayList(username,spotify,date,track_list_from_albumid):
  play_list_info = spotify.user_playlist_create(username,date)
  play_list_id = play_list_info['id']
  spotify.user_playlist_add_tracks(username,play_list_id,track_list_from_albumid)

#TODO
#def CreateLog(track_list):
  
#認証情報の取得
def ReadAuthInfo():
  with open('./secret') as f:
    for line in f:
      value = line.split(":")
  return value

if __name__ == '__main__':
  main()