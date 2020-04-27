import sys
import random
import json
import redis_utils
from spotify_token_util import get_spotify_token_info

def shuffle_list( list_to_shuffle ):
	seed_int = random.randint( 0 , sys.maxsize )
	random.seed( seed_int )
	random.shuffle( list_to_shuffle )
	return list_to_shuffle

def prepare_random_track_uris( uris ):
	uris = list( map( lambda x: str( x , 'utf-8' ) , uris ) )
	uris = shuffle_list( uris )
	uris = shuffle_list( uris )
	uris = shuffle_list( uris )
	uris = list( map( lambda x: 'spotify:track:' + x , uris ) )
	return uris

def get_common_config():
	redis_connection = redis_utils.try_to_connect_to_redis()
	#spotify_token_info = get_spotify_token_info()
	spotify_api_credentials = redis_connection.get( "PERSONAL.SPOTIFY" )
	spotify_api_credentials = json.loads( spotify_api_credentials )
	chromecast_output_ip = redis_connection.get( "STATE.CHROMECAST_OUTPUT.IP" )
	chromecast_output_ip = str( chromecast_output_ip , 'utf-8' )
	chromecast_output_uuid = redis_connection.get( "CONFIG.CHROMECAST_OUTPUT.UUID" )
	chromecast_output_uuid = str( chromecast_output_uuid , 'utf-8' )
	return {
		"redis_connection": redis_connection ,
		"spotify_token_info": spotify_token_info ,
		"chromecast_output_ip": chromecast_output_ip ,
		"chromecast_output_uuid": chromecast_output_uuid
	}