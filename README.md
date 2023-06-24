# Twitch API Search Sim
[![Style Checker Workflow](https://github.com/pablo-cs/twitch-api-run/actions/workflows/style.yaml/badge.svg)](https://github.com/pablo-cs/twitch-api-run/actions/workflows/style.yaml)
[![Test Checker Workflow](https://github.com/pablo-cs/twitch-api-run/actions/workflows/tests.yaml/badge.svg)](https://github.com/pablo-cs/twitch-api-run/actions/workflows/tests.yaml)

## Table of Contents
- [Description](#description)
- [Setup](#setup)
  - [Updating Environment Variables](#updating-environment-variables)
  - [Install Libraries](#install-libraries)
- [How to Run](#how-to-run)
- [How this Code Works](#how-this-code-works)

## Description

This program serves to allow users to search up any given Twitch account and
output relevant information regarding their channel, and then adds them to a
user database. The user may enter as many accounts as they want until they quit.
This program uses the [Twitch API](https://dev.twitch.tv/docs/api/) to request and retrieve information about Twitch's
user base.
Relevant data from the search profiles include:
* Channel Name
* Channel Description
* Follower Count
* Broadcaster Type
* Account Creation Date
* Most Recent Videos
  * Title
  * Date Posted
  * View Count


## Setup

In order to use this code, one must attain a Twitch Developer Account and obtain a Client ID and Client Secret.
Steps to do so can be found [here](https://dev.twitch.tv/docs/api/get-started/)

### Updating Environment Variables
From there, open .bashrc:


```
sudo nano ~/.bashrc
```

Scroll down and add the following variables:

```
export TWITCH_CLIENT_ID=[variable_value]
export TWITCH_CLIENT_SECRET=[variable_value]
```

Then:

```
source ~/.bashrc
```

### Install libraries
Final step, install the following python libraries:
```
pip install twitchAPI pandas requests sqlalchemy pytest
```

## How to Run
1. Navigate to directory where twitch.py is located
2. Execute the following command

```
python3 twitch.py
```

Sample output:
```Enter username to search and add or QUIT: Miniminter
------------------
User found!
Name: miniminter
Description: Professional Simon
Follower count: 1,921,105
Broadcaster Type: partner
Member since: February 01, 2013
Last played: Overwatch 2
Most Recent Videos:

Title: SIMON REACTS!
Views: 50,340
Posted: November 02, 2022
------------------
Enter username to search and add or QUIT: Shofu
------------------
User found!
Name: shofu
Description: WDFA. Business Inquires: shofubiz@gmail.com
Follower count: 266,587
Broadcaster Type: partner
Member since: February 10, 2009
Last played: Street Fighter 6
Most Recent Videos:

Title: back on the dee jay !merch
Views: 18,992
Posted: June 22, 2023

Title: Highlight: whats this nintendo direct talkin bout?? !merch
Views: 385
Posted: June 21, 2023

Title: whats this nintendo direct talkin bout?? !merch
Views: 19,592
Posted: June 21, 2023

Title: skreet fighter !merch
Views: 7,851
Posted: June 20, 2023

Title: in the dee jay lab !merch
Views: 35,207
Posted: June 19, 2023
------------------
Enter username to search and add or QUIT: quit
------------------
Here are all the streamers you added
  display_name broadcaster_type  follower_count
0   miniminter          partner         1921105
1        shofu          partner          266587
Bye!
```

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