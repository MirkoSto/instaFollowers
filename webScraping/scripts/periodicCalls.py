import random
import time
from webScraping.scripts.instagram import InstagramClient
from webScraping.scripts.randomNumbers import secondForWaitFollowPeriodicCall


def followPeriodicCall():
    bot = InstagramClient.client

    temp_followed = 0
    while temp_followed < bot.max_followed:
        try:
            followed = bot.follow()
            temp_followed = temp_followed + followed
            bot.followers_following()

            time_for_wait = secondForWaitFollowPeriodicCall()
            print("Sledeci zahtev za pracenje za " + str(time_for_wait) + "sek")
            time.sleep(time_for_wait)
        except Exception as e:
            print(e)


def behaviour2():
    bot = InstagramClient.client


    while True:

        action = random.randint(1, 4)
        print("Broj akcije " + str(action))

        if bot.follow_requested and action == 1:
            print("Poceo follow")
            time.sleep(2)

        if bot.unfollow_requested and action == 2:
            print("Poceo unfollow")
            time.sleep(2)

        if bot.like_requested and action == 3:
            print("Poceo like")
            time.sleep(2)

        if bot.watch_requested and action == 4:
            print("Poceo watch")
            time.sleep(2)



def behaviour():
    bot = InstagramClient.client

    temp_followed = 0
    temp_unfollowed = 0
    temp_liked = 0
    temp_wathced = 0



    #TODO: praviti pauze u koriscenju platforme
    # Na kraju svake iteracije proveravati koliko je vremena bio aktivan, pa ugasiti ako je duze od tipa 20min
    # koliko vremena pauzira drajver, toliko i sistem
    while True:
        action = random.randint(1, 4)

        if temp_followed < bot.max_followed and bot.follow_requested and action == 1:
            followed = bot.follow()
            temp_followed = temp_followed + followed
            bot.followers_following()

            doRandomStuff()

        if temp_unfollowed < bot.max_unfollowed and bot.unfollow_requested and action == 2:
            unfollowed = bot.follow()
            temp_unfollowed = temp_unfollowed + unfollowed
            bot.followers_following()

            doRandomStuff()

        if temp_liked < bot.max_liked and bot.like_requested and action == 3:
            liked = bot.like()
            temp_liked = temp_liked + liked

            doRandomStuff()

        if temp_wathced < bot.max_watched and bot.watch_requested and action == 4:
            watched = bot.watch()
            temp_wathced = temp_wathced + watched

            doRandomStuff()


def doRandomStuff():
    #raditi neodredjeno (random) vreme
    pass


