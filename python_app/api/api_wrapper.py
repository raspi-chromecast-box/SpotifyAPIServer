import time
import os
import sys
import requests
import pprint

def get_track_ids_from_album_id( options ):
	offset = 0
	tracks = []
	while True:
		headers = {
			'Authorization': f"Bearer {options[ 'access_token' ]}" ,
		}
		data = {
			"offset": offset ,
			"fields": 'items.track.id,total'
		}
		response = requests.get( f"https://api.spotify.com/v1/albums/{options['album_id']}/tracks" , headers=headers , params=data )
		data = response.json()
		#pprint( data )
		for i , item in enumerate( data[ 'items' ] ):
			if 'id' in item:
				tracks.append( item[ 'id' ] )
		#tracks.append( data[ 'items' ] )
		offset = offset + len( data[ 'items' ] )
		print( offset , "/" , data[ 'total' ] )
		if len( data[ 'items' ] ) < 100:
			break
	return tracks

def get_track_ids_from_playlist_id( options ):
	offset = 0
	tracks = []
	while True:
		headers = {
			'Authorization': f"Bearer {options[ 'access_token' ]}" ,
		}
		data = {
			"offset": offset ,
			"fields": 'items.track.id,total'
		}
		response = requests.get( f"https://api.spotify.com/v1/playlists/{options['playlist_id']}/tracks" , headers=headers , params=data )
		data = response.json()
		for i , item in enumerate( data[ 'items' ] ):
			if 'track' in item:
				if 'id' in item[ 'track' ]:
					tracks.append( item[ 'track' ][ 'id' ] )
		#tracks.append( data[ 'items' ] )
		offset = offset + len( data[ 'items' ] )
		print( offset , "/" , data[ 'total' ] )
		if len( data[ 'items' ] ) < 100:
			break
	return tracks