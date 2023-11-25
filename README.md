# 概要
SpotifyAPIを用いて、新規作成したプレイリストに楽曲を登録する半自動スクリプト。  
Spotifyでは毎週、新規楽曲のプレイリストが作成されるが、プレイリストに入りきらなかった  
楽曲を含めてプレイリストに登録するようにする。

新規楽曲をまとめたサイトがあるので、そこから取得したTrackIDを元に  
TrackID(サイトから取得)  
↓  
AlbumID(TrackIDから楽曲が属するAlbumIDを取得)  
↓  
TrackID(上記AlbumIDに含まれる全楽曲のTrackIDを取得)  
とすることで実現した。  

# 使い方
- 認証情報について  
同一の階層に"secret"という名称でファイルを作成。  
以下の形式で認証情報を記載する。  
```
username:client_id:client_secret
```
- スクリプト使用法  
以下のサイトから取得したい楽曲のTrack情報を取得する。  
https://everynoise.com/new_releases_by_genre.cgi?genre=local&region=JP
dataフォルダ配下に実行日付を名称として(yyyymmdd)保存する。  
その後スクリプトを実行。実行日付でSpotify上にプレイリストが作成され、楽曲が登録される。  
```
./main.py
```