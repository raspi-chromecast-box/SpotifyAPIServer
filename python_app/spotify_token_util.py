#!/usr/bin/env python3
import http.client as http_client
import time
import os
import sys
import json
import pychromecast
from pychromecast import Chromecast
from pychromecast.controllers.spotify import SpotifyController
import spotify_token as st
import redis
import spotipy

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

def GenerateSpotifyToken( options ):
	try:
		print( "Generating Spotify Token" )
		print( options )
		data = st.start_session( options[ "username" ] , options[ "password" ] )
		access_token = data[ 0 ]
		seconds_left = data[ 1 ] - int( time.time() )
		result = {
			"access_token": access_token ,
			"expire_time": data[ 1 ] ,
			"seconds_left": seconds_left
		}
		return result
	except Exception as e:
		print( "Couldn't Generate Spotify Token" )
		print( e )
		return False

def RefreshSpotifyTokenIfNecessary( redis_connection ):
	try:
		try:
			spotify_personal = redis_connection.get( "PERSONAL.SPOTIFY" )
			spotify_personal = json.loads( spotify_personal )
		except Exception as e:
			print( "No Spotify Personal Info Saved to Redis" )
			print( e )
			return False
		try:
			spotify_token_info = redis_connection.get( "STATE.SPOTIFY.TOKEN_INFO" )
			spotify_token_info = json.loads( spotify_token_info )
		except Exception as e:
			print( "No Spotify Token Info Saved to Redis" )
			spotify_token_info = {}
		if "seconds_left" not in spotify_token_info:
			spotify_token_info = GenerateSpotifyToken( spotify_personal )
			redis_connection.set( "STATE.SPOTIFY.TOKEN_INFO" , json.dumps( spotify_token_info ) )
			return spotify_token_info

		time_now = int( time.time() )
		spotify_token_info[ "seconds_left" ] = spotify_token_info[ "expire_time" ] - time_now
		if spotify_token_info[ "seconds_left" ] < 300:
			print( "Spotify Token is About to Expire in " + str( spotify_token_info[ "seconds_left" ] ) + " Seconds" )
			spotify_token_info = GenerateSpotifyToken( spotify_personal )
			redis_connection.set( "STATE.SPOTIFY.TOKEN_INFO" , json.dumps( spotify_token_info ) )
			return spotify_token_info
		else:
			print( "Spotify Token is Still Valid for " + str( spotify_token_info[ "seconds_left" ] ) + " Seconds" )
			return spotify_token_info
	except Exception as e:
		print( "Couldn't Regenerate Spotify Token" )
		print( e )
		return False

def get_spotify_token_info():
	try:
		redis_connection = try_to_connect_to_redis()
		if redis_connection == False:
			return False
		spotify_token_info = RefreshSpotifyTokenIfNecessary( redis_connection )
		if spotify_token_info == False:
			return False
		return spotify_token_info
	except Exception as e:
		print( "Couldn't Get Spotify Token Info" )
		print( e )
		return False
