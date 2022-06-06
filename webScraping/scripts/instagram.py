import time
import json

from selenium.webdriver import Keys
from selenium.webdriver.common.actions.action_builder import ActionBuilder
from selenium.webdriver.common.actions.mouse_button import MouseButton
from selenium.webdriver.common.by import By

from threading import Thread

from configuration import Configuration
from webScraping.scripts.randomNumbers import numberStories, nextStorie, ordinalNumberPic, waitToLoadPage, \
    secondForWaitFollow
from webScraping.strings.classNamesCSS import ClassNames

from webScraping.scripts.webdriverInstance import WebDriverInstance
from webScraping.strings.xpaths import XPaths
from webScraping.strings.urls import URL

from webScraping.scripts.webUtility import showPictureByTag, findFollowButtonsAndUsernames, getPicturesForTag, \
    get_cookies, set_cookies, getUsersPics, getTagPics, showPictureByHref, clickAtPoint, \
    findUnfollowButtonsAndUsernames, scrollWindow
from webScraping.scripts.utility import getUnfollowedUsernames, getStatisticData, updateFollowedUsernames, \
    getFollowedUsernames, getFromStatistic, updateStatisticDataFollow, updateLikedPics, updateStatisticDataLike, \
    getLikedUsers, printExceptionDetails, updateLikedUsers, updateWatchedUsers, updateStatisticDataWatch, \
    setFollowedUsernames, updateUnfollowedUsernames, updateStatisticDataUnfollow

from webScraping.scripts import randomNumbers

print(Configuration.CHROMEDRIVER_PATH)


