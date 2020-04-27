#!/usr/bin/env python3
import time
import os
import sys
import json
import pychromecast
from pychromecast import Chromecast
from pychromecast.controllers.spotify import SpotifyController
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# Old Example
# https://github.com/raspi-chromecast-box/WebServer/blob/f434683eff7d2e19ac926b54cf3f3739fadb0646/node_app/commands/Spotify/Play.py

def play_currated_uris( spotify_api_credentials , chromecast_output_ip , uris ):
	try:
		cast = Chromecast( chromecast_output_ip )
		cast.wait()
		cast.media_controller.stop()
		#client = spotipy.Spotify( auth=spotify_token_info[ "access_token" ] )
		client = spotipy.Spotify( client_credentials_manager=SpotifyClientCredentials( client_id=spotify_api_credentials[ "client_id" ] , client_secret=spotify_api_credentials[ "client_secret" ] ) )
		sp = SpotifyController( spotify_token_info[ "access_token" ] , spotify_token_info[ "seconds_left" ] )
		cast.register_handler( sp )
		sp.launch_app()
		if not sp.is_launched and not sp.credential_error:
			print('Failed to launch spotify controller due to timeout')
			return False
		if not sp.is_launched and sp.credential_error:
			print('Failed to launch spotify controller due to credential error')
			return False

		devices_available = client.devices()
		spotify_device_id = None
		for device in devices_available['devices']:
			if device['id'] == sp.device:
				spotify_device_id = device['id']
				break
		if not spotify_device_id:
			print( 'No device with id "{}" known by Spotify'.format( sp.device) )
			print( 'Known devices: {}'.format( devices_available['devices'] ) )
			return False

		client.start_playback( device_id=spotify_device_id , uris=uris )
		time.sleep( 2 )
		client.volume( 99 )
		time.sleep( 2 )
		client.volume( 100 )
		client.shuffle( False )
		return True
	except Exception as e:
		print( "Couldn't Load Spotify Chromecast App" )
		print( e )
		return False

# def try_run_block( options ):
# 	for i in range( options[ 'number_of_tries' ] ):
# 		attempt = options[ 'function_reference' ]( options[ 'function_args' ] )
# 		if attempt is not False:
# 			return attempt
# 		print( f"Couldn't Run '{ options[ 'task_name' ] }', Sleeping for { str( options[ 'sleep_inbetween_seconds' ] ) } Seconds" )
# 		time.sleep( options[ 'sleep_inbetween_seconds' ] )
# 	if options[ 'reboot_on_failure' ] == True:
# 		os.system( "reboot -f" )

# try_run_block({
# 	"task_name": "Spotify Play Currated URIS" ,
# 	"number_of_tries": 5 ,
# 	"sleep_inbetween_seconds": 1 ,
# 	"function_reference": play_currated ,
# 	"reboot_on_failure": True
# 	})
