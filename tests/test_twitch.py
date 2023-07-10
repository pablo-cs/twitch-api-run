import unittest
from unittest.mock import patch, Mock
import requests
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Import the twitch_api module from the app package
from app import twitch_api

class TwitchAPITestCase(unittest.TestCase):

    @patch('app.twitch_api.requests.get')
    def test_get_user_data(self, mock_get):
        # Set up the mock responses
        mock_user_response = {
            'data': [{
                'id': '141981764',
                'login': 'twitchdev',
                'display_name': 'TwitchDev',
                'type': '',
                'broadcaster_type': 'partner',
                'description': 'Supporting third-party developers.',
                'profile_image_url': 'n/a',
                'offline_image_url': 'n/a',
                'view_count': 5980557,
                'email': 'not-real@email.com',
                'created_at': '2016-12-14T20:32:28Z',
            }]
        }

        mock_followers_response = {
            'total': 8,
            'data': [
                {
                    'user_id': '11111',
                    'user_name': 'UserDisplayName',
                    'user_login': 'userloginname',
                    'followed_at': '2022-05-24T22:22:08Z',
                }

            ]
        }

        mock_channel_response = {
            'data': [
                {
                    'broadcaster_id': '141981764',
                    'broadcaster_login': 'twitchdev',
                    'broadcaster_name': 'TwitchDev',
                    'broadcaster_language': 'en',
                    'game_id': '509670',
                    'game_name': 'Science & Technology',
                    'title': 'TwitchDev Monthly Update // May 6, 2021',
                    'delay': 0,
                    'tags': ['DevsInTheKnow']
                }
            ]
        }

        # Configure the mock responses
        mock_get.side_effect = [
            Mock(json=Mock(return_value=mock_user_response)),
            Mock(json=Mock(return_value=mock_followers_response)),
            Mock(json=Mock(return_value=mock_channel_response)),
            Mock(json=Mock(return_value={'data': []}))
        ]

        # Call the function under test
        headers = {
            'Authorization': 'Bearer mock_token',
            'Client-Id': 'mock_client_id'
            }

        streamer_data = twitch_api.get_streamer_data('twitchdev', headers)
        print(streamer_data['follower_count'])
        # Assert the expected result
        expected_streamer_data = {
            'id': '141981764',
            'login': 'twitchdev',
            'name': 'TwitchDev',
            'url': 'https://www.twitch.tv/twitchdev',
            'broadcaster_type': 'partner',
            'description': 'Supporting third-party developers.',
            'pfp_url': 'n/a',
            'follower_count': 8,
            'last_game_played': 'Science & Technology',
            'video_data': [],
            'created_at': 'December 14, 2016',
        }

        self.assertEqual(streamer_data, expected_streamer_data)

if __name__ == '__main__':
    unittest.main()
