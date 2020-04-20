import random
from sanic import Blueprint
from sanic.response import json
from sanic import response

import redis

from spotify_token_util import get_spotify_token_info
from .play_currated import play_currated_uris

commands_blueprint = Blueprint( 'commands_blueprint' , url_prefix='/commands' )

# https://github.com/andymccurdy/redis-py/blob/1f857f0053606c23cb3f1abd794e3efbf6981e09/tests/test_commands.py
# https://github.com/ceberous/redis-manager-utils/blob/master/BaseClass.js
# https://redis.io/commands/sadd

def redis_previous_in_circular_list( redis_connection , list_key ):
	list_key_index = f"{list_key}.INDEX"
	# 1.) Get Length
	circular_list_length = redis_connection.llen( list_key )
	circular_list_length = int( str( circular_list_length , 'utf-8' ) )
	if circular_list_length < 1:
		return False

	# 2.) Get Previous and Recylce in Necessary
	recycled = False
	circular_list_index = redis_connection.llen( list_key_index )
	if circular_list_index is None:
		circular_list_index = ( circular_list_length - 1 )
		redis_connection.set( list_key_index , circular_list_index )
	else:
		circular_list_index = int( str( circular_list_length , 'utf-8' ) )
		circular_list_index -= 1
		redis_connection.decr( list_key_index )

	# 3.) Recycle Test
	if circular_list_index < 0:
		circular_list_index = ( circular_list_length - 1 )
		recycled = True
		redis_connection.set( list_key_index , circular_list_index )

	previous_in_circle = redis_connection.lindex( list_key , circular_list_index )
	return previous_in_circle

def redis_next_in_circular_list( redis_connection , list_key ):
	list_key_index = f"{list_key}.INDEX"
	# 1.) Get Length
	circular_list_length = redis_connection.llen( list_key )
	circular_list_length = int( str( circular_list_length , 'utf-8' ) )
	if circular_list_length < 1:
		return False

	# 2.) Get Next and Recycle if Necessary
	recycled = False
	circular_list_index = redis_connection.llen( list_key_index )
	if circular_list_index is None:
		circular_list_index = 0
		redis_connection.set( list_key_index , '0' )
	else:
		circular_list_index = int( str( circular_list_length , 'utf-8' ) )
		circular_list_index += 1
		redis_connection.incr( list_key_index )

	# 3.) Recycle Test
	if circular_list_index > ( circular_list_length - 1 ):
		circular_list_index = 0
		recycled = True
		redis_connection.set( list_key_index , '0' )

	next_in_circle = redis_connection.lindex( list_key , circular_list_index )
	return next_in_circle

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

@commands_blueprint.route( '/' )
def commands_root( request ):
	return response.text( "you are at the /commands url\n" )

@commands_blueprint.route( '/play' )
def play( request ):
	#return response.text( "you are at the /commands url\n" )
	return json({'my': 'blueprint'})

@commands_blueprint.route( '/play/currated' )
def play_currated( request ):

	redis_connection = try_to_connect_to_redis()

	spotify_token_info = get_spotify_token_info()

	chromecast_output_ip = redis_connection.get( "STATE.CHROMECAST_OUTPUT.IP" )
	chromecast_output_ip = str( chromecast_output_ip , 'utf-8' )
	print( chromecast_output_ip )

	uris = redis_connection.smembers( 'SPOTIFY.CURRATED_URIS.ALL' )
	uris = list( map( lambda x: str( x , 'utf-8' ) , uris ) )

	print( uris )

	result = play_currated_uris( spotify_token_info , chromecast_output_ip , uris )
	#return response.text( "you are at the /commands url\n" )
	return json( { 'result': result } )

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

