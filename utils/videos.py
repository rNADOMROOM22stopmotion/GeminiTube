import csv
from pathlib import Path
from pprint import pprint
from typing import Any

import requests
from utils.auth import authorization
from utils.playlist import get_playlist_id

URL = "https://www.googleapis.com/youtube/v3/playlistItems"

def get_video_list(token: str = authorization().token ):
    """
    Makes request to youtube data api

    Returns:
        list of recently uploaded 50 videos, their data
    """
    url = URL


    header = {
        "Authorization": f"Bearer {token}"
    }
    parameters = {
        "part" : ["snippet"],
        "maxResults": 50,
        "playlistId" : get_playlist_id(url="https://www.googleapis.com/youtube/v3/channels")
    }
    response = requests.get(url, headers=header, params=parameters)
    data = response.json()
    #pprint(data)
    video_id_list = []
    for video in data['items']:
        video_id_list.append(video['snippet']['resourceId']['videoId'])
    return video_id_list, data


def to_update_video_list():
    """
        Takes the video list, checks videos.csv to check last updated video and updates csv if needed.

        Returns:
            list of videos that need to be updated with AI.
    """
    vid_list = get_video_list()[0]

    BASE_DIR = Path(__file__).resolve().parent
    csv_path = BASE_DIR / "./videos.csv"

    with open(csv_path, 'r') as f:
        reader = csv.reader(f)
        next(reader)  # SKIP HEADER
        for row in reader:
            last_video_id = row[0]
    for i, video_id in enumerate(vid_list):
        if video_id == last_video_id and i != 0:
            #updating csv
            rows = [
                ['lastvideoid'],
                [vid_list[0]]
            ]
            with open(csv_path, 'w') as f:
                writer = csv.writer(f)
                writer.writerows(rows)
            return vid_list[:i]
    return None

def to_update_video_data() -> dict[str, str] | list[Any]:
    """
    Returns:
        final dictionary of videos to be updated by AI.
    """

    vid_list = to_update_video_list()
    vid_data = get_video_list()[1]


    data_list = vid_data['items']
    try:
        final_data_list = []
        list_len = len(vid_list)  # 2
        sliced_data_list = data_list[:list_len]
        #pprint(sliced_data_list)
        for video in sliced_data_list:
            vid_dict = {}
            vid_dict['id'] = video['snippet']['resourceId']['videoId']
            vid_dict['title'] = video['snippet']['title']
            vid_dict['description'] = video['snippet']['description']
            final_data_list.append(vid_dict)
    except TypeError:
        return {"message": "video already up to date"}
    return final_data_list



if __name__ == "__main__":
    print(to_update_video_data())
    # BrasOb-Vh-s