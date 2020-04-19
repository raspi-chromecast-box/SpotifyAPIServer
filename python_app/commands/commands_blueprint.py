from sanic import Blueprint
from sanic.response import json
from sanic import response

from spotify_token_util import get_spotify_token_info

commands_blueprint = Blueprint( 'commands_blueprint' , url_prefix='/commands' )

@commands_blueprint.route( '/' )
def commands_root( request ):
	return response.text( "you are at the /commands url\n" )

@commands_blueprint.route( '/play' )
def play( request ):
	#return response.text( "you are at the /commands url\n" )
	return json({'my': 'blueprint'})

@commands_blueprint.route( '/play_currated' )
def play_currated( request ):
	#return response.text( "you are at the /commands url\n" )
	return json({'my': 'blueprint'})

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

