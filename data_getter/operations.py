import os
import pathlib

import aiohttp
import asyncio
from collections import deque
import json
from pandas import DataFrame
import pandas as pd
import requests

from configuration.loader import ConfigurationClass


def get_friends_from_user(steam_id, api_key, relationship="friend"):
    url = f"http://api.steampowered.com/ISteamUser/GetFriendList/v0001/?key={api_key}&steamid={steam_id}&relationship={relationship}"
    response = requests.get(url)
    code = response.status_code
    content = response.json()
    if (code == 200) and ("friendslist" in content.keys()):
        friends = content["friendslist"]["friends"]
        friends = [int(friend["steamid"]) for friend in friends]
    else:
        friends = []
    return friends


def get_initial_users_to_friends_dict(config: ConfigurationClass, starting_id=None):
    api_key = config.API_KEY
    max_empty_streak = config.MAX_EMPTY_STREAK
    max_users = config.MAX_USERS_PER_SESSION
    if starting_id is None:
        starting_id = config.STARTING_ID

    users_to_friends = {}
    user_queue = deque(maxlen=100000)
    user_queue.append(starting_id)
    empty_streak = 0

    while (
        len(user_queue) > 0
        and empty_streak < max_empty_streak
        and len(users_to_friends) < max_users
    ):
        current_user = user_queue.popleft()
        friends = get_friends_from_user(current_user, api_key)
        if len(friends) == 0:
            empty_streak += 1
            continue
        else:
            empty_streak = 0
            users_to_friends[current_user] = friends
            for id in friends:
                if id not in users_to_friends:
                    user_queue.append(id)
            if len(users_to_friends) % 10 == 0:
                print(f"User friends list details added: {len(users_to_friends)}")
    return users_to_friends


def save_as_json(data, filename, directory=None):
    if not (isinstance(data, list) or isinstance(data, dict)):
        data = list(data)

    if directory is None:
        directory = pathlib.Path(__file__).parent.parent

    if not filename.endswith(".json"):
        filename = filename + ".json"

    path = os.path.join(directory, "data", filename)

    with open(path, "w") as fp:
        json.dump(data, fp)
