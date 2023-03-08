from apiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.tools import argparser
import pandas as pd
import re # 正規表現

import environ

env = environ.Env()
env.read_env('.env')

YOUTUBE_API_KEY = env('YOUTUBE_API_KEY')

YOUTUBE_API_SERVICE_NAME = 'youtube'

def get_movie_id(movie_url):
    match = re.search(r'\?v=([^&]+)', movie_url)
    if match:
        movie_id = match.group(1)
        return movie_id
    else:
        return 'OgYWssWn7uQ'

def get_movie_meta(movie_id):

    youtube = build(YOUTUBE_API_SERVICE_NAME, 'v3', developerKey = YOUTUBE_API_KEY)
    videos_response = youtube.videos().list(part='snippet,statistics', id='{},'.format(movie_id)).execute()

    # snippet
    snippetInfo = videos_response["items"][0]["snippet"]
    # 動画タイトル
    movie_title = snippetInfo['title']
    # チャンネル名
    channeltitle = snippetInfo['channelTitle']

    # 再生プレーヤー
    movie_player = '<iframe width="560" height="315" src="https://www.youtube.com/embed/{}" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>'.format(movie_id)

    movie_meta = {
    'movie_title': movie_title,
    'channeltitle': channeltitle,
    'movie_player': movie_player,
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
