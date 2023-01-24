import re
import pandas as pd
from googleapiclient.discovery import build
from config import api_key, channels



class Channel():
    def __init__(self, channel_id) -> None:
        self.channel_id = channel_id 
        self.youtube = build('youtube', 'v3', developerKey=api_key)
        self.pattern = re.compile(r'(?<!^)(?=[A-Z])')
        self.get_channel_stats()
        self.get_video_ids()
        self.get_video_stats()
    
    def _make_snake_case(self, name:str):
        '''Converts a string in camelCase to snake_case'''
        return self.pattern.sub('_', name).lower().replace('.', '_')
    
    def _clean_columns(self, columns:list):
        '''Converts a list of snakeCase strings into snake_case'''
        return list(map(self._make_snake_case, columns))

    def get_channel_stats(self):
        '''Returns a single-line dataframe with the channel's information and high-level statistics as its columns'''
        request = self.youtube.channels().list(
            part='snippet,contentDetails,statistics',
            id=self.channel_id
        )
        response = request.execute()
        self.channel_stats = pd.json_normalize(response['items'][0])
        self.channel_stats.columns = self._clean_columns(self.channel_stats.columns)
        self.uploads_id = self.channel_stats.loc[0,'content_details_related_playlists_uploads']

    def get_video_ids(self):
        '''Returns a list of the channel's video IDs, which are used as input for `function_name`'''
        self.video_ids = []
        
        request = self.youtube.playlistItems().list(
            part='snippet,contentDetails',
            playlistId=self.uploads_id,
            maxResults=50
        )
        response = request.execute()
        
        for video in response['items']:
            self.video_ids.append(video['contentDetails']['videoId'])
        next_page_token = response.get('nextPageToken')
        
        while next_page_token is not None:
            request = self.youtube.playlistItems().list(
                part='snippet,contentDetails',
                playlistId=self.uploads_id,
                maxResults=50,
                pageToken=next_page_token
            )
            response = request.execute()
            for video in response['items']:
                self.video_ids.append(video['contentDetails']['videoId'])
            next_page_token = response.get('nextPageToken')

    def get_video_stats(self):
        '''Returns a dataframe of videos and their details the channel has published'''
        self.video_stats = pd.DataFrame()
        
        for video_id_index in range(0, len(self.video_ids), 50):
            request = self.youtube.videos().list(
                part='snippet,contentDetails,statistics',
                id=','.join(self.video_ids[video_id_index:video_id_index+50])
            )
            response = request.execute()
            self.video_stats = pd.concat([self.video_stats, pd.json_normalize(response['items'][0])])
        
        self.video_stats.columns = self._clean_columns(self.video_stats.columns)
