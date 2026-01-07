from pprint import pprint
import requests
from utils.auth import authorization
CHANNEL_URL = "https://www.googleapis.com/youtube/v3/channels"


def get_playlist_id(url: str = CHANNEL_URL, token: str = authorization().token ) -> str:
    header = {
        "Authorization": f"Bearer {token}"
    }

    parameters = {
        "part" : "contentDetails",
        "maxResults": 50,
        "mine": True,
    }
    response = requests.get(url, headers=header, params=parameters)
    data = response.json()
    #pprint(data)
    return data['items'][0]['contentDetails']['relatedPlaylists']['uploads']
