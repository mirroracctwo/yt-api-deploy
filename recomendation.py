from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import os
from dotenv.main import load_dotenv
load_dotenv()
import requests



def search_youtube_playlists(query,count):
    try:
        # Build the YouTube Data API client
        youtube = build('youtube', 'v3', developerKey=os.environ['yt_api_key'])

        # Search for playlists matching the query
        search_response = youtube.search().list(
            q=query,
            type='playlist',
            part='id',
            maxResults=count
        ).execute()

        # Get the URLs of the matching playlists
        playlist_ids = [result['id']['playlistId'] for result in search_response['items']]
        
        data_res = []
        for j in playlist_ids:
            
            playlist_request = youtube.playlists().list(
                part='snippet, contentDetails',
                id=j
            )
            playlist_response = playlist_request.execute()
            
            title = playlist_response['items'][0]['snippet']['title']
            video_count = playlist_response['items'][0]['contentDetails']['itemCount']
            try:
                thumbnail_link = playlist_response['items'][0]['snippet']['thumbnails']['maxres']['url']
            except:
                thumbnail_link = playlist_response['items'][0]['snippet']['thumbnails']['default']['url']

#             discription = playlist_response['items'][0]['snippet']['localized']['description']
            data = {"play_id":j,"title":title,"videoCount":video_count,"thumbnail_link":thumbnail_link}
            data_res.append(data)
        
        return data_res

    except HttpError as e:
        print('An error occurred: %s' % e)
        return None

def get_playlist_videos(playlist_id,count):
    # Set up the YouTube API client
    youtube = build('youtube', 'v3', developerKey=os.environ['yt_api_key'])

    # Retrieve the playlist items
    request = youtube.playlistItems().list(
        part="snippet",
        playlistId=playlist_id,
        maxResults=count
    )
    response = request.execute()

    # Process the playlist items to extract the video information
    videos = []
    for item in response["items"]:
        video = {
            "id": item["snippet"]["resourceId"]["videoId"],
            "title": item["snippet"]["title"],
            "views": 0,
            "thumbnails": item["snippet"]["thumbnails"]["maxres"]["url"]
        }

        # Retrieve the video statistics to get the view count
        stats_request = youtube.videos().list(
            part="statistics",
            id=video["id"]
        )
        stats_response = stats_request.execute()
        if "items" in stats_response:
            video["views"] = int(stats_response["items"][0]["statistics"]["viewCount"])

        videos.append(video)

    return videos
