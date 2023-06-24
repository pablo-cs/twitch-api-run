import unittest
from unittest.mock import patch, Mock
import requests
from twitch import get_user_data


class TwitchAPITestCase(unittest.TestCase):

    @patch('twitch.requests.get')
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

        user_data = get_user_data('twitchdev', headers)
        print(user_data['follower_count'])
        # Assert the expected result
        expected_user_data = {
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
            'follower_count': 8,
            'last_game_played': 'Science & Technology',
            'video_data': []
        }

        self.assertEqual(user_data, expected_user_data)


if __name__ == '__main__':
    unittest.main()
