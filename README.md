Before doing anything:

1. Clone repository and install requirements.
2. make a .env file and add your GEMINI_API_KEY


Simple usage guide:

1. Make a folder "tokens" and add oauth2 tokens inside oauth.json file inside this folder.
2. Get hold of a youtube video id. You may use the get_video_list() function located in utils/videos.py.
   This acutally returns video_id_list (used by other functions) and data. Here, data basically contains the API reponse. This will contain 50 items/ videos.
3. Choose any video from these 50. Copy that video's ID inside utils/video.csv below "lastvideoid". All the videos above this video will be updated.
4. Note that this is only temporary. Whenever you upload new videos and run this script videos.csv will be auto updated.
5. Next, run the main.py file.
