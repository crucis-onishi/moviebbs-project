from apiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.tools import argparser
import pandas as pd
import re # 正規表現
import requests
from xml.etree import ElementTree

import environ

env = environ.Env()
env.read_env('.env')

YOUTUBE_API_KEY = env('YOUTUBE_API_KEY')

YOUTUBE_API_SERVICE_NAME = 'youtube'

def get_movie_platform(url):
    youtube_pattern = r"(?:https?:\/\/)?(?:www\.)?(?:youtube\.com|youtu\.be)"
    niconico_pattern = r"(?:https?:\/\/)?(?:www\.)?(?:niconico\.jp|nicovideo\.jp)"

    if re.search(youtube_pattern, url):
        return "youtube"
    elif re.search(niconico_pattern, url):
        return "niconico"
    else:
        return None

def get_movie_id(movie_url):
    youtube_match = re.search(r'\?v=([^&]+)', movie_url)
    niconico_match = re.search(r'watch/(\w+)', movie_url)

    if youtube_match:
        movie_id = youtube_match.group(1)
    elif niconico_match:
        movie_id = niconico_match.group(1)
    else:
        movie_id = 'OgYWssWn7uQ'

    return movie_id

def get_movie_meta(movie_id, movie_platform):
    if movie_platform == "youtube":
        youtube = build(YOUTUBE_API_SERVICE_NAME, 'v3', developerKey = YOUTUBE_API_KEY)
        videos_response = youtube.videos().list(part='snippet,statistics', id='{},'.format(movie_id)).execute()

        # snippet
        snippetInfo = videos_response["items"][0]["snippet"]

        # 動画のメタ情報
        movie_title = snippetInfo['title']
        channel_title = snippetInfo['channelTitle']
        movie_description = snippetInfo['description']

    elif movie_platform == "niconico":
        url = f'http://ext.nicovideo.jp/api/getthumbinfo/{movie_id}'
        response = requests.get(url)
        tree = ElementTree.fromstring(response.content)
        status = tree.attrib['status']

        if status is not None and status == 'ok':
            movie_title_element = tree.find('./thumb/title')
            channel_title_element = tree.find('./thumb/user_nickname')
            movie_description_element = tree.find('./thumb/description')
            movie_title = movie_title_element.text if movie_title_element is not None else "Error: Could not retrieve video title"
            channel_title = channel_title_element.text if channel_title_element is not None else "Error: Could not retrieve channel title"
            movie_description = movie_description_element.text if movie_description_element is not None else "Error: Could not retrieve video description"
        else:
            movie_title = "Error: Could not retrieve video title"
            channel_title = "Error: Could not retrieve channel title"
            movie_description = "Unknown Description"
    else:
        movie_title = "Unknown Title"
        channel_title = "Unknown Channel"

    movie_meta = {
    'movie_title': movie_title,
    'channel_title': channel_title,
    'movie_description': movie_description,
    }

    return movie_meta

def youtube_search(keyword):
    youtube = build(YOUTUBE_API_SERVICE_NAME, 'v3', developerKey = YOUTUBE_API_KEY)
    search_response = youtube.search().list(part = 'id, snippet', q = keyword, maxResults = 10, order = 'viewCount', type = 'video',).execute()

    viewcount_list = []
    title_list = []
    channel_list = []
    thumbnail_list = []
    videoid = []

    for search_result in search_response['items']:
        viewcount = youtube.videos().list(part = 'statistics', id = search_result['id']['videoId']).execute()
        viewcount_list.append(viewcount['items'][0]['statistics']['viewCount'] + '回')
        title_list.append(search_result['snippet']['title'])
        channel_list.append(search_result['snippet']['channelTitle'])
        thumbnail_list.append(search_result['snippet']['thumbnails']['default']['url'])
        videoid.append(search_result['id']['videoId'])


        df = pd.DataFrame({
            'title':title_list,
            'channel':channel_list,
            'viewcount':viewcount_list,
            'thumbnail':thumbnail_list,
            'videoid':videoid
        })

    return df
