import datetime
import json
import sys

from configuration import Configuration


def getFromStatistic(arg):
    with open(Configuration.USER_STATISTIC_DIR_PATH) as file:
        data = json.load(file)

    return data.get(arg)

def getFollowedUsernames():
    with open(Configuration.FOLLOWED_USERNAMES_FILE_PATH) as file:
        data = json.load(file)

    return data.get("usernames")


def getUnfollowedUsernames():
    with open(Configuration.UNFOLLOWED_USERNAMES_FILE_PATH) as file:
        data = json.load(file)

    return data.get("usernames")


def getStatisticData():
    with open(Configuration.USER_STATISTIC_DIR_PATH) as file:
        data = json.load(file)

    return data


def getLikedUsers():
    with open(Configuration.LIKED_USERNAMES_FILE_PATH) as file:
        data = json.load(file)

    return data.get("liked_usernames")


def updateLikedUsers(liked_users):

    data = {"liked_usernames" : liked_users}

    with open(Configuration.LIKED_USERNAMES_FILE_PATH, 'w') as file:
        json.dump(data, file)


def updateFollowedUsernames(followed):
    fileDir = Configuration.FOLLOWED_USERNAMES_FILE_PATH
    with open(fileDir, 'r') as file:
        followed_history = json.load(file)

    [followed_history["usernames"].append(followed_username) for followed_username in followed]

    with open(fileDir, 'w') as file:
        json.dump(followed_history, file)


def setFollowedUsernames(followed):
    fileDir = Configuration.FOLLOWED_USERNAMES_FILE_PATH
    with open(fileDir, 'r') as file:
        followed_history = json.load(file)

    followed_history["usernames"] = followed

    with open(fileDir, 'w') as file:
        json.dump(followed_history, file)



def updateUnfollowedUsernames(unfollowed):
    fileDir = Configuration.UNFOLLOWED_USERNAMES_FILE_PATH
    with open(fileDir, 'r') as file:
        unfollowed_history = json.load(file)

    [unfollowed_history["usernames"].append(unfollowed_username) for unfollowed_username in unfollowed]

    with open(fileDir, 'w') as file:
        json.dump(unfollowed_history, file)


def updateLikedPics(pics):
    fileDir = Configuration.LIKED_PICTURES_FILE_PATH
    with open(fileDir, 'r') as file:
        pictures = json.load(file)

    [pictures["liked_pics"].append(picture) for picture in pics]

    with open(fileDir, 'w') as file:
        json.dump(pictures, file)


def updateWatchedUsers(watched_users):
    with open(Configuration.WATCHED_USERNAMES_FILE_PATH, 'r') as file:
        data = json.load(file)


    users = data["usernames"]

    print(users)
    [users.append(username) for username in watched_users]
    print(users)

    data["usernames"] = users
    with open(Configuration.WATCHED_USERNAMES_FILE_PATH, 'w') as file:
        json.dump(data, file)


def updateStatisticDataFollow(number_followed):
    with open(Configuration.USER_STATISTIC_DIR_PATH, 'r') as file:
        data = json.load(file)

    new_total = data["total_followed"]
    new_followed = data["followed"]

    data["total_followed"] = new_total + number_followed
    data["followed"] = new_followed + number_followed

    with open(Configuration.USER_STATISTIC_DIR_PATH, 'w') as file:
        json.dump(data, file)



def updateStatisticDataUnfollow(number_unfollowed):
    with open(Configuration.USER_STATISTIC_DIR_PATH, 'r') as file:
        data = json.load(file)

    new_total = data["total_unfollowed"]
    new_followed = data["unfollowed"]

    data["total_unfollowed"] = new_total + number_unfollowed
    data["unfollowed"] = new_followed + number_unfollowed

    with open(Configuration.USER_STATISTIC_DIR_PATH, 'w') as file:
        json.dump(data, file)


def updateStatisticDataLike(number_liked):
    with open(Configuration.USER_STATISTIC_DIR_PATH, 'r') as file:
        data = json.load(file)

    new_total = data["total_liked"]
    new_liked = data["liked"]

    data["total_liked"] = new_total + number_liked
    data["liked"] = new_liked + number_liked

    with open(Configuration.USER_STATISTIC_DIR_PATH, 'w') as file:
        json.dump(data, file)


