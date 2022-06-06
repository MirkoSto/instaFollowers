import random
import time
import datetime

from webScraping.scripts.instagram import InstagramClient
from webScraping.scripts.utility import getStartingTime, getEndingTime, printExceptionDetails, setEndingTime, \
    setStartingTime, enableAllActions, updateActionsNumber, eraseWatchedUsernames


def try_login():
    bot = InstagramClient.client

    print("usao u thread fju")
    bot.login()
    bot.login_request = False


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


def isAllActionsFinished(bot, temp_followed, temp_unfollowed, temp_liked, temp_wathced):
    if bot.max_followed == temp_followed \
            and bot.max_unfollowed == temp_unfollowed \
            and bot.max_liked == temp_liked \
            and bot.max_watched == temp_wathced:

        return True

    else:
        return False


#ako ne postoji ni jedan uslov, cekaj 60 sekundi, pa nastavi izvrsavanje ako postoji zahtev
def waitIfNoAction(bot):

    if not bot.follow_requested and \
            not bot.unfollow_requested and \
            not bot.like_requested and \
            not bot.watch_requested :
        print("ceka 5 sekundi za sledecu proveru akcije")
        time.sleep(5)


def waitTillNextDay():
    ending_time = getEndingTime()
    curr_time = datetime.datetime.today()

    left = (ending_time - curr_time).total_seconds()

    print(f"spavace {left} sekundi")
    time.sleep(left)


#TODO: praviti pauze u koriscenju platforme
# Na kraju svake iteracije proveravati koliko je vremena bio aktivan, pa ugasiti ako je duze od tipa 20min
# koliko vremena pauzira drajver, toliko i sistem

# TODO: napraviti fju za povecanje broja akcija na dnevnom nivou


# TODO: za svako vreme cekanja genersiati random broj sekundi
#  omoguciti random skrolovanje gore-dole pre neke akcije, sacekati neko vreme pre preuzimanja akcije
#  gledati sliku neko vreme


def passedOneDay():
    ending_time = getEndingTime()
    curr_time = datetime.datetime.today()

    #print(curr_time)
    #print(ending_time)

    if curr_time > ending_time:
        print("Prosao jedan ceo dan")
        return True
    else:
        print("Nije prosao jedan ceo dan")
        return False



def updateFlagsAndValues(bot):
    bot.follow_requested = False
    bot.unfollow_requested = False
    bot.like_requested = False
    bot.watch_requested = False

    bot.searched_pictures_like = []
    bot.searched_pictures_follow = []

    starting_time = datetime.datetime.today()
    ending_time = starting_time + datetime.timedelta(days=1)

    setStartingTime(str(starting_time))
    setEndingTime(str(ending_time))

    enableAllActions()
    updateActionsNumber()
    eraseWatchedUsernames()


def behaviour():
    bot = InstagramClient.client

    temp_followed = 0
    temp_unfollowed = 0
    temp_liked = 0
    temp_watched = 0

    follow_request_number = 0
    like_request_number = 0

    starting_time = datetime.datetime.today()
    ending_time = starting_time + datetime.timedelta(days=1)

    setStartingTime(str(starting_time))
    setEndingTime(str(ending_time))

    finished_unfollowing = False

    while True:
        action = random.randint(1, 4)

        #ovo se moze dogoditi sledeceg dana, kada se ceka na akciju
        waitIfNoAction(bot)

        try:

            if temp_followed < bot.max_followed and bot.follow_requested and action == 1:
                print("following")
                followed = bot.follow(temp_followed, follow_request_number % len(bot.follow_tags))
                temp_followed = temp_followed + followed
                bot.followers_following()
                follow_request_number = follow_request_number + 1

                time.sleep(2)

                doRandomStuff()



            if temp_unfollowed < bot.max_unfollowed and bot.unfollow_requested and action == 2 and not finished_unfollowing:
                print("unfollowing")
                unfollowed = bot.unfollow(temp_unfollowed)
                #u slucaju da je prazna lista followed
                if unfollowed == -1:
                    finished_unfollowing = True
                    continue

                temp_unfollowed = temp_unfollowed + unfollowed
                bot.followers_following()

                time.sleep(5)

                doRandomStuff()



            if temp_liked < bot.max_liked and bot.like_requested and action == 3:
                print("liking")
                liked = bot.like(temp_liked, like_request_number % len(bot.like_tags))
                temp_liked = temp_liked + liked
                like_request_number = like_request_number + 1

                time.sleep(5)

                doRandomStuff()

            if temp_watched < bot.max_watched and bot.watch_requested and action == 4:
                print("watching")
                watched = bot.watch()
                temp_watched = temp_watched + watched
                time.sleep(5)

                doRandomStuff()

            print("---------------------------")
            print(f"Followed {temp_followed} / {bot.max_followed}")
            print(f"Unfollowed {temp_unfollowed} / {bot.max_unfollowed}")
            print(f"Liked {temp_liked} / {bot.max_liked}")
            print(f"Watched {temp_watched} / {bot.max_watched}")
            print("---------------------------")


            if isAllActionsFinished(bot, temp_followed, temp_unfollowed, temp_liked, temp_watched):
                print("sve akcije su izvrsene")
                waitTillNextDay()
                updateFlagsAndValues(bot)

                temp_followed = 0
                temp_unfollowed = 0
                temp_liked = 0
                temp_watched = 0
                follow_request_number = 0
                like_request_number = 0
                finished_unfollowing = False

            # ulazi u slucaju da nisu sve akcije izvrsene tokom prethodnog dana, jer korisnik nije poslao zahtev za njima
            if passedOneDay():
                print("prosao jedan dan")
                updateFlagsAndValues(bot)

                temp_followed = 0
                temp_unfollowed = 0
                temp_liked = 0
                temp_watched = 0
                follow_request_number = 0
                like_request_number = 0
                finished_unfollowing = False

        except Exception as e:
            printExceptionDetails()



def doRandomStuff():
    # raditi neodredjeno (random) vreme

    # u ovo mogu uci one cetiri fje za akciju, samo bez ikakvih akcija
    pass
