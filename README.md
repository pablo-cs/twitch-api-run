# Twitch API Search Sim

## Description

This code currently allows the user to enter in any number
of Twitch users, view their relevant Twitch information, and then
add them to a database. The user enters as many users as they want
until they quit.
Relevant data from the search profiles include:
* Username
* Follower count
* Broadcaster Type
* Account creation date
* Most recent videos

## Setup

In order to use this code, one must attain a Twitch Developer Account
and obtain a Client ID and Client Secret.

### Updating Environment Variables
From there, open .bashrc:


`
sudo nano ~/.bashrc
`

Scroll down and add the following variables:

`
export TWITCH_CLIENT_ID=[variable_value]
`


`
export TWITCH_CLIENT_SECRET=[variable_value]
`

Then:

`
source ~/.bashrc
`

### Install libraries
Final step, install the twitchAPI python library:

`
pip install twitchAPI
`

## How to Run

To run, execute the following command in the directory twitch.py is located:

`
python3 twitch.py
`

## How this Code Works

The code uses the TwitchAPI to fetch information from the users search for and provide
corresponding public information about their Twitch profile. 
1. The code asks for the user's username.
2. The TwitchAPI is queried to find a user with the matching username. 
3. If such a user is found, that user's unique ID, along with other data, is shared and put into a dictionary. 
4. Using that dictionary, relevant information is printed by the program. 
5. Using the user's ID that is obtained from the API, the code than queries the TwitchAPI to search for videos with a matching user ID (since they can't be searched
by directly using the username like with the user itself). 
6. The program then prints the most recent 5 videos on channel.