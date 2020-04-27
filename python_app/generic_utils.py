import os
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


def save_personal_file_to_redis():
	personal_file_path = os.path.join( os.path.expanduser( "~" ) , ".config" , "personal" , "raspi_chromecast_box.json" )
	with open( personal_file_path ) as f:
		personal_file = json.load( f )
	personal_spotify = personal_file[ "personal" ][ "spotify" ]
	redis_connection = redis_utils.try_to_connect_to_redis()
	redis_connection.set( "PERSONAL.SPOTIFY" , json.dumps( personal_spotify ) )

# https://github.com/bjarneo/Pytify
# https://github.com/maschhoff/py-spotify-track-album-control/blob/master/py-spotify-trackcontrol/spotify_auth.py
def get_common_config():
	redis_connection = redis_utils.try_to_connect_to_redis()
	spotify_token_info = get_spotify_token_info()
	# spotify_api_credentials = redis_connection.get( "PERSONAL.SPOTIFY" )
	# spotify_api_credentials = json.loads( spotify_api_credentials )
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