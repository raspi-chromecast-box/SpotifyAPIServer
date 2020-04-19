from sanic import Blueprint
from sanic.response import json
from sanic import response

from .api_wrapper import get_track_ids_from_playlist_id
from spotify_token_util import get_spotify_token_info

api_blueprint = Blueprint( 'api_blueprint' , url_prefix='/api' )

@api_blueprint.route( '/' )
def commands_root( request ):
	return response.text( "you are at the /api url\n" )

@api_blueprint.route( '/test/<unknown>' )
def commands_root( request , unknown ):
	print( "wtf are <> params" )
	print( unknown )
	return json( { "result": unknown } )

@api_blueprint.route( "/token" , methods=[ "GET" ] )
def token_info( request ):
	try:
		result = get_spotify_token_info()
	except Exception as e:
		result = { "message": "Couldn't Get Spotify Token" }
	return json( result )

@api_blueprint.route( "/uris" , methods=[ "GET" ] )
def token_info( request ):
	try:
		token_info = get_spotify_token_info()
		options = {
			"access_token": token_info[ 'access_token' ] ,
			"playlist_id": request.args.get( "playlist_id" )
		}
		track_ids = get_track_ids_from_playlist_id( options )
		result = { "track_ids": track_ids }
	except Exception as e:
		result = { "message": "Couldn't Get Spotify Playlist Tracks" }
	return sanic_json( result )