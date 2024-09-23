# 概要
SpotifyAPIを用いて、新規作成したプレイリストに楽曲を登録する自動スクリプト。  
Spotifyでは毎週、新規楽曲のプレイリストが作成されるが、プレイリストに入りきらなかった  
楽曲を含めてプレイリストに登録するようにする。
  
AlbumID  
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
# スクリプト使用法  
- 基本的な使い方  
最新の楽曲リストを取得し、自分のプレイリストに登録する    
```
usage: main.py [-h] [all]

Import music track for spotify.

positional arguments:
  all         Import all previous tracks.

options:
  -h, --help  show this help message and exit
```
