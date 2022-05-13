import time
from instagram import InstagramClient


def statisticCall():
    instagramBot = InstagramClient()
    logged = False
    while True:
        try:
            if not logged:
                instagramBot.login()
                logged = True

            instagramBot.followers_following()
            time.sleep(300)
        except Exception as e:
            print(e)
            logged = False


statisticCall()
