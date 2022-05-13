import json
from configuration import Configuration

with open(Configuration.UNFOLLOWED_USERNAMES_FILE_PATH) as file:
    data = json.load(file)
    print("Unfollowed usernames: ")
    print(data.get("unfollowed_usernames"))
