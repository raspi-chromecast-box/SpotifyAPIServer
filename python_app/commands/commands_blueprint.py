import sys
import random

from sanic import Blueprint
from sanic.response import json
from sanic import response

import generic_utils
import redis_utils

from spotify_token_util import get_spotify_token_info
from .play_currated import play_currated_uris
from .shared_cast_instance import *

commands_blueprint = Blueprint( "commands_blueprint" , url_prefix="/commands" )

@commands_blueprint.route( '/' )
def commands_root( request ):
	return response.text( "you are at the /commands url\n" )

@commands_blueprint.route( '/play' )
def play( request ):
	#return response.text( "you are at the /commands url\n" )
	return json({'my': 'blueprint'})

@commands_blueprint.route( '/rebuild/list/currated/all' )
def rebuild_list_currated_all( request ):
	redis_connection = redis_utils.try_to_connect_to_redis()
	uris = redis_connection.smembers( 'SPOTIFY.CURRATED_URIS.ALL' )
	uris = list( map( lambda x: str( x , 'utf-8' ) , uris ) )
	redis_connection.delete( 'SPOTIFY.CURRATED_URIS.ALL.LIST' )
	redis_connection.rpush( 'SPOTIFY.CURRATED_URIS.ALL.LIST' , *uris )
	return response.text( "rebuild the currated all list\n" )

@commands_blueprint.route( '/play/list/currated/all/test' )
def play_list_currated_all_test( request ):
	config = generic_utils.get_common_config()
	uri = redis_utils.next_in_circular_list( config[ "redis_connection" ] , 'SPOTIFY.CURRATED_URIS.ALL.LIST' )
	uri = f"spotify:track:{uri}"
	print( "trying to play: " + uri )
	result = play_currated_uris( config[ "spotify_token_info" ] , config[ "chromecast_output_ip" ] , [ uri ] )
	return response.text( "playing the next track in currated all circular list\n" )

@commands_blueprint.route( '/play/currated' )
def play_currated( request ):
	config = generic_utils.get_common_config()
	print( config )
	uris = config[ "redis_connection" ].srandmember( 'SPOTIFY.CURRATED_URIS.ALL' , 200 )
	uris = generic_utils.prepare_random_track_uris( uris )
	result = play_currated_uris( config[ "spotify_token_info" ] , config[ "chromecast_output_ip" ] , uris )
	return json( { 'result': str( result ) , 'uris': uris } )

@commands_blueprint.route( '/pause' )
def pause( request ):
	#return response.text( "you are at the /commands url\n" )
	return json({'my': 'blueprint'})

@commands_blueprint.route( '/resume' )
def resume( request ):
	#return response.text( "you are at the /commands url\n" )
	return json({'my': 'blueprint'})

@commands_blueprint.route( '/next' )
def next( request ):
	#return response.text( "you are at the /commands url\n" )
	return json({'my': 'blueprint'})

@commands_blueprint.route( '/previous' )
def previous( request ):
	#return response.text( "you are at the /commands url\n" )
	return json({'my': 'blueprint'})

@commands_blueprint.route( '/shuffle_false' )
def shuffle_false( request ):
	#return response.text( "you are at the /commands url\n" )
	return json({'my': 'blueprint'})

@commands_blueprint.route( '/shuffle_true' )
def shuffle_true( request ):
	#return response.text( "you are at the /commands url\n" )
	return json({'my': 'blueprint'})

@commands_blueprint.route( '/spotify-paused' )
def spotify_paused( request ):
	print( "they told us spotify is now paused" )
	print( "we are assuming that we did not do this via a usb-button" )
	print( "so if STATE.PLAYING_CURRATED = true , or something like that, start off the next currated track" )
	return response.text( "gracias\n" )
