import threading

from flask import Flask, Response, jsonify, request, send_file
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt, get_jwt_identity
import json

from webScraping.scripts.instagram import InstagramClient
from configuration import Configuration
from models import database

from webScraping.scripts.utility import getFromStatistic, isStartedFollowing, isStartedUnfollowing, isStartedWatching, \
    isStartedLiking, setStartedFollowing, setStartedUnfollowing, setStartedLiking, setStartedWatching
from webScraping.scripts.periodicCalls import behaviour, try_login

app = Flask(__name__)
app.config.from_object(Configuration)

jwt = JWTManager(app)

print("Ulogovan : " + str(getFromStatistic("logged")))

InstagramClient.client = InstagramClient()


@app.route("/login", methods = ["POST"])
def login():

    instagramClient = InstagramClient.client
    instagramClient.username = request.args.get('username')
    instagramClient.password = request.args.get('password')
   # instagramClient.login_request = True
    startLogging(instagramClient)
    #if not instagramClient.try_login_started:
    #    instagramClient.try_login_started = True
    #    startLogging(instagramClient)
    return {"response" : "logging"}



@app.route("/isLogged", methods = ["GET"])
def isLogged():
    mydir = Configuration.USER_STATISTIC_DIR_PATH

    with open(mydir) as file:
        data = json.load(file)

        if not data["logged"]:
            print("logging")
            return {"message": "logging"}
        else:
            print("logged")
            return {"message": "logged"}


@app.route("/getProfilePicture", methods = ["GET"])
def getProfilePicture():

    return send_file(Configuration.USER_PROFILE_PICTURE_FILE_PATH, mimetype='image/gif'), 200


#samo za svrhe testiranja
@app.route("/followingsFollowers", methods = ["GET"])
def followingsFollowers():
    instagramClient = InstagramClient.client

    #thread = threading.Thread(target=instagramClient.followers_following, args=(), kwargs={})
    #thread.start()
    #instagramClient.followers_following()

    instagramClient.moveMouse()

    return {"request" : "true"}, 200



@app.route("/statistic", methods = ["GET"])
def statistic():
    logged = getFromStatistic("logged")
    if not logged:
        return {"response": "false"}, 200

    mydir = Configuration.USER_STATISTIC_DIR_PATH

    with open(mydir) as file:
        data = json.load(file)
        return data, 200


@app.route("/follow", methods = ["GET"])
def follow():
    logged = getFromStatistic("logged")
    if not logged:
        return {"response": "not logged"}, 200

    if isStartedFollowing():
        return {"response" : "in use"}, 200

    instagramClient = InstagramClient.client

    tags = request.args.get("tags")
    tags = tags.split(",")
    instagramClient.follow_tags = tags
    instagramClient.follow_requested = True

    setStartedFollowing(True)

    # samo ce se na prvu aktivnost pokrenuti
    if not instagramClient.started_periodic_calls:
        print("usao u uslov")
        startBehaviour(instagramClient)

    return {"response" : "started"}, 200


@app.route("/unfollow", methods = ["GET"])
def unfollow():
    logged = getFromStatistic("logged")
    if not logged:
        return {"response": "not logged"}, 200

    if isStartedUnfollowing():
        return {"response" : "in use"}, 200

    instagramClient = InstagramClient.client
    instagramClient.unfollow_requested = True

    setStartedUnfollowing(True)

    # samo ce se na prvu aktivnost pokrenuti
    if not instagramClient.started_periodic_calls:
        startBehaviour(instagramClient)

    return {"response": "started"}, 200


@app.route("/like", methods = ["GET"])
def like():
    logged = getFromStatistic("logged")
    if not logged:
        return {"response": "not logged"}, 200

    if isStartedLiking():
        return {"response": "in use"}, 200

    instagramClient = InstagramClient.client

    tags = request.args.get("tags")
    tags = tags.split(",")

    instagramClient.like_tags = tags
    instagramClient.like_requested = True
    setStartedLiking(True)

    # samo ce se na prvu aktivnost pokrenuti
    if not instagramClient.started_periodic_calls:
        startBehaviour(instagramClient)

    return {"response": "started"}, 200

@app.route("/watch", methods=["GET"])
def watch():
    logged = getFromStatistic("logged")
    if not logged:
        return {"response": "false"}, 200

    if isStartedWatching():
        return {"response": "in use"}, 200

    instagramClient = InstagramClient.client
    instagramClient.watch_requested = True
    setStartedWatching(True)

    # samo ce se na prvu aktivnost pokrenuti
    if not instagramClient.started_periodic_calls:
        startBehaviour(instagramClient)

    return {"response": "started"}, 200



@app.route("/getLikedPictures", methods=["GET"])
def getLikedPictures():
    logged = getFromStatistic("logged")
    if not logged:
        return [], 500

    with open(Configuration.LIKED_PICTURES_FILE_PATH, 'r') as file:
        pictures = json.load(file)

    return pictures, 200



@app.route("/getFollowedUsernames", methods=["GET"])
def getFollowedUsernames():
    logged = getFromStatistic("logged")
    if not logged:
        return [], 500

    with open(Configuration.FOLLOWED_USERNAMES_FILE_PATH, 'r') as file:
        pictures = json.load(file)

    return pictures, 200



@app.route("/getUnfollowedUsernames", methods=["GET"])
def getUnfollowedUsernames():
    logged = getFromStatistic("logged")
    if not logged:
        return [], 500

    with open(Configuration.UNFOLLOWED_USERNAMES_FILE_PATH, 'r') as file:
        pictures = json.load(file)

    return pictures, 200

@app.route("/getWatchedUsernames", methods=["GET"])
def getWatchedUsernames():
    logged = getFromStatistic("logged")
    if not logged:
        return [], 500

    with open(Configuration.WATCHED_USERNAMES_FILE_PATH, 'r') as file:
        pictures = json.load(file)

    return pictures, 200


def startLogging(instagramClient):
    thread = threading.Thread(target=try_login, args=(), kwargs={})
    thread.start()

def startBehaviour(instagramClient):
    instagramClient.started_periodic_calls = True
    thread = threading.Thread(target=behaviour, args=(), kwargs={})
    thread.start()

@app.route("/", methods = ["GET"])
def index():
    return "Hello World!"


if __name__ == "__main__":
    database.init_app(app)
    app.run(debug = False, host = "0.0.0.0", port = 5000)
