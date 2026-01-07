from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import os
import pickle
from pathlib import Path


def authorization():
    credentials = None

    BASE_DIR = Path(__file__).resolve().parent
    token_path = BASE_DIR / '../tokens/token.pickle'
    auth_path = BASE_DIR / '../tokens/oauth.json'

    token_path = token_path.resolve()
    auth_path = auth_path.resolve()


    if os.path.exists(token_path):
        #print('Loading Credentials From File...')
        with open(token_path, 'rb') as token:
            credentials = pickle.load(token)

    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            #print('Refreshing Access Token...')
            credentials.refresh(Request())
        else:
            print('Fetching New Tokens...')
            flow = InstalledAppFlow.from_client_secrets_file(
                client_secrets_file = auth_path.__str__(),
                scopes=[
                    'https://www.googleapis.com/auth/youtube.force-ssl',
                    'https://www.googleapis.com/auth/youtube.upload',
                    'https://www.googleapis.com/auth/youtube',
                    'https://www.googleapis.com/auth/youtube.readonly',
                    'https://www.googleapis.com/auth/youtubepartner'
                ]
            )

            flow.run_local_server(authorization_prompt_message='')
            credentials = flow.credentials

            # Save the credentials for the next run
            with open(token_path, 'wb') as f:
                print('Saving Credentials for Future Use...')
                pickle.dump(credentials, f)
    return credentials

