#!/usr/bin/env python3
import time
import os
import sys
import json
import pychromecast
from pychromecast import Chromecast
from pychromecast.controllers.spotify import SpotifyController
import spotipy
from pprint import pprint
import redis
import threading
import logging

shared_redis_connection = False
shared_options = False
shared_chromecast = False
shared_chromecast_listener = False
shared_chromecast_media_listener = False
shared_spotify_client = False
shared_spotify_device_id = False

def try_to_connect_to_redis():
	global shared_redis_connection
	try:
		shared_redis_connection = redis.StrictRedis(
			host="127.0.0.1" ,
			port="6379" ,
			db=1 ,
			#password=ConfigDataBase.self[ 'redis' ][ 'password' ]
			)
		return True
	except Exception as e:
		print( e )
		return False

def attach_custom_logger():
	global shared_chromecast
	spotify_logger = shared_chromecast.socket_client._handlers[ 'urn:x-cast:com.spotify.chromecast.secure.v1' ].logger
	FORMAT = "%(process)s %(thread)s: %(message)s"
	formatter = logging.Formatter(fmt=FORMAT)
	handler = logging.StreamHandler()
	handler.setFormatter(formatter)
	spotify_logger.addHandler(handler)
	spotify_logger.setLevel(logging.DEBUG)

def start_adhoc_listener():
	global shared_chromecast
	try:
		#['urn:x-cast:com.google.cast.tp.heartbeat', 'urn:x-cast:com.google.cast.tp.connection', 'urn:x-cast:com.google.cast.receiver', 'urn:x-cast:com.google.cast.media', 'urn:x-cast:com.spotify.chromecast.secure.v1']
		#print( shared_chromecast.media_controller.status )
		print( shared_chromecast.socket_client )
		#print( list( shared_chromecast.socket_client._handlers ) )
		#print( shared_chromecast.socket_client )
		#print( shared_chromecast.socket_client.media_controller.status )
		print( shared_chromecast.socket_client._handlers[ 'urn:x-cast:com.spotify.chromecast.secure.v1' ] )
		#print( shared_chromecast.spotify_controller.status )
	except Exception as e:
		pass
	threading.Timer( 3.0 , start_adhoc_listener ).start()

class StatusListener:
	def __init__( self , name , cast , uuid , redis_connection ):
		self.name = name
		self.cast = cast
		self.uuid = uuid
		self.redis_connection = redis_connection
	def new_cast_status( self , status ):
		#print( '[' , time.ctime() , ' - ' , self.name , '] status chromecast change:' )
		pprint( status )
		try:
			key = "STATE.UUIDS." + self.uuid
			db_object = {
				"uuid": self.uuid ,
				"name": self.name ,
				"status": {
					"is_active_input": status.is_active_input ,
					"is_stand_by": status.is_stand_by ,
					"volume_level": status.volume_level ,
					"volume_muted": status.volume_muted ,
					"app_id": status.app_id ,
					"display_name": status.display_name ,
					"namespaces": status.namespaces ,
					"session_id": status.session_id ,
					"transport_id": status.transport_id ,
					"status_text": status.status_text ,
					"icon_url": status.icon_url ,
				}
			}
			pprint( db_object )
			db_object = json.dumps( db_object )
			self.redis_connection.set( key , db_object )
			self.redis_connection.publish( "STATE" , db_object )
		except Exception as e:
			print( "Couldn't Publish to Redis Channel" )
			print( e )

class StatusMediaListener:
	def __init__( self , name , cast , uuid , redis_connection ):
		self.name = name
		self.cast = cast
		self.uuid = uuid
		self.redis_connection = redis_connection
	def new_media_status( self , status ):
		#print( '[' , time.ctime() , ' - ' , self.name , '] status media change:' )
		pprint( status )
		try:
			key = "STATE.MEDIA.UUIDS." + self.uuid
			db_object = {
				"uuid": self.uuid ,
				"name": self.name ,
				"media_status": {
					"metadata_type": status.metadata_type ,
					"title": status.title ,
					"series_title": status.series_title ,
					"season": status.season ,
					"episode": status.episode ,
					"artist": status.artist ,
					"album_name": status.album_name ,
					"album_artist": status.album_artist ,
					"track": status.track ,
					"subtitle_tracks": status.subtitle_tracks ,
					"images": status.images ,
					"supports_pause": status.supports_pause ,
					"supports_seek": status.supports_seek ,
					"supports_stream_volume": status.supports_stream_volume ,
					"supports_stream_mute": status.supports_stream_mute ,
					"supports_skip_forward": status.supports_skip_forward ,
					"supports_skip_backward": status.supports_skip_backward ,
					"current_time": status.current_time ,
					"duration": status.duration ,
					"stream_type": status.stream_type ,
					"idle_reason": status.idle_reason ,
					"media_session_id": status.media_session_id ,
					"playback_rate": status.playback_rate ,
					"player_state": status.player_state ,
					"supported_media_commands": status.supported_media_commands ,
					"volume_level": status.volume_level ,
					"volume_muted": status.volume_muted ,
					"media_custom_data": status.media_custom_data ,
					"media_metadata": status.media_metadata ,
					"current_subtitle_tracks": status.current_subtitle_tracks ,
					"last_updated": str( status.last_updated )
				}
			}
			pprint( db_object )
			db_object = json.dumps( db_object )
			self.redis_connection.set( key , db_object )
			self.redis_connection.publish( "STATUS-MEDIA" , db_object )
		except Exception as e:
			print( "Couldn't Publish to Redis Channel" )
			print( e )

