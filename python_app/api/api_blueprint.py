from sanic import Blueprint
from sanic.response import json
from sanic import response

from .api_wrapper import get_track_ids_from_album_id
from .api_wrapper import get_track_ids_from_playlist_id
from spotify_token_util import get_spotify_token_info

api_blueprint = Blueprint( 'api_blueprint' , url_prefix='/api' )

@api_blueprint.route( '/' )
def commands_root( request ):
	return response.text( "you are at the /api url\n" )

@api_blueprint.route( "/token" , methods=[ "GET" ] )
def token_info( request ):
	try:
		result = get_spotify_token_info()
	except Exception as e:
		result = { "message": "Couldn't Get Spotify Token" }
	return json( result )

@api_blueprint.route( "/uris/<decode>" , methods=[ "GET" ] )
def token_info( request , decode ):
	try:
		decoded = decode.split( ":" )
		if len( decoded ) < 2:
			return json({
					"error": "Couldn't Decode The Passed Spotify URI" ,
					"uri_sent": decode
				})
		if len( decoded ) == 2:
			if decoded[ 0 ] != "album" or decoded[ 0 ] != "playlist" or decoded[ 0 ] != "track":
				return json({
						"error": "Couldn't Decode The Passed Spotify URI" ,
						"suggestion": "Spotify -> ... -> Share -> Copy Spotify URI"
						"uri_sent": decode
					})
			decoded.insert( "spotify" )
		if decoded[ 1 ] == "track":
			return json({
					"uris": [ decoded[ 2 ] ] ,
				})
		token_info = get_spotify_token_info()
		if decoded[ 1 ] == "album":
			uris = get_track_ids_from_album_id({
					"access_token": token_info[ 'access_token' ] ,
					"album_id": decoded[ 2 ]
				})
		elif decoded[ 1 ] == "playlist":
			uris = get_track_ids_from_playlist_id({
					"access_token": token_info[ 'access_token' ] ,
					"playlist_id": decoded[ 2 ]
				})
		else:
			return json({
					"error": "Couldn't Decode The Passed Spotify URI" ,
					"suggestion": "Spotify -> ... -> Share -> Copy Spotify URI"
					"uri_sent": decode
				})
		return json({
				"uris": uris
			})
	except Exception as e:
		print( e )
		return json({
				"error": "Couldn't Get Spotify Track URIS" ,
				"python_error": e ,
				"suggestion": "Spotify -> ... -> Share -> Copy Spotify URI"
				"uri_sent": decode
			})

