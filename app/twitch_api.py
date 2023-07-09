from flask import Flask, render_template, request
import os
from datetime import datetime

import pandas as pd
import requests
import sqlalchemy as db

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
    access_token = auth_response_data['access_token']
    headers = {
        'Authorization': 'Bearer {token}'.format(token=access_token),
        'Client-Id': CLIENT_ID
    }
    return headers


def get_streamer_data(user_name, headers):
    """
    Returns a dictionary of Twitch user data, given their username
    """
    if not user_name or len(user_name) == 0 or ' ' in user_name:
        return None
    # Requests the user's information and converts to JSON
    streamer_req = requests.get(BASE_URL +
                                '/users?login=' +
                                user_name, headers=headers)
    streamer_data = streamer_req.json()['data']

    if len(streamer_data) != 0:
        twitch_url = 'https://www.twitch.tv/'
        streamer_data = {}
        streamer_data_json = streamer_req.json()['data'][0]

        user_id = streamer_data_json['id']
        streamer_data['id'] = user_id
        streamer_data['login'] = streamer_data_json['login']
        streamer_data['url'] = twitch_url + streamer_data['login']
        streamer_data['name'] = streamer_data_json['display_name']
        streamer_data['description'] = streamer_data_json['description']
        streamer_data['broadcaster_type'] = \
            streamer_data_json['broadcaster_type']
        streamer_data['pfp_url'] = streamer_data_json['profile_image_url']
        # Requests the follower data of the user and stores it in the user data
        followers_req = requests.get(
                                        BASE_URL +
                                        '/channels/followers?broadcaster_id=' +
                                        user_id,
                                        headers=headers)

        streamer_data['follower_count'] = followers_req.json()['total']

        channel_req = requests.get(
                                    BASE_URL +
                                    '/channels?broadcaster_id=' +
                                    user_id,
                                    headers=headers)
        channel_data = channel_req.json()['data'][0]
        streamer_data['last_game_played'] = channel_data['game_name']

        # Requests information on the user's videos
        video_req = requests.get(
                                    BASE_URL +
                                    '/videos?user_id=' +
                                    user_id,
                                    headers=headers)
        streamer_data['video_data'] = video_req.json()['data'][:5]
        for i in range(len(streamer_data['video_data'])):
            vid_date = streamer_data['video_data'][i]['published_at']
            try:
                vid_date = datetime.strptime(vid_date, "%Y-%m-%dT%H:%M:%S.%fZ")
            except ValueError:
                vid_date = datetime.strptime(vid_date, "%Y-%m-%dT%H:%M:%SZ")
            vid_date = vid_date.strftime("%B %d, %Y")
            streamer_data['video_data'][i]['published_at'] = vid_date

        streamer_data['created_at'] = datetime.strptime(
                    streamer_data_json['created_at'], "%Y-%m-%dT%H:%M:%SZ"
                ).strftime("%B %d, %Y")
        return streamer_data
    else:
        return None


def get_active_streamers(headers):
    active_req = requests.get(
                                BASE_URL + '/search/channels?' +
                                'query=gaming&live_only=true',
                                headers=headers)
    active_data = active_req.json()['data']
    active_streamers = []
    for streamer in active_data:
        active_streamers.append(
            get_streamer_data(streamer['broadcaster_login'], headers))
    return active_streamers
