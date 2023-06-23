import os
from datetime import datetime

import pandas as pd
import requests
import sqlalchemy as db
import twitchAPI

CLIENT_ID = os.environ.get('TWITCH_CLIENT_ID')
CLIENT_SECRET = os.environ.get('TWITCH_CLIENT_SECRET')
AUTH_URL = 'https://id.twitch.tv/oauth2/token'
BASE_URL = 'https://api.twitch.tv/helix'


def generate_headers():
    # Authentication Set-up
    auth_response = requests.post(AUTH_URL, {
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'grant_type': 'client_credentials',
    })

    auth_response_data = auth_response.json()
    print(auth_response_data)
    access_token = auth_response_data['access_token']
    headers = {
        'Authorization': 'Bearer {token}'.format(token=access_token),
        'Client-Id': CLIENT_ID
    }
    return headers


def get_user_data(user_name, headers):
    if len(user_name) == 0 or ' ' in user_name:
        return None
    # Requests the user's information and converts to JSON
    user_req = requests.get(BASE_URL +
                            '/users?login=' +
                            user_name, headers=headers)
    user_data = user_req.json()['data']

    # Checks if user was found, if not then their data list would be empty
    if len(user_data) != 0:
        print('------------------')
        user_data = user_req.json()['data'][0]

        user_id = user_data['id']

        # Requests the follower data of the user and stores it in the user data
        followers_req = requests.get(BASE_URL +
                                     '/channels/followers?broadcaster_id=' +
                                     user_id, headers=headers)

        user_data['follower_count'] = followers_req.json()['total']

        # Requests information on the user's videos
        video_req = requests.get(BASE_URL +
                                 '/videos?user_id=' +
                                 user_id, headers=headers)
        user_data['video_data'] = video_req.json()['data']

        return user_data
    else:
        return None


def print_info(user_data):
    print('------------------')
    print("User found!")
    print("Name:", user_data['display_name'])
    print("Description:", user_data['description'])
    print("Follower count:", format(user_data['follower_count'], ","))
    print("Broadcaster Type:", user_data['broadcaster_type'])

    created_date = datetime.strptime(
                                user_data['created_at'], "%Y-%m-%dT%H:%M:%SZ"
                                ).strftime("%B %d, %Y")

    print("Member since:", created_date)

    print("Most recent videos - ")

    # Prints out information on the 5 (at most) most recent videos
    i = 0
    while i < 5 and i < len(user_data['video_data']):
        curr_vid = user_data['video_data'][i]
        print("Title:", curr_vid['title'])
        print("Views:", format(curr_vid['view_count'], ","))
        i += 1
    print('------------------')


def print_sql(user_data_list, engine):
    if len(user_data_list) > 0:
        print('Here are all the streamers you added')

        # Creates dataframes and SQL stuff using a list of users' dictionaries
        df = pd.DataFrame(user_data_list)
        df = df.drop('video_data', axis=1)
        df.to_sql('users', con=engine, if_exists='replace', index=False)

        with engine.connect() as connection:
            columns = "display_name, broadcaster_type, follower_count"
            query = "SELECT " + columns + " FROM users;"
            query_result = connection.execute(db.text(query)).fetchall()
            print(pd.DataFrame(query_result))
    print('Bye!')


def main():
    headers = generate_headers()
    # Setup engine for SQL interaction
    engine = db.create_engine('sqlite:///users.db')

    # Asks user to input username of a Twitch account
    user_name = ''

    user_data_list = []  # Used to create a list of user data

    while True:
        user_name = input('Enter username to search and add or QUIT: ')
        if user_name.upper() == 'QUIT':
            break
        user_data = get_user_data(user_name.strip(), headers)
        if user_data:
            user_data_list.append(user_data)
            print_info(user_data)

    print_sql(user_data_list, engine)


if __name__ == '__main__':
    main()
