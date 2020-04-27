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
import spotipy
import requests

import redis_utils

# def GenerateSpotifyToken( options ):
# 	try:
# 		print("Generating Spotify Token")
# 		print( options )
# 		data = st.start_session( options[ "username" ] , options[ "password" ] )
# 		access_token = data[ 0 ]
# 		seconds_left = data[ 1 ] - int( time.time() )
# 		result = {
# 			"access_token": access_token ,
# 			"expire_time": data[ 1 ] ,
# 			"seconds_left": seconds_left
# 		}
# 		return result
# 	except Exception as e:
# 		print("Couldn't Generate Spotify Token")
# 		print( e )
# 		return False

# https://developer.spotify.com/documentation/general/guides/authorization-guide/#client-credentials-flow
# https://developer.spotify.com/documentation/general/guides/scopes/
def GenerateSpotifyToken( options ):
	try:
		headers = {
			'Authorization': f"Basic {options[ 'base64_clientid_clientsecret' ]}" ,
		}
		data = {
			'grant_type': 'client_credentials' ,
			#'scope': 'streaming app-remote-control'
			'scope': 'ugc-image-upload user-read-playback-state user-modify-playback-state user-read-currently-playing streaming app-remote-control user-read-email user-read-private playlist-read-collaborative playlist-modify-public playlist-read-private playlist-modify-private user-library-modify user-library-read user-top-read user-read-playback-position user-read-recently-played user-follow-read user-follow-modify'
		}
		response = requests.post( 'https://accounts.spotify.com/api/token' , headers=headers , data=data )
		token_info = response.json()
		print( token_info )
		expire_time = int( time.time() ) + token_info[ "expires_in" ]
		result = {
			"access_token": token_info[ "access_token" ] ,
			"expire_time": expire_time ,
			"seconds_left": token_info[ "expires_in" ]
		}
		return result
	except Exception as e:
		print("Couldn't Generate Spotify Token")
		print( e )
		return False

def RefreshSpotifyTokenIfNecessary():
	try:
		redis_connection = redis_utils.try_to_connect_to_redis()
		if redis_connection == False:
			return False
		try:
			spotify_personal = redis_connection.get( "PERSONAL.SPOTIFY" )
			spotify_personal = json.loads( spotify_personal )
		except Exception as e:
			print("No Spotify Personal Info Saved to Redis")
			print( e )
			return False
		try:
			spotify_token_info = redis_connection.get( "STATE.SPOTIFY.TOKEN_INFO" )
			spotify_token_info = json.loads( spotify_token_info )
		except Exception as e:
			print( "No Spotify Token Info Saved to Redis" )
			spotify_token_info = {}
		if spotify_token_info == False or None:
			spotify_token_info = {}
		if "seconds_left" not in spotify_token_info:
			print("seconds_left is not in spotify_token_info")
			spotify_token_info = GenerateSpotifyToken( spotify_personal )
			print( spotify_token_info )
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
		spotify_token_info = RefreshSpotifyTokenIfNecessary()
		print( spotify_token_info )
		if spotify_token_info == False:
			return False
		return spotify_token_info
	except Exception as e:
		print( "Couldn't Get Spotify Token Info" )
		print( e )
		return False
