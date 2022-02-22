import dash
from flask import Flask
from flask_caching import Cache

app = dash.Dash(__name__, suppress_callback_exceptions=True)

# theme = {
#     'dark': True,
#     'detail': '#007439',
#     'primary': '#00EA64',
#     'secondary': '#6E6E6E',
# }

server = app.server

# initiate cache
CACHE_CONFIG = {
    # try 'FileSystemCache' if you don't want to setup redis
    #   'CACHE_TYPE': 'redis',
    #   'CACHE_REDIS_URL': os.environ.get('REDIS_URL', 'redis://localhost:6379')
    'CACHE_TYPE': 'filesystem',
    'CACHE_DIR': 'cachestore',
    'CACHE_DEFAULT_TIMEOUT': 3600,
}
cache = Cache()
cache.init_app(server, config=CACHE_CONFIG)
#   print("AF init_app()")


