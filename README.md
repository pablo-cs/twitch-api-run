# <img src="https://upload.wikimedia.org/wikipedia/commons/d/d3/Twitch_Glitch_Logo_Purple.svg" alt="Twitch Icon" width="24"> Twitch API Search Sim
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

This web app serves to allow users to search up any given Twitch streamer and
output relevant information regarding their channel, and adds them to a
streamer database. The user may also view recently active streamers via the home page.
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

1. Navigate to app/routes.py
2. Run the following command

```
python3 routes.py
```
OR

Visit: [here](http://pcrisostomosuarez.pythonanywhere.com/search)
Sample Website: