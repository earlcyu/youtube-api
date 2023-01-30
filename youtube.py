import os
import re
import pandas as pd
from googleapiclient.discovery import build



class Channel:
    '''
    A class that represents a YouTube channel

    Attributes
    ----------
    channel_id : str
        A unique string identifier for a channel
    
    channel_stats : pd.DataFrame
        A single-line dataframe with the channel's information 
        and high-level statistics as its columns
    
    uploads_id : str
        A unique string identifier for the channel's uploads ID
    
    video_ids : list
        A list of video IDs the channel has published
    
    video_stats : pd.DataFrame
        A dataframe of videos and their details the channel has published

    Methods
    -------
    _clean_string(self, column_name:str):
        Removes prefixes and converts the string to snake_case
    
    _clean_columns(columns: list)
        Applies the _clean_string() function to a given list of strings
    
    get_channel_stats()
        Returns a single-line dataframe with the channel's information 
        and high-level statistics as its columns
    
    get_video_ids()
        Returns a list of the channel's video IDs, which are used as input 
        for `get_video_stats()`
    
    get_video_stats()
        Returns a dataframe of videos and their details the channel 
        has published
    '''
    
    def __init__(self, channel_id: str) -> None:
        self.channel_id = channel_id 
        self.youtube = build(
            'youtube', 
            'v3', 
            developerKey=os.environ['YOUTUBE_API_KEY']
        )
        # List of prefixes to remove in cleaning column names
        self.prefixes = ['snippet.', 'contentDetails.', 'statistics.']
        # RegEx pattern to help convert camelCase to snake_case
        self.pattern = re.compile(r'(?<!^)(?=[A-Z])')
        # Instantiate the following methods upon creating a class
        self.get_channel_stats()
        self.get_video_ids()
        self.get_video_stats()

    def _clean_string(self, column_name:str):
        '''Removes prefixes and converts the string to snake_case'''
        for prefix in self.prefixes:
            column_name = column_name.replace(prefix, '') 
        return self.pattern.sub('_', column_name).lower().replace('.', '_') 
    
    def _clean_columns(self, column_names:list):
        '''Applies the _clean_string() function to a given list of strings'''
        return list(map(self._clean_string, column_names))

    def get_channel_stats(self):
        '''Returns a single-line dataframe with the channel's information 
        and high-level statistics as its columns'''
        request = self.youtube.channels().list(
            part='snippet,contentDetails,statistics',
            id=self.channel_id
        )
        response = request.execute()
        self.channel_stats = pd.json_normalize(response['items'][0])
        self.channel_stats.columns = self._clean_columns(
            self.channel_stats.columns
        )
        self.uploads_id = self.channel_stats.loc[0,'related_playlists_uploads']

    def get_video_ids(self):
        '''Returns a list of the channel's video IDs, which are used as input 
        for `get_video_stats()`'''
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
        '''Returns a dataframe of videos and their details the channel 
        has published'''
        self.video_stats = pd.DataFrame()
        
        for video_id_index in range(0, len(self.video_ids), 50):
            request = self.youtube.videos().list(
                part='snippet,contentDetails,statistics',
                id=','.join(self.video_ids[video_id_index:video_id_index+50])
            )
            response = request.execute()
            self.video_stats = pd.concat(
                [self.video_stats, pd.json_normalize(response['items'][0])]
            )
        
        self.video_stats.columns = self._clean_columns(self.video_stats.columns)
