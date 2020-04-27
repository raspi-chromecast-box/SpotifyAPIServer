import time
import os
import sys
import json
import pychromecast
from pychromecast import Chromecast
from pychromecast.controllers.spotify import SpotifyController
import spotipy
import general_utils

def play_currated_uris( spotify_token_info , chromecast_output_ip , uris ):
    try:
        cast = Chromecast( chromecast_output_ip )
        cast.wait()
        cast.media_controller.stop()
        #client = spotipy.Spotify( auth=spotify_token_info[ "access_token" ] )
        client = spotipy.Spotify( auth=spotify_token_info[ "access_token" ] )
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

config = generic_utils.get_common_config()
print( config )
uris = config[ "redis_connection" ].srandmember( 'SPOTIFY.CURRATED_URIS.ALL' , 10 )
uris = generic_utils.prepare_random_track_uris( uris )
print( uris )
result = play_currated_uris( config[ "spotify_token_info" ] , config[ "chromecast_output_ip" ] , uris )