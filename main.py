import pandas as pd 
from config import channels
from youtube import Channel



channel_stats = pd.DataFrame()
video_stats = pd.DataFrame()

for channel_id in channels.values():
    channel = Channel(channel_id)
    channel_stats = pd.concat([channel_stats, channel.channel_stats])
    video_stats = pd.concat([video_stats, channel.video_stats])

print(channel_stats.head())
print(video_stats.head())