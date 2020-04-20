from sanic import Blueprint
from sanic.response import json
from sanic import response

from .api_wrapper import get_track_ids_from_album_id
from .api_wrapper import get_track_ids_from_playlist_id
from spotify_token_util import get_spotify_token_info

def try_to_connect_to_redis():
	try:
		redis_connection = redis.StrictRedis(
			host="127.0.0.1" ,
			port="6379" ,
			db=1 ,
			#password=ConfigDataBase.self[ 'redis' ][ 'password' ]
			)
		return redis_connection
	except Exception as e:
		return False

def decode_spotify_uri_string( spotify_uri_string ):
	decoded = spotify_uri_string.split( ":" )
	print( decoded )
	if len( decoded ) < 2:
		return json({
				"error": "Couldn't Decode The Passed Spotify URI" ,
				"uri_sent": decode
			})
	if len( decoded ) == 2:
		if decoded[ 0 ] != "album" or decoded[ 0 ] != "playlist" or decoded[ 0 ] != "track":
			return json({
					"error": "Couldn't Decode The Passed Spotify URI" ,
					"suggestion": "Spotify -> ... -> Share -> Copy Spotify URI" ,
					"uri_sent": decode
				})
	decoded.insert( "spotify" )
	return decoded

def get_uris_from_decoded( decoded ):
	if len( decoded ) < 3:
		return []
	if decoded[ 1 ] == "track":
		return [ decoded[ 2 ] ]
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
		return []
	return uris

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

@api_blueprint.route( "/uris/<message>" , methods=[ "GET" ] )
def token_info( request , message ):
	try:
		decoded = decode_spotify_uri_string( message )
		uris = get_uris_from_decoded( decoded )
		return json({
				"uris": uris
			})
	except Exception as e:
		print( e )
		return json({
				"error": "Couldn't Get Spotify Track URIS" ,
				"python_error": e ,
				"suggestion": "Spotify -> ... -> Share -> Copy Spotify URI" ,
				"uri_sent": decode
			})

@api_blueprint.route( "/import/currated/all/<message>" , methods=[ "GET" ] )
def import_currated_all( request , message ):
	try:
		decoded = decode_spotify_uri_string( message )
		uris = get_uris_from_decoded( decoded )
		print( uris )
		redis_connection = try_to_connect_to_redis()
		redis_connection.sadd( 'SPOTIFY.CURRATED_URIS.ALL' , *uris )
		return response.text( "imported\n" )
	except Exception as e:
		return json({ "message": "Couldn't Import Spotify URIS" , "python_error": str( e ) })