def updateStatisticDataWatch(number_watched):
    with open(Configuration.USER_STATISTIC_DIR_PATH, 'r') as file:
        data = json.load(file)

    new_total = data["total_stories"]
    new_stories = data["stories"]

    data["total_stories"] = new_total + number_watched
    data["stories"] = new_stories + number_watched

    with open(Configuration.USER_STATISTIC_DIR_PATH, 'w') as file:
        json.dump(data, file)

def updateActionsNumber():
    with open(Configuration.USER_STATISTIC_DIR_PATH, 'r') as file:
        data = json.load(file)

    data["followed"] = 0
    data["unfollowed"] = 0
    data["stories"] = 0
    data["liked"] = 0

    with open(Configuration.USER_STATISTIC_DIR_PATH, 'w') as file:
        json.dump(data, file)

def printExceptionDetails():
    exception_type, exception_object, exception_traceback = sys.exc_info()
    filename = exception_traceback.tb_frame.f_code.co_filename
    line_number = exception_traceback.tb_lineno

    print("Exception type: ", exception_type)
    print("File name: ", filename)
    print("Line number: ", line_number)


def setStartedFollowing(arg):
    with open(Configuration.ACTIONS_FILE_PATH, 'r') as file:
        data = json.load(file)

    data["follow_requested"] = arg

    with open(Configuration.ACTIONS_FILE_PATH, 'w') as file:
        json.dump(data, file)


def isStartedFollowing():
    with open(Configuration.ACTIONS_FILE_PATH, 'r') as file:
        data = json.load(file)

    return data.get("follow_requested")


def setStartedUnfollowing(arg):
    with open(Configuration.ACTIONS_FILE_PATH, 'r') as file:
        data = json.load(file)

    data["unfollow_requested"] = arg

    with open(Configuration.ACTIONS_FILE_PATH, 'w') as file:
        json.dump(data, file)


def isStartedUnfollowing():
    with open(Configuration.ACTIONS_FILE_PATH, 'r') as file:
        data = json.load(file)

    return data.get("unfollow_requested")


def setStartedLiking(arg):
    with open(Configuration.ACTIONS_FILE_PATH, 'r') as file:
        data = json.load(file)

    data["like_requested"] = arg

    with open(Configuration.ACTIONS_FILE_PATH, 'w') as file:
        json.dump(data, file)


def isStartedLiking():
    with open(Configuration.ACTIONS_FILE_PATH, 'r') as file:
        data = json.load(file)

    return data.get("like_requested")


def setStartedWatching(arg):
    with open(Configuration.ACTIONS_FILE_PATH, 'r') as file:
        data = json.load(file)

    data["watch_requested"] = arg

    with open(Configuration.ACTIONS_FILE_PATH, 'w') as file:
        json.dump(data, file)


def isStartedWatching():
    with open(Configuration.ACTIONS_FILE_PATH, 'r') as file:
        data = json.load(file)

    return data.get("watch_requested")



def setStartingTime(time):
    with open(Configuration.ACTIONS_FILE_PATH, 'r') as file:
        data = json.load(file)

    data["datetime_started"] = time

    with open(Configuration.ACTIONS_FILE_PATH, 'w') as file:
        json.dump(data, file)


def setEndingTime(time):
    with open(Configuration.ACTIONS_FILE_PATH, 'r') as file:
        data = json.load(file)

    data["datetime_finished"] = time

    with open(Configuration.ACTIONS_FILE_PATH, 'w') as file:
        json.dump(data, file)


def getStartingTime():
    with open(Configuration.ACTIONS_FILE_PATH, 'r') as file:
        data = json.load(file)

    return datetime.datetime.fromisoformat(data.get("datetime_started"))


#vreme kada moze ponovo da se krene sa izvrsavanjem akcija
def getEndingTime():
    with open(Configuration.ACTIONS_FILE_PATH, 'r') as file:
        data = json.load(file)

    return datetime.datetime.fromisoformat(data.get("datetime_finished"))


def enableAllActions():
    with open(Configuration.ACTIONS_FILE_PATH, 'r') as file:
        data = json.load(file)

    data["follow_requested"] = False
    data["unfollow_requested"] = False
    data["like_requested"] = False
    data["watch_requested"] = False

    with open(Configuration.ACTIONS_FILE_PATH, 'w') as file:
        json.dump(data, file)

def eraseWatchedUsernames():
    with open(Configuration.WATCHED_USERNAMES_FILE_PATH, 'r') as file:
        data = json.load(file)

    data["usernames"] = []

    with open(Configuration.WATCHED_USERNAMES_FILE_PATH, 'w') as file:
        json.dump(data, file)