def init_chromecast( options ):
	global shared_options
	global shared_redis_connection
	global shared_chromecast
	global shared_chromecast_listener
	global shared_chromecast_media_listener
	try:
		try_to_connect_to_redis()
		shared_options = options
		shared_chromecast = False
		shared_chromecast = Chromecast( shared_options[ 'chromecast_output_ip' ] )
		shared_chromecast.start()
		shared_chromecast.wait()
		shared_chromecast_listener = StatusListener( shared_chromecast.name , shared_chromecast , shared_options[ "chromecast_output_uuid" ] , shared_redis_connection )
		shared_chromecast.register_status_listener( shared_chromecast_listener )
		shared_chromecast_media_listener = StatusMediaListener( shared_chromecast.name , shared_chromecast , shared_options[ "chromecast_output_uuid" ] , shared_redis_connection )
		shared_chromecast.media_controller.register_status_listener( shared_chromecast_media_listener )
		#start_adhoc_listener()
		try:
			shared_chromecast.media_controller.stop()
		except Exception as e:
			print( e )
	except Exception as e:
		shared_chromecast = False
		return False

def launch_spotify_app():
	global shared_options
	global shared_chromecast
	global shared_spotify_client
	global shared_spotify_device_id
	try:
		if shared_chromecast == False:
			init_chromecast( shared_options )
		shared_spotify_client = False
		shared_spotify_client = spotipy.Spotify( auth=shared_options[ 'spotify_token_info' ][ "access_token" ] )
		sp = SpotifyController( shared_options[ 'spotify_token_info' ][ "access_token" ] , shared_options[ 'spotify_token_info' ][ "seconds_left" ] )
		shared_chromecast.register_handler( sp )
		sp.launch_app()
		if not sp.is_launched and not sp.credential_error:
			print('Failed to launch spotify controller due to timeout')
			return False
		if not sp.is_launched and sp.credential_error:
			print('Failed to launch spotify controller due to credential error')
			return False
		devices_available = shared_spotify_client.devices()
		#shared_spotify_device_id = False
		print( "Available Devices ==" )
		print( devices_available['devices'] )
		for device in devices_available['devices']:
			if device[ 'is_active' ] == True:
				# if device[ 'name' ] == "Attic TV":
				# 	shared_spotify_device_id = device['id']
				# 	break
				if device[ 'type' ] == "CastVideo":
					shared_spotify_device_id = device['id']
					break;
			if device['id'] == sp.device:
				shared_spotify_device_id = device['id']
				break
		if not shared_spotify_device_id:
			print('No device with id "{}" known by Spotify'.format(sp.device))
			print('Known devices: {}'.format(devices_available['devices']))
			return False
		return True
	except Exception as e:
		print( e )
		shared_spotify_client = False
		shared_spotify_device_id = False
		return False

def play_list_of_track_uris( uris ):
	global shared_spotify_client
	global shared_spotify_device_id
	try:
		if shared_spotify_client == False:
			launch_spotify_app()
		if shared_spotify_device_id == False:
			launch_spotify_app()
		shared_spotify_client.start_playback( device_id=shared_spotify_device_id , uris=uris )
		time.sleep( 2 )
		return True
	except Exception as e:
		print( e )
		return False

def play_playlist_uri( playlist_uri ):
	global shared_spotify_client
	global shared_spotify_device_id
	try:
		if shared_spotify_client == False:
			launch_spotify_app()
		if shared_spotify_device_id == False:
			launch_spotify_app()
		shared_spotify_client.start_playback( device_id=spotify_device_id , context_uri=[ playlist_uri ] )
		time.sleep( 2 )
		return True
	except Exception as e:
		print( e )
		return False

def play_album_uri( ablum_uri ):
	global shared_spotify_client
	global shared_spotify_device_id
	try:
		if shared_spotify_client == False:
			launch_spotify_app()
		if shared_spotify_device_id == False:
			launch_spotify_app()
		shared_spotify_client.start_playback( device_id=spotify_device_id , context_uri=[ ablum_uri ] )
		time.sleep( 2 )
		return True
	except Exception as e:
		print( e )
		return False

def set_shuffle_to_true():
	global shared_spotify_client
	try:
		shared_spotify_client.shuffle( True )
		return True
	except Exception as e:
		print( e )
		return False

def set_shuffle_to_false():
	global shared_spotify_client
	try:
		shared_spotify_client.shuffle( False )
		return True
	except Exception as e:
		print( e )
		return False

def stop():
	pass

def pause():
	pass

def resume():
	pass

def skip():
	pass

def previous():
	pass