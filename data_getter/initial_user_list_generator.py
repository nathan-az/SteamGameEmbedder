import json

from configuration.loader import ConfigurationLoader
from data_getter.operations import get_initial_users_to_friends_dict, save_as_json

config = ConfigurationLoader().get_engine_configuration()
users_to_friends = get_initial_users_to_friends_dict(config)
save_as_json(users_to_friends, "users_to_friends")
