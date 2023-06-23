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