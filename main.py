#!/usr/bin/env python3

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy.util as util
import datetime
import os
import sys

def main():
  #デバッグ
  DEBUG = os.getenv("DEBUG", None) is not None

  #オプション判定
  flg = OptionHandle() 

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
  if flg == "":
    track_list_from_file = GetTrackId(date)
    album_list_from_trackid = GetAlbumId(track_list_from_file,spotify)
    track_list_from_albumid = GetTrackIdFromAlbumId(album_list_from_trackid,spotify)
    MakePlayList(username,spotify,date,track_list_from_albumid)
  if flg == "all":
    all_track_list = GetAllTrackIdList()
    MakePlayList(username,spotify,"All_New_Track",all_track_list)

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
  CreateLog(track_list)
  return track_list

#取得したTrackID全てを新規作成したプレイリストに突っ込む
def MakePlayList(username,spotify,trackname,track_list_from_albumid):
  play_list_info = spotify.user_playlist_create(username,trackname)
  play_list_id = play_list_info['id']
  #上限が100リクエストまでなので100件ずつ区切って処理を行う
  while track_list_from_albumid:
    spotify.user_playlist_add_tracks(username,play_list_id,track_list_from_albumid[:100])
    track_list_from_albumid = track_list_from_albumid[100:]

#追加した楽曲を記憶し、ファイルに書き出ししておく
def CreateLog(track_list):
  with open('data/out/log', mode = 'w') as f:
    for track in track_list:
      f.write("spotify:track:" + track + "\r\n")

#オプションの判定
def OptionHandle():
  args = sys.argv
  if len(args) != 2:
    return ""    
  if(args[1] == "all"):
    return "all"

def GetAllTrackIdList():
  track_list = []
  with open('data/out/log') as f:
    for line in f:
      track_list.append(line.replace("spotify:track:",'').strip())
  return track_list

#認証情報の取得
def ReadAuthInfo():
  with open('secret') as f:
    for line in f:
      value = line.split(":")
  return value

if __name__ == '__main__':
  main()
