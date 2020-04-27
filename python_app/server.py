import os
import redis
import json
import time

from sanic import Sanic
from sanic.response import json as sanic_json
from sanic import response

from api.api_blueprint import api_blueprint
from commands.commands_blueprint import commands_blueprint

from generic_utils import save_personal_file_to_redis
save_personal_file_to_redis()

# https://github.com/huge-success/sanic/tree/master/examples
# https://github.com/huge-success/sanic/blob/master/examples/try_everything.py

# https://sanic.readthedocs.io/en/latest/sanic/blueprints.html

app = Sanic( name="Spotify API Server" )

@app.route( "/" )
def hello( request ):
	return response.text( "You Found the Spotify API Server!\n" )

@app.route( "/ping" )
def ping( request ):
	return response.text( "pong\n" )

app.blueprint( api_blueprint )
app.blueprint( commands_blueprint )

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

def get_config( redis_connection ):
	try:
		try:
			config = redis_connection.get( "CONFIG.SPOTIFY_API_SERVER" )
			config = json.loads( config )
			return config
		except Exception as e:
			config_path = os.path.join( os.path.dirname( os.path.abspath( __file__ ) ) , "config.json" )
			with open( config_path ) as f:
				config = json.load( f )
			redis_connection.set( "CONFIG.SPOTIFY_API_SERVER" , json.dumps( config ) )
			return config
	except Exception as e:
		print( "Could't Find Spotify API Server Config in Redis or Local JSON File" )
		print( e )
		return False

def run_server():
	try:

		redis_connection = try_to_connect_to_redis()
		if redis_connection == False:
			return False
		config = get_config( redis_connection )
		if config == False:
			return False

		host = '0.0.0.0'
		port = config[ 'spotify_api_server' ][ 'port' ]
		app.run( host=host , port=port )

	except Exception as e:
		print( "Couldn't Start Spotify API Server" )
		print( e )
		return False

def try_run_block( options ):
	for i in range( options[ 'number_of_tries' ] ):
		attempt = options[ 'function_reference' ]()
		if attempt is not False:
			return attempt
		print( f"Couldn't Run '{ options[ 'task_name' ] }', Sleeping for { str( options[ 'sleep_inbetween_seconds' ] ) } Seconds" )
		time.sleep( options[ 'sleep_inbetween_seconds' ] )
	if options[ 'reboot_on_failure' ] == True:
		os.system( "reboot -f" )

try_run_block({
	"task_name": "Spotify API Server" ,
	"number_of_tries": 5 ,
	"sleep_inbetween_seconds": 5 ,
	"function_reference": run_server ,
	"reboot_on_failure": True
	})
