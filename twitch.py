import requests
import twitchAPI
import os
from datetime import datetime

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
access_token = auth_response_data['access_token']

headers = {'Authorization': 'Bearer {token}'.format(token=access_token),
          'Client-Id': CLIENT_ID}
BASE_URL = 'https://api.twitch.tv/helix'
user_name = ''
while True:
  user_name = input('Enter username to search or QUIT: ')
  if user_name.upper() == 'QUIT':
    break
  user_req = requests.get(BASE_URL + '/users?login=' + user_name, headers=headers)
  user_data = user_req.json()['data']
  
  if len(user_data) != 0:
    print('------------------')
    user_data = user_req.json()['data'][0]
    user_id = user_data['id']
    followers_req = requests.get(BASE_URL + '/channels/followers?broadcaster_id=' + user_id, headers=headers)
    followers_data = followers_req.json()
    print("User found!")
    print("Name:", user_data['display_name'])
    print("Description:", user_data['description'])
    print("Follower count:", format(followers_data['total'],","))
    print("Broadcaster Type:", user_data['broadcaster_type'])
    print("Member since:", datetime.strptime(user_data['created_at'], "%Y-%m-%dT%H:%M:%SZ").strftime("%B %d, %Y"))
    print("Most recent videos - ")
    video_req = requests.get(BASE_URL + '/videos?user_id=' + user_id, headers=headers)
    video_data = video_req.json()['data']
    i = 0
    while i < 5 and i < len(video_data):
      curr_vid = video_data[i]
      print("Title:", curr_vid['title'])
      print("Posted:", datetime.strptime(curr_vid['published_at'], "%Y-%m-%dT%H:%M:%SZ").strftime("%B %d, %Y"))
      print("Views:", format(curr_vid['view_count'],","))
      i+=1
    print('------------------')
  else:
    print("User not found :(")
print('Bye!')
