import pandas as pd 
from youtube import Channel



# Dictionary of channel names and their channel IDs
channels = {
    'BicycleDutch': 'UC67YlPrRvsO117gFDM7UePg',
    'CityNerd': 'UCfgtNfWCtsLKutY-BHzIb9Q',
    'City Beautiful': 'UCGc8ZVCsrR3dAuhvUbkbToQ',
    'Not Just Bikes': 'UC0intLFzLaudFG-xAvUEO-A',
    'RMTransit': 'UCf4iKXL_SJQ5d0qsKkboRRQ'
}

# Create empty dataframes to store information
channel_stats = pd.DataFrame()
video_stats = pd.DataFrame()

# Iterate over each channel ID
for channel_id in channels.values():
    # Create an instance of the Channel object for each channel ID
    channel = Channel(channel_id)
    # Append the respective information to the above dataframes
    channel_stats = pd.concat([channel_stats, channel.channel_stats])
    video_stats = pd.concat([video_stats, channel.video_stats])

# Preview the resulting dataframes
print(channel_stats.head())
print(video_stats.head())