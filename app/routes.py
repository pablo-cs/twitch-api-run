from flask import Flask, render_template, request
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
engine = db.create_engine('sqlite:///users.db')

def generate_headers():
    """
    This method generates the headers to be used for the
    API calls across the program
    """
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
    """
    Returns a dictionary of Twitch user data, given their username
    """
    if len(user_name) == 0 or ' ' in user_name:
        return None
    # Requests the user's information and converts to JSON
    user_req = requests.get(BASE_URL +
                            '/users?login=' +
                            user_name, headers=headers)
    user_data = user_req.json()['data']

    if len(user_data) != 0:
        user_data = user_req.json()['data'][0]

        user_id = user_data['id']

        # Requests the follower data of the user and stores it in the user data
        followers_req = requests.get(
                                        BASE_URL +
                                        '/channels/followers?broadcaster_id=' +
                                        user_id,
                                        headers=headers)

        user_data['follower_count'] = followers_req.json()['total']

        channel_req = requests.get(
                                    BASE_URL +
                                    '/channels?broadcaster_id=' +
                                    user_id,
                                    headers=headers)
        channel_data = channel_req.json()['data'][0]
        user_data['last_game_played'] = channel_data['game_name']

        # Requests information on the user's videos
        video_req = requests.get(
                                    BASE_URL +
                                    '/videos?user_id=' +
                                    user_id,
                                    headers=headers)
        user_data['video_data'] = video_req.json()['data']

        return user_data
    else:
        return None


def user_to_str(user_data):
    """
    Returns a string represenation of a Twitch user's data,
    given a dictionary
    """
    user_str = "Name: " + user_data['display_name'] + \
        "\nDescription: " + user_data['description'] + \
        "\nFollower count: " + format(user_data['follower_count'], ",") + \
        "\nBroadcaster Type: " + user_data['broadcaster_type'] + \
        "\nMember since: " + datetime.strptime(
        user_data['created_at'], "%Y-%m-%dT%H:%M:%SZ"
    ).strftime("%B %d, %Y") + \
        "\nLast played: " + user_data['last_game_played'] + \
        "\nMost Recent Videos:"

    # Prints out information on the 5 (at most) most recent videos
    i = 0
    while i < 5 and i < len(user_data['video_data']):
        curr_vid = user_data['video_data'][i]
        user_str += "\n\nTitle: " + curr_vid['title'] + \
            "\nViews: " + format(curr_vid['view_count'], ",") + \
            "\nPosted: "
        vid_date = curr_vid['published_at']
        try:
            vid_date = datetime.strptime(vid_date, "%Y-%m-%dT%H:%M:%S.%fZ")
        except ValueError:
            vid_date = datetime.strptime(vid_date, "%Y-%m-%dT%H:%M:%SZ")
        user_str += vid_date.strftime("%B %d, %Y")
        i += 1

    return user_str


def update_sql(user_data_list):
    """"
    Updates the user database to include the streamers
    added to the list of users
    """
    if len(user_data_list) > 0:
        print('Here are all the streamers you added')

        # Creates dataframes and SQL stuff using a list of users' dictionaries
        df = pd.DataFrame(user_data_list)
        df = df.drop('video_data', axis=1)
        df.to_sql('users', con=engine, if_exists='append', index=False)

        with engine.connect() as connection:
            columns = "display_name, broadcaster_type, follower_count"
            query = "SELECT " + columns + " FROM users;"
            query_result = connection.execute(db.text(query)).fetchall()
            print(pd.DataFrame(query_result))
    print('Bye!')


def main():
    headers = generate_headers()
    # Setup engine for SQL interaction

    # Asks user to input username of a Twitch account
    user_name = ''

    user_data_list = []  # Used to create a list of user data

    while True:
        user_name = input('Enter username to search and add or QUIT: ')
        print('------------------')

        if user_name.upper() == 'QUIT':
            break
        user_data = get_user_data(user_name.strip(), headers)
        if user_data:
            print("User found!")
            if user_data not in user_data_list:
                user_data_list.append(user_data)
            print(user_to_str(user_data))
        else:
            print("User not found :(")
        print('------------------')

    update_sql(user_data_list)


if __name__ == '__main__':
    main()
