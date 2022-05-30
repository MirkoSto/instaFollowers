import random
import time
from webScraping.scripts.instagram import InstagramClient


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

    follow_request_number = 0
    like_request_number = 0

    #TODO: praviti pauze u koriscenju platforme
    # Na kraju svake iteracije proveravati koliko je vremena bio aktivan, pa ugasiti ako je duze od tipa 20min
    # koliko vremena pauzira drajver, toliko i sistem


    #TODO: vrsiti update uradjenih akcija na dnevnom nivou!
    while True:
        #action =  #random.randint(1, 2)

        try:
            if temp_followed < bot.max_followed and bot.follow_requested: #and action == 1:
                followed = bot.follow(follow_request_number % len(bot.follow_tags))
                temp_followed = temp_followed + followed
                bot.followers_following()
                follow_request_number = follow_request_number + 1

                doRandomStuff()

            if temp_unfollowed < bot.max_unfollowed and bot.unfollow_requested:# and action == 2:
                unfollowed = bot.unfollow()
                temp_unfollowed = temp_unfollowed + unfollowed
                bot.followers_following()

                doRandomStuff()

            if temp_liked < bot.max_liked and bot.like_requested:# and action == 3:
                liked = bot.like(like_request_number % len(bot.like_tags))
                temp_liked = temp_liked + liked
                like_request_number = like_request_number + 1

                time.sleep(10)
                doRandomStuff()

            if temp_wathced < bot.max_watched and bot.watch_requested:# and action == 4:
                print("Usao u gledanje storija")
                watched = bot.watch()
                temp_wathced = temp_wathced + watched
                print("Odgledao do sada: " + str(temp_wathced))

                doRandomStuff()

        except Exception as e:
            print(e)

def doRandomStuff():
    #raditi neodredjeno (random) vreme

    #u ovo mogu uci one cetiri fje za akciju, samo bez ikakvih akcija
    pass


