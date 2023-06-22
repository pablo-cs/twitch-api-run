import requests
import twitchAPI
import os
from datetime import datetime
import sqlalchemy as db
import pandas as pd

CLIENT_ID = os.environ.get('TWITCH_CLIENT_ID')
CLIENT_SECRET = os.environ.get('TWITCH_CLIENT_SECRET')

## Authentication Set-up
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

##Setup engine for SQL interaction
engine = db.create_engine('sqlite:///users.db')

##Asks user to input username of a Twitch account
user_name = ''

user_data_list = []##Used to create list of user data

while True:
  user_name = input('Enter username to search and add or QUIT: ')
  if user_name.upper() == 'QUIT':
    break

  ##Requests the user's information and converts to json
  user_req = requests.get(BASE_URL + '/users?login=' + user_name, headers=headers)
  user_data = user_req.json()['data']
  
    
  ##Checks if user was found, if not then their data list would be empty
  if len(user_data) != 0:
    print('------------------')
    user_data = user_req.json()['data'][0]
    user_data_list.append(user_data)

    user_id = user_data['id']
    
    ##Requests the follower data of the user and stores in the user data
    followers_req = requests.get(BASE_URL + '/channels/followers?broadcaster_id=' + user_id, headers=headers)
    user_data['follower_count'] = followers_req.json()['total']

    ##Prints out the informations on the user
    print("User found!")
    print("Name:", user_data['display_name'])
    print("Description:", user_data['description'])
    print("Follower count:", format(user_data['follower_count'],","))
    print("Broadcaster Type:", user_data['broadcaster_type'])
    print("Member since:", datetime.strptime(user_data['created_at'], "%Y-%m-%dT%H:%M:%SZ").strftime("%B %d, %Y"))
    print("Most recent videos - ")
    
    ##Requests information on the user's videos
    video_req = requests.get(BASE_URL + '/videos?user_id=' + user_id, headers=headers)
    video_data = video_req.json()['data']
    
    ##Prints out information on the 5 (at most) most recent videos
    i = 0
    while i < 5 and i < len(video_data):
      curr_vid = video_data[i]
      print("Title:", curr_vid['title'])
      #print("Posted:", datetime.strptime(curr_vid['published_at'], "%Y-%m-%dT%H:%M:%SZ").strftime("%B %d, %Y"))
      print("Views:", format(curr_vid['view_count'],","))
      i+=1
    print('------------------')
  else:
    print("User not found :(")

if len(user_data_list) > 0:
  print('Here are all the streamers you added')
  #Creates dataframes and SQL stuff using list of users dictionaries
  df = pd.DataFrame(user_data_list)
  df.to_sql('users', con=engine, if_exists='replace', index=False)

  with engine.connect() as connection:
        query_result = connection.execute(db.text("SELECT display_name, broadcaster_type, follower_count, created_at FROM users;")).fetchall()
        print(pd.DataFrame(query_result))
print('Bye!')


