import csv
from pathlib import Path
from pprint import pprint
import google.oauth2.credentials
import requests
from utils.auth import authorization
from utils.playlist import get_playlist_id



class VideoAPI:
    URL = "https://www.googleapis.com/youtube/v3/playlistItems"
    BASE_DIR = Path(__file__).resolve().parent
    CSV_PATH = BASE_DIR / "./videos.csv"

    def __init__(self, auth_token: google.oauth2.credentials.Credentials):
        self.auth = auth_token

    def get_video_list(self):
        """
        Makes request to YouTube data api

        Returns:
            list of recently uploaded 50 videos, their data
        """
        url = VideoAPI.URL
        header = {
            "Authorization": f"Bearer {self.auth.token}"
        }
        parameters = {
            "part" : ["snippet"],
            "maxResults": 50,
            "playlistId" : get_playlist_id(url="https://www.googleapis.com/youtube/v3/channels")
        }
        response = requests.get(url, headers=header, params=parameters)
        data = response.json()
        return data


    def to_update_video_list(self):
        """
            Takes the video list, checks videos.csv to check last updated video and updates csv if needed.

            Returns:
                list of videos that need to be updated with AI.
        """

        vid_data = self.get_video_list()
        vid_list = [video['snippet']['resourceId']['videoId'] for video in vid_data['items']]


        #reading csv
        with open(VideoAPI.CSV_PATH, 'r') as f:
            reader = csv.reader(f)
            next(reader)  # SKIP HEADER
            for row in reader:
                last_video_id = row[0]
        for i, video_id in enumerate(vid_list):
            if video_id == last_video_id and i != 0:
                return vid_list[:i]
        return None

    def to_update_video_data(self) -> list[dict[str, str]] | None:
        """
        Returns:
            final dictionary of videos to be updated by AI.
        """

        vid_list = self.to_update_video_list()
        vid_data = self.get_video_list()


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

    @staticmethod
    def set_video(video_id: str):
        rows = [
            ['lastvideoid'],
            [video_id]
        ]
        with open(VideoAPI.CSV_PATH, 'w') as f:
            writer = csv.writer(f)
            writer.writerows(rows)




if __name__ == "__main__":
    video_api = VideoAPI(authorization())
    pprint(video_api.to_update_video_data())
    video_api.set_video("BrasOb-Vh-s")
    # BrasOb-Vh-s