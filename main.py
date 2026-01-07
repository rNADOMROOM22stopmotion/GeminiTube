from pprint import pprint
import requests
from utils.auth import authorization
from models import VideoBody, Snippet, Status
from utils.videos import to_update_video_data

print(to_update_video_data())

# token = authorization().token
# url = "https://www.googleapis.com/youtube/v3/videos"
# header = {
#         "Authorization": f"Bearer {token}"
#     }
# parameters = {
#         "part" : "snippet, status",
#         "maxResults": 50,
#     }
# body = VideoBody(id="IiFG1Lupq10",
#                 snippet=Snippet(title="sample title",
#                                 description="hahahhahaha #peter",
#                                 tags=["hello", "peter", "horse", "food"]),
#                  status=Status()
#                  ).model_dump()
# print(body)
# response = requests.put(url= url, headers=header, params=parameters,json=body)
# print(response.json())
