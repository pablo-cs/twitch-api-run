import requests
import twitchAPI
import os

CLIENT_ID = os.environ.get('TWITCH_CLIENT_ID')
CLIENT_SECRET = os.environ.get('TWITCH_CLIENT_SECRET')

AUTH_URL = 'https://id.twitch.tv/oauth2/token'

auth_response = requests.post(AUTH_URL, {
    'client_id': CLIENT_ID,
    'client_secret': CLIENT_SECRET,
    'grant_type': 'client_credentials',
})
auth_response_data = auth_response.json()
print(auth_response_data)