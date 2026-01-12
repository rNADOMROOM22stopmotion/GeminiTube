import csv
from datetime import datetime
import json
from pathlib import Path
from pprint import pprint
import requests
from utils.auth import authorization
from AI import gen
from models import VideoBody, Snippet, Status, GeminiOutput, GeminiInput
from utils.videos import to_update_video_data, get_video_list

video_data = to_update_video_data()
# video_data = None
if video_data:
    # --backing up current titles/ desc --
    BASE_DIR = Path(__file__).resolve().parent
    log_path = BASE_DIR / "logged_vid_data"
    csv_path = BASE_DIR / "utils/videos.csv"

    with open(f"{log_path}/change_{datetime.now()}.json", "w", encoding="utf-8") as f:
        json.dump(video_data, f, indent=4, ensure_ascii=False)

    # -- generating new stuff --
    for video in video_data:
        ai_output = gen.ai_video_response(GeminiInput(**video)) # title, description and tags pydantic object
        pprint(ai_output.__dict__)
    # -- updating video
        token = authorization().token
        url = "https://www.googleapis.com/youtube/v3/videos"
        header = {
                 "Authorization": f"Bearer {token}"
             }
        parameters = {
                 "part" : "snippet, status",
                 "maxResults": 50,
             }
        body = VideoBody(id=video["id"],
                         snippet=Snippet(title=ai_output.title,
                                         description=ai_output.description,
                                         tags=ai_output.tags),
                          status=Status()
                          ).model_dump()
        response = requests.put(url= url, headers=header, params=parameters,json=body)
        response_data = response.json()
        pprint(response.json())
        if not response_data.get('error', False):
            # updating csv if theres no error
            rows = [
                ['lastvideoid'],
                [video['id']]
            ]
            with open(csv_path, 'w') as f:
                writer = csv.writer(f)
                writer.writerows(rows)

# vid_list, data = get_video_list()
# pprint(data)