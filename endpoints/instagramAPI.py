import os
from flask import Flask, Response, jsonify, request
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt, get_jwt_identity
import json
from webScraping.scripts.instagram import InstagramClient
from configuration import Configuration
from models import database


app = Flask(__name__)
app.config.from_object(Configuration)

jwt = JWTManager(app)


@app.route("/login", methods = ["POST"])
def login():
    instagramClient = InstagramClient()
 #   self.username = 
 #   self.password =
    instagramClient.login_thread.start()
    return "logging..."


@app.route("/statistic", methods = ["GET"])
def statistic():
    mydir = Configuration.USER_STATISTIC_DIR_PATH

    with open(mydir) as file:
        data = json.load(file)
        #print(data["followers_number"])
        return data

@app.route("/follow", methods = ["GET"])
def follow():
    instagramClient = InstagramClient()
    instagramClient.tag = request.args.get("tag")
    #instagramClient.follow_thread.start()
    instagramClient.watch_thread.start()
    return {"response" : "Started following..."}, 200


@app.route("/unfollow", methods = ["GET"])
def unfollow():
    pass


@app.route("/getHTML", methods = ["GET"])
def getHTML():
    return "Hello World!"


@app.route("/", methods = ["GET"])
def index():
    return "Hello World!"


if(__name__ == "__main__"):
    database.init_app(app)
    app.run(debug = True, host = "0.0.0.0", port = 5000)
