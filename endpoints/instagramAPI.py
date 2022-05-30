import threading

from flask import Flask, Response, jsonify, request
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt, get_jwt_identity
import json

from webScraping.scripts.instagram import InstagramClient
from configuration import Configuration
from models import database

from webScraping.scripts.utility import getFromStatistic
from webScraping.scripts.periodicCalls import behaviour

app = Flask(__name__)
app.config.from_object(Configuration)

jwt = JWTManager(app)

InstagramClient.client = InstagramClient()

logged = getFromStatistic("logged")
print("Ulogovan : " + str(logged))

@app.route("/login", methods = ["POST"])
def login():

    instagramClient = InstagramClient.client
    instagramClient.username = request.args.get('username')
    instagramClient.password = request.args.get('password')
    instagramClient.login_thread.start()
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




@app.route("/statistic", methods = ["GET"])
def statistic():
    mydir = Configuration.USER_STATISTIC_DIR_PATH

    with open(mydir) as file:
        data = json.load(file)
        #print(data["followers_number"])
        return data

@app.route("/action", methods = ["GET"])
def actionFunction():
    if not logged:
        return {"response": "false"}, 200

    instagramClient = InstagramClient.client

    action = request.args.get("action")
    if action == "follow":
        tags = request.args.get("tags")
        tags = tags.split(",")
        instagramClient.follow_tags = tags
        instagramClient.follow_requested = True

    if action == "unfollow":
        instagramClient.unfollow_requested = True

    if action == "like":
        tags = request.args.get("tags")
        tags = tags.split(",")
        instagramClient.like_tags = tags
        instagramClient.like_requested = True

    if action == "watch":
        instagramClient.watch_requested = True

    if not instagramClient.started_periodic_calls:
        instagramClient.started_periodic_calls = True
        #samo ce se na prvu aktivnost pokrenuti
        thread = threading.Thread(target=behaviour, args=(), kwargs={})
        thread.start()

    return {"response": "true"}, 200


@app.route("/follow", methods = ["GET"])
def follow():

    if not logged:
        return {"response": "false"}, 200

    instagramClient = InstagramClient.client

    tags = request.args.get("tags")
    tags = tags.split(",")
    instagramClient.follow_tags = tags
    instagramClient.follow_requested = True

    # samo ce se na prvu aktivnost pokrenuti
    if not instagramClient.started_periodic_calls:
        print("usao u uslov")
        startBehaviour(instagramClient)

    return {"response" : "true"}, 200


@app.route("/unfollow", methods = ["GET"])
def unfollow():
    if not logged:
        return {"response": "false"}, 200

    instagramClient = InstagramClient.client
    instagramClient.unfollow_requested = True

    # samo ce se na prvu aktivnost pokrenuti
    if not instagramClient.started_periodic_calls:
        startBehaviour(instagramClient)

    return {"response": "true"}, 200


@app.route("/like", methods = ["GET"])
def like():
    if not logged:
        return {"response": "false"}, 200

    instagramClient = InstagramClient.client

    tags = request.args.get("tags")
    tags = tags.split(",")

    instagramClient.like_tags = tags
    instagramClient.like_requested = True

    # samo ce se na prvu aktivnost pokrenuti
    if not instagramClient.started_periodic_calls:
        startBehaviour(instagramClient)

    return {"response": "true"}, 200

@app.route("/watch", methods=["GET"])
def watch():
    if not logged:
        return {"response": "false"}, 200

    instagramClient = InstagramClient.client
    instagramClient.watch_requested = True

    # samo ce se na prvu aktivnost pokrenuti
    if not instagramClient.started_periodic_calls:
        startBehaviour(instagramClient)

    return {"response": "true"}, 200


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
