from flask import Flask, request, jsonify, render_template
from recomendation import search_youtube_playlists , get_playlist_videos
import os
from dotenv.main import load_dotenv
from flask_caching import Cache
load_dotenv()
from flask_cors import CORS

app = Flask(__name__)
CORS(app, origins='*')

cache = Cache(app, config={'CACHE_TYPE': 'simple', 'CACHE_DEFAULT_TIMEOUT': 3600})  # Cache timeout set to 1 hour (3600 seconds)

valid_api_keys = {os.environ['api_key_for_api']: True}


def make_cache_key(*args, **kwargs):
    # Custom cache key function based on API key and keyword
    api_key = request.args.get('api_key', 'default')
    keyword = request.args.get('keyword', 'default')
    count = request.args.get('count','default')
    return f"{api_key}:{keyword}:{count}"

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/api/yt_play_recom')
@cache.cached(timeout=3600, key_prefix=make_cache_key)
def yt_play_recom():
    api_key = request.args.get('api_key')
    if api_key not in valid_api_keys:
        return jsonify({'error': 'Invalid API key'})
    keyword = request.args.get('keyword')
    count = request.args.get('count')
    # Call your function with the parameters and get the list
    result = search_youtube_playlists(keyword, int(count))
    # Return the list as JSON
    return jsonify(result)

@app.route('/api/all_vid_of_play')
@cache.cached(timeout=3600, key_prefix=make_cache_key)
def all_vid_of_play():
    api_key = request.args.get('api_key')
    if api_key not in valid_api_keys:
        return jsonify({'error': 'Invalid API key'})
    keyword = request.args.get('playlist_id')
    count = request.args.get('count')
    # Call your function with the parameters and get the list
    result = get_playlist_videos(keyword,int(count))
    # Return the list as JSON
    return jsonify(result)



if __name__ == '__main__':
    app.run()

    
