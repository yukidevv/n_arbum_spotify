#!/usr/bin/env python3

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy.util as util
import datetime
import os
import sys
import click

def main():
  #デバッグ
  DEBUG = os.getenv("DEBUG", None) is not None

  value = read_auth_info() # Read clientID,Client Secret
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
  option = option_handle()
  if DEBUG:
    #sandbox
    exit()
  if option == "imp":
    #AlbumIDからTrackID(複数)を取得してその数分プレイリストに突っ込む
    album_lists = get_new_album_lists(spotify.new_releases(country='JP'))
    make_play_list(username,spotify,date,get_track_id_from_album_lists(album_lists,spotify))
  elif option == "all":
    all_track_list = get_all_track_id_list()
    make_play_list(username,spotify,"All_New_Track",all_track_list)

#AlbumIDからTrackID(Fileから取得したTrackIDが属するAlbumID内の全てのTrackIDを取得)
def get_track_id_from_album_lists(album_list_from_trackid,spotify):
  track_list = []
  for albumid_items in album_list_from_trackid:
    track_info = spotify.album_tracks(albumid_items)
    for item in track_info['items']:
      track_list.append(item['id'])
  create_log(track_list)
  return track_list

#取得したTrackID全てを新規作成したプレイリストに突っ込む
def make_play_list(username,spotify,trackname,track_list_from_albumid):
  play_list_info = spotify.user_playlist_create(username,trackname)
  play_list_id = play_list_info['id']
  #上限が100リクエストまでなので100件ずつ区切って処理を行う
  while track_list_from_albumid:
    spotify.user_playlist_add_tracks(username,play_list_id,track_list_from_albumid[:100])
    track_list_from_albumid = track_list_from_albumid[100:]

#追加した楽曲を記憶し、ファイルに書き出ししておく
def create_log(track_list):
  with open('data/out/log', mode = 'a') as f:
    for track in track_list:
      f.write("spotify:track:" + track + "\r\n")

#オプションの判定
@click.group()
def option_handle():
  pass

@option_handle.command('imp')
def sub_new_track_import():
  return "imp"

@option_handle.command('all')
def sub_all_new_track_import():
  return "all"

def get_all_track_id_list():
  track_list = []
  with open('data/out/log') as f:
    for line in f:
      track_list.append(line.replace("spotify:track:",'').strip())
  return track_list

def get_new_album_lists(new_releases_lists):
  new_album_id_lists = []
  for new_album_id in new_releases_lists['albums']['items']:
    new_album_id_lists.append(new_album_id['id'])
  return new_album_id_lists

#認証情報の取得
def read_auth_info():
  with open('secret') as f:
    for line in f:
      value = line.split(":")
  return value

if __name__ == '__main__':
  main()
