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

    return data.get("followed_usernames")


def getUnfollowedUsernames():
    with open(Configuration.UNFOLLOWED_USERNAMES_FILE_PATH) as file:
        data = json.load(file)

    return data.get("unfollowed_usernames")


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

    [followed_history["followed_usernames"].append(followed_username) for followed_username in followed]

    with open(fileDir, 'w') as file:
        json.dump(followed_history, file)


def updateLikedPics(pics):
    fileDir = Configuration.LIKED_PICTURES_FILE_PATH
    with open(fileDir, 'r') as file:
        pictures = json.load(file)

    [pictures["liked_pics"].append(picture) for picture in pics]

    with open(fileDir, 'w') as file:
        json.dump(pictures, file)


def updateStatisticDataFollow(number_followed):
    with open(Configuration.USER_STATISTIC_DIR_PATH, 'r') as file:
        data = json.load(file)

    new_total = data["total_followed"]
    new_followed = data["followed"]

    data["total_followed"] = new_total + number_followed
    data["followed"] = new_followed + number_followed

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

    new_total = data["total_followed"]
    new_followed = data["followed"]

    data["total_stories"] = new_total + number_watched
    data["stories"] = new_followed + number_watched

    with open(Configuration.USER_STATISTIC_DIR_PATH, 'w') as file:
        json.dump(data, file)



def printExceptionDetails():
    exception_type, exception_object, exception_traceback = sys.exc_info()
    filename = exception_traceback.tb_frame.f_code.co_filename
    line_number = exception_traceback.tb_lineno

    print("Exception type: ", exception_type)
    print("File name: ", filename)
    print("Line number: ", line_number)