import csv
from pathlib import Path
from pprint import pprint
import requests
from utils.auth import authorization
from utils.playlist import get_playlist_id

URL = "https://www.googleapis.com/youtube/v3/playlistItems"
BASE_DIR = Path(__file__).resolve().parent

def get_video_list(token: str = authorization().token ):
    """
    Makes request to YouTube data api

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
    return data


def to_update_video_list():
    """
        Takes the video list, checks videos.csv to check last updated video and updates csv if needed.

        Returns:
            list of videos that need to be updated with AI.
    """

    vid_data = get_video_list()
    vid_list = [video['snippet']['resourceId']['videoId'] for video in vid_data['items']]

    csv_path = BASE_DIR / "./videos.csv"

    #reading csv
    with open(csv_path, 'r') as f:
        reader = csv.reader(f)
        next(reader)  # SKIP HEADER
        for row in reader:
            last_video_id = row[0]
    for i, video_id in enumerate(vid_list):
        if video_id == last_video_id and i != 0:
            return vid_list[:i]
    return None

def to_update_video_data() -> list[dict[str, str]] | None:
    """
    Returns:
        final dictionary of videos to be updated by AI.
    """

    vid_list = to_update_video_list()
    vid_data = get_video_list()


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
        return None
    return final_data_list



if __name__ == "__main__":
    print(to_update_video_list())
    print(to_update_video_data())
    # print(len(to_update_video_list()))
    pprint(get_video_list())
    # BrasOb-Vh-s