class InstagramClient:

    client = None

    def __init__(self):

        self.driver = WebDriverInstance().driver

        self.username = Configuration.USERNAME
        self.password = Configuration.PASSWORD

        self.logged = False
        self.follow_tags = []
        self.like_tags = []

        self.max_followed = getFromStatistic("max_followed")
        self.max_unfollowed = getFromStatistic("max_unfollowed")
        self.max_liked = getFromStatistic("max_liked")
        self.max_watched = getFromStatistic("max_stories")
        self.max_commented = getFromStatistic("max_commented")

        self.temp_followed = 0
        self.temp_unfollowed = 0
        self.temp_watched = 0
        self.temp_liked = 0
        self.temp_commented = 0

        #flegovi da li je danas upucen zahtev za datom akcijom
        self.follow_requested = False
        self.unfollow_requested = False
        self.like_requested = False
        self.watch_requested = False
        self.login_request = False
        self.try_login_started = False

        #podatak koji se cuva samo u RAM memoriji. Cuva slike iz kojih je pronalazio korisnike za lajkovanje/pracenje za taj dan
        self.searched_pictures_like = []
        self.searched_pictures_follow = []

        self.started_periodic_calls = False

        self.login_thread = Thread(target=self.login, args=())
        #self.follow_thread = Thread(target=self.follow, args=())
        #self.watch_thread = Thread(target=self.watchStories, args=())

        self.login_with_cookies(self.driver)


    def login(self):
        print("Logovanje...")

        statistic_dir = Configuration.USER_STATISTIC_DIR_PATH
        driver = self.driver

        failed = self.login_with_cookies(driver)

        #ako nema kolacica
        if failed:
            try:

                driver.get(URL.INSTAGRAM_LOGIN)
                driver.implicitly_wait(10)

                user_name_elem = driver.find_element(by=By.XPATH, value=XPaths.LOGIN_USERNAME)
                user_name_elem.clear()
                user_name_elem.send_keys(self.username)
                pass_elem = driver.find_element(by=By.XPATH, value=XPaths.LOGIN_PASSWORD)
                pass_elem.clear()
                pass_elem.send_keys(self.password)
                button = driver.find_element(by=By.XPATH, value=XPaths.LOGIN_SUBMIT_BUTTON)
                button.click()

                failed = False

            #ako je doslo do greske, nece se ulogovati
            except Exception as e:
                print(str(e))

                with open(statistic_dir) as file:
                    data = json.load(file)

                print("Selenium exception!")
                data["logged"] = False

                with open(statistic_dir, 'w') as file:
                    json.dump(data, file)

                failed = True

            #ako je failed = True, zavrsava se funkcija i vraca se odgovor da je neuspelo logovanje
            if not failed:
                print(f"usao u uslov if not faiiled, failed = {failed}")
                time.sleep(4)

                with open(statistic_dir) as file:
                    data = json.load(file)

                print(driver.current_url)

                #ako nije uspeo da se uloguje
                if driver.current_url == URL.INSTAGRAM_LOGIN:
                    print("Problem u mrezi ili u kredencijalima")
                    data["logged"] = False

                    with open(statistic_dir, 'w') as file:
                        json.dump(data, file)

                # ako je ulogovan
                else:

                    self.logged = True

                    Configuration.USERNAME = self.username

                    data["logged"] = True
                    data["username"] = self.username
                    with open(statistic_dir, 'w') as file:
                        json.dump(data, file)

                    #preuzimanje kolacica
                    get_cookies(driver)
                    self.followers_following()




        #osvezavanje kolacica
        else:
            get_cookies(driver)
            self.followers_following()


    #vraca vrednost failed
    def login_with_cookies(self, driver):
        # dodavanje kolacica

        has_cookies = set_cookies(driver)

        if has_cookies:
            driver.get(URL.INSTAGRAM_LOGIN)
            self.logged = True
            return False

        else:
            return True


    def getProfilePicture(self, driver):

        try:
            with open(Configuration.USER_PROFILE_PICTURE_FILE_PATH, 'wb') as file:
                pic = driver.find_elements(by=By.TAG_NAME, value='img')
                print(f"Pronadjeno {len(pic)} slika!")
                file.write(pic[0].screenshot_as_png)

        except Exception as e:
            printExceptionDetails()


    def moveMouse(self):
        driver = self.driver
        driver.get(URL.INSTAGRAM + Configuration.USERNAME)
        time.sleep(5)

        print("Kliktanje na stori")
        action = ActionBuilder(self.driver)
        action.pointer_action.move_to_location(376, 379)
        action.pointer_action.pointer_down(MouseButton.LEFT)
        action.pointer_action.pointer_up(MouseButton.LEFT)
        action.perform()

    def followers_following(self):
        print("Dohvatanje broja pratilaca")

        driver = self.driver
        driver.get(URL.INSTAGRAM + Configuration.USERNAME)
        time.sleep(5)

        self.getProfilePicture(driver)

        followers_number = driver.find_element(by=By.XPATH, value=XPaths.FOLLOWERS_NUMBER).text
        following_number = driver.find_element(by=By.XPATH, value=XPaths.FOLLOWING_NUMBER).text

        print("Broj pratilaca: " + followers_number)
        print("Broj pracenja: " + following_number)

        statistic_dir = Configuration.USER_STATISTIC_DIR_PATH

        with open(statistic_dir, 'r') as file:
            data = json.load(file)

        if data is None:
            print("Error: data from statistic.json is None!")

            data = {
                "followers_number": followers_number,
                "following_number": following_number
            }

        data["followers_number"] = followers_number
        data["following_number"] = following_number

        with open(statistic_dir, 'w') as file:
            json.dump(data, file)


    def preparingForLiking(self, driver, tag):
        unfollowed_usernames = getUnfollowedUsernames()
        followed = getFollowedUsernames()

        # lista koja sadrzi imena korisnika koje ne treba vise pratiti
        [followed.append(username) for username in unfollowed_usernames]
        time.sleep(5)
        print("Vec zapraceni korisnici: ")
        print(followed)

        try:
            print(f"Tag za trenutnu akciju: {tag}")
            driver.get(URL.TAG_SEARCH + tag)
            driver.implicitly_wait(10)

            pic_hrefs = getTagPics(driver)

            print(f"Pronadjeno {len(pic_hrefs)} slika sa taga")


            pic_hrefs = [href for href in pic_hrefs if href not in self.searched_pictures_like]

            print(f"Posle izbacivanja slika ima {len(pic_hrefs)}")

            if not showPictureByTag(driver, pic_hrefs):
                return False, [], []

        except Exception as e:
            print(e)
            return False, [], []

        return True, followed, pic_hrefs


    def preparingForFollowing(self, driver, tag):
        unfollowed_usernames = getUnfollowedUsernames()
        followed = getFollowedUsernames()

        # lista koja sadrzi imena korisnika koje ne treba vise pratiti
        [followed.append(username) for username in unfollowed_usernames]
        time.sleep(5)
        print("Vec zapraceni korisnici: ")
        print(followed)

        try:
            print(f"Tag za trenutnu akciju: {tag}")
            driver.get(URL.TAG_SEARCH + tag)
            driver.implicitly_wait(10)

            pic_hrefs = getTagPics(driver)

            print(f"Pronadjeno {len(pic_hrefs)} slika sa taga")


            pic_hrefs = [href for href in pic_hrefs if href not in self.searched_pictures_follow]

            print(f"Posle izbacivanja slika ima {len(pic_hrefs)}")

        except Exception as e:
            print(e)
            return False, [], []

        return True, followed, pic_hrefs



    #vraca broj zapracenih korisnika
    def follow(self, today_followed, index):
        print("Priprema za pracenje...")
        driver = self.driver

        self.temp_followed = 0
        new_followed = []

        try:

            #ako dodje do greske u pripremi, izlazi iz fje
            success, followed, pic_hrefs = self.preparingForFollowing(driver, self.follow_tags[index])
            if not success:
                return 0



            number_follows = randomNumbers.followNumberOneTry()
            if today_followed + number_follows > self.max_followed:
                number_follows = self.max_followed - today_followed

            print(f"Broj pracenja u ovom zahtevu: {number_follows}")

            for picture in pic_hrefs:
                showPictureByHref(driver, picture)
                follow_buttons, follow_usernames = findFollowButtonsAndUsernames(driver)
                self.searched_pictures_follow.append(picture)

                i = 0
                while self.temp_followed < number_follows:

                    button_color = follow_buttons[i].value_of_css_property("background-color")
                    print("Color: " + button_color)
                    print(follow_buttons[i].text)

                    # ako je dugme plavo i ako nije nekad pre zapratio --> zaprati
                    if button_color != Configuration.WHITE_COLOR_FOLLOW_BUTTON and follow_usernames[i] not in followed:
                        self.temp_followed = self.temp_followed + 1

                        follow_buttons[i].click()
                        new_followed.append(follow_usernames[i])
                        print(f"Zapracen {follow_usernames[i]}!")

                        # ako je dostignuta kvota pracenja za taj dan, prekini pracenje
                        if self.max_followed == self.temp_followed:
                            break

                        time.sleep(randomNumbers.secondForWaitFollow())

                    #ako je probao da klikne na sve ucitane dugmice, a nije zapratio dovoljan broj, predji na drugu sliku
                    i = i + 1
                    if i == len(follow_buttons):
                        break

                if self.temp_followed == number_follows:
                    break

            if len(new_followed) > 0:
                updateFollowedUsernames(new_followed)
                updateStatisticDataFollow(self.temp_followed)

            print(f"Zapraceno {self.temp_followed} od {number_follows}")
            return self.temp_followed

        except Exception as e:
            printExceptionDetails()

            if len(new_followed) > 0:
                updateFollowedUsernames(new_followed)
                updateStatisticDataFollow(self.temp_followed)

            return self.temp_followed



    #TODO: kretati se kroz listu korisnika koje pratimo i proveravati kad se naidje na korisnika koji treba da se otprati,
    # kako bi se ponasalo realno ponasanje korisnika na platformi
    def unfollow(self, today_unfollowed):
        driver = self.driver
        self.temp_unfollowed = 0

        unfollowed_number = 2 #randomNumbers.followNumberOneTry()

        if today_unfollowed + unfollowed_number > self.max_unfollowed:
            unfollowed_number = self.max_unfollowed - today_unfollowed


        unfollow_usernames_all = getFollowedUsernames()

        if unfollowed_number > len(unfollow_usernames_all):
            unfollowed_number = len(unfollow_usernames_all)

        #indikator da nema vise koga da otprati
        if len(unfollow_usernames_all) == 0:
            return -1

        unfollow_usernames = unfollow_usernames_all[0:unfollowed_number]

        print(f"Broj pracenja u ovom zahtevu: {unfollowed_number}")
        print("korisnici koji ce se otpratiti")


        unfollowed = []

        try:
            driver.get(URL.INSTAGRAM + Configuration.USERNAME)
            time.sleep(5)

            clickAtPoint(driver, 874, 164)

            #dok ne otprati odredjen broj u ovom zahtevu
            while self.temp_unfollowed < unfollowed_number:
                print(unfollow_usernames)
                usernames, buttons = findUnfollowButtonsAndUsernames(driver)

                for i in range(0, len(usernames)):
                    if usernames[i] in unfollow_usernames:
                        self.temp_unfollowed = self.temp_unfollowed + 1

                        buttons[i].click()
                        time.sleep(1.5)
                        try:
                            button = driver.find_element(by=By.CLASS_NAME, value=ClassNames.UNFOLLOW_BUTTON_CONFIRM)
                            button.click()

                        except Exception as e:
                            print("Nalog nije privatan")
                            printExceptionDetails()

                        unfollowed.append(usernames[i])
                        print(f"Otpracen {usernames[i]}")

                        time.sleep(secondForWaitFollow())

                        #TODO: ispitati da li je privatan profil

                time.sleep(10)

                #izbacivanje iz liste ako je otpracen
                for username in unfollowed:
                    unfollow_usernames_all.remove(username)

                #skrolovanje liste, ako nije zavrsena operacija
                scrollWindow(driver, ClassNames.FOLLOWING_SCROLL_LIST)

            setFollowedUsernames(unfollow_usernames_all)
            updateUnfollowedUsernames(unfollowed)
            updateStatisticDataUnfollow(self.temp_unfollowed)

            return self.temp_unfollowed


        except Exception as e:
            printExceptionDetails()

            setFollowedUsernames(unfollow_usernames_all)
            updateUnfollowedUsernames(unfollowed)
            updateStatisticDataUnfollow(self.temp_unfollowed)
            return self.temp_unfollowed


    #ne lajkuje slike korisnika koje ne prati
    def like(self, today_liked, index):
        print("Priprema za lajkovanje...")
        driver = self.driver

        liked_users = getLikedUsers()

        liked_pics = []
        number_likes = 0
        self.temp_liked = 0

        try:

            #ako dodje do greske u pripremi, izlazi iz fje
            success, followed, pic_hrefs = self.preparingForLiking(driver, self.like_tags[index])
            if not success:
                return 0

            follow_buttons, like_usernames = findFollowButtonsAndUsernames(driver)
            self.searched_pictures_like.append(pic_hrefs.pop(0))

            number_likes = randomNumbers.followNumberOneTry()
            if today_liked + number_likes > self.max_followed:
                number_likes = self.max_liked - today_liked

            print(f"Broj korisnika za lajkovanje u ovom zahtevu: {number_likes}")

            while True:
                for username in like_usernames:

                    #ako je ovog korisnika vec nekad lajkovao ili zapratio, preskoci ga
                    if username in liked_users or username in followed:
                        print(f"Korisnik {username} je vec lajkovan ili zapracen!")
                        continue

                    driver.get(URL.INSTAGRAM + username)

                    users_pics = getUsersPics(driver)
                    if len(users_pics) == 0:
                        continue

                    pic_number = ordinalNumberPic(len(users_pics) - 1)
                    driver.get(users_pics[pic_number])
                    time.sleep(waitToLoadPage())

                    span_like_button = driver.find_element(by=By.CLASS_NAME, value=ClassNames.LIKE_SPAN)
                    like_button = span_like_button.find_element(by=By.TAG_NAME, value='Button')

                    # slika nikad nece biti lajkovana od pre, jer se preskacu vec lajkovani korisnici!
                    self.temp_liked = self.temp_liked + 1

                    like_button.click()
                    liked_pics.append(users_pics[pic_number])
                    liked_users.append(username)

                    print(f"Lajkovana slika {users_pics[pic_number]}!")

                    time.sleep(randomNumbers.secondForWaitFollow())

                    if self.temp_liked == number_likes:
                        break

                if self.temp_liked == number_likes:
                    break

                #pod pretpostavkom da nikad nece doci do kraja liste pretrazenih slika sa taga, jer se lajkuje manji broj ljudi
                next_pic = pic_hrefs.pop(0)
                self.searched_pictures_like.append(next_pic)
                showPictureByHref(driver, next_pic)
                follow_buttons, like_usernames = findFollowButtonsAndUsernames(driver)

            if len(liked_pics) > 0:
                updateLikedPics(liked_pics)
                updateLikedUsers(liked_users)
                updateStatisticDataLike(self.temp_liked)


            print(f"Lajkovano {self.temp_liked} od {number_likes}")
            return self.temp_liked

        except Exception as e:
            print(e)
            printExceptionDetails()

            if len(liked_pics) > 0:
                updateLikedPics(liked_pics)
                updateLikedUsers(liked_users)
                updateStatisticDataLike(self.temp_liked)

                print(f"Lajkovano {self.temp_liked} od {number_likes}")

                return self.temp_followed

            else:
                return 0




    #gledanje storija korisnika koje pratim
    def watch(self):
        driver = self.driver
        driver.get(URL.INSTAGRAM)
        time.sleep(3)

        try:
            driver.find_element(by=By.CLASS_NAME, value=ClassNames.POPUP_DIALOG).click()
        except Exception as e:
            print("Nije iskocio dijalog za notifikacije!")


        self.temp_watched = 0

        try:
            storie = driver.find_elements(by=By.CLASS_NAME, value=ClassNames.STORIE_FOLLOWING)[3]
            storie.click()
            time.sleep(2)
        except Exception as e:
            printExceptionDetails()
            print("Greska pri ulasku na stori!")
            return 0

        watched_users = []
        number_users = 2 #numberStories()
        print("Treba da odgleda " + str(number_users) + " storija!")


        page_body = driver.find_element(by=By.TAG_NAME, value="body")

        while self.temp_watched < number_users:
            try:
                username_div = driver.find_element(by=By.CLASS_NAME, value=ClassNames.STORIE_USERNAME)
                username = username_div.find_element(by=By.TAG_NAME, value="a").get_attribute("href")
                username = username.removeprefix("https://www.instagram.com/")

                #povecava se za jedan i pamti korisnika samo jednom u slucaju da je objavio vise storija
                if username not in watched_users:
                    self.temp_watched = self.temp_watched + 1
                    watched_users.append(username)
                    print(username)

                watch_time = nextStorie()
                print("Gledace " + str(watch_time) + " sekundi")
                time.sleep(watch_time)
                page_body.send_keys(Keys.ARROW_RIGHT)


            except Exception:
                #moze da se se desi, pored uobicajenih stvari, da nema vise storija za gledanje!
                #isto tako dolazi do greske ako stori traje krace od vremena cekanja!
                printExceptionDetails()

                #print(watched_users)
                updateWatchedUsers(watched_users)
                updateStatisticDataWatch(self.temp_watched)
                return self.temp_watched

        page_body.send_keys(Keys.ARROW_UP)

        #print(watched_users)
        updateWatchedUsers(watched_users)
        updateStatisticDataWatch(self.temp_watched)
        return self.temp_watched



    #vraca broj odgledanih storija u jednom zahtevu
    #ne mora da vraca, ima vec u instagramClient instanci temp atribut!!
    def watchStories(self):
        driver = self.driver
        driver.get(URL.TAG_SEARCH + self.tag)

        pic_urls = getPicturesForTag(driver)
        #pic_urls = ["https://www.instagram.com/p/CcNkX3ijrDG/"]

        number_stories = randomNumbers.storiesNumberOneTry()


        number_watched = 0
        print(f"Broj storija za gledanje: {number_stories}")


        for pic_url in pic_urls:
            driver.get(pic_url)
            time.sleep(randomNumbers.waitToLoadPage())

            body = driver.find_element(by=By.TAG_NAME, value="body")

            number_scrolling = randomNumbers.scrollingNumber()
            print(f"Broj skrolovanja: {number_scrolling}")


            # probati preko taga
            likes_button = driver.find_element(by=By.XPATH, value=XPaths.LIKES_OF_PICTURE)

            try:
                print("Broj lajkova: " + likes_button.text)
                likes_button.click()
            except Exception as e:
                printExceptionDetails()
                print("Korisnik onemogucio broj lajkova!")
                continue

            try:
                likes_list = driver.find_element_by_css_selector(ClassNames.SCROLL_BOX_LIKES)
                likes_list = likes_list.find_element(by=By.TAG_NAME, value='div')

                while number_watched < number_stories and number_scrolling > 0:
                    time.sleep(randomNumbers.waitToLoadPage())

                    stories = likes_list.find_elements(by=By.TAG_NAME, value='span')
                    stories = [storie for storie in stories if ClassNames.STORIE in storie.get_attribute("class")]
                    print(f"Pronadjeno {len(stories)} prica")

                    for storie in stories:

                        print("Kliknut stori!")
                        print(f"Element: {storie.text}, tagname: {storie.tag_name}")

                        storie.click()
                        time.sleep(randomNumbers.watchStorie())
                        body.send_keys(Keys.ARROW_UP)

                        likes_list = driver.find_element_by_css_selector(ClassNames.SCROLL_BOX_LIKES)
                        likes_list = likes_list.find_element(by=By.TAG_NAME, value='div')
                        driver.execute_script("arguments[0].scrollIntoView();", storie)

                        number_watched = number_watched + 1
                        time.sleep(randomNumbers.waitToLoadPage())

                    self.temp_watched = self.temp_stories + number_watched

                    if self.temp_stories == self.max_watched:
                        return


                    number_scrolling = number_scrolling - 1

                if number_watched == number_stories:
                    return

            except Exception as e:
                printExceptionDetails()
                print("Nije pronadjena lista ili greska u spanu za stori!")
                continue




