from selenium.webdriver import Keys
from selenium.webdriver.common.by import By

import time
import json
from threading import Thread

from configuration import Configuration
from webScraping.scripts.classNamesCSS import ClassNames

from webScraping.scripts.webdriverInstance import WebDriverInstance
from webScraping.scripts.xpaths import XPaths
from webScraping.scripts.urls import URL

from webScraping.scripts.webUtility import showPicture, findFollowButtons, scrollWindow, getPicturesForTag
from webScraping.scripts.utility import getUnfollowedUsernames, getStatisticData, updateFollowedUsernames, \
    getFollowedUsernames

from webScraping.scripts import randomNumbers

print(Configuration.CHROMEDRIVER_PATH)

# TODO: za svako vreme cekanja genersiati random broj sekundi
# TODO: omoguciti random skrolovanje gore dole pre neke akcije, sacekati neko vreme pre preuzimanje akcije
# TODO: gledati sliku neko vreme

#TODO: staviti logovanje u funckiju koja ce pozivati sve ove akcije (PeriodicCalls, ako bude i dalje namenjena za to)



class InstagramClient:

    def __init__(self):

        self.driver = WebDriverInstance()

        self.username = Configuration.USERNAME
        self.password = Configuration.PASSWORD

        self.logged = False
        self.tag = ""

        self.max_liked = None
        self.max_stories = None
        self.max_unfollowed = None
        self.max_followed = None
        self.max_commented = None
        self.temp_followed = 0
        self.temp_unfollowed = 0
        self.temp_stories = 0
        self.temp_liked = 0
        self.temp_commented = 0

        self.initStatisticData()

        self.login_thread = Thread(target=self.login, args=())
        self.follow_thread = Thread(target=self.follow, args=())
        self.watch_thread = Thread(target=self.watchStories, args=())


    def initStatisticData(self):
        data = getStatisticData()

        self.max_followed = data.get("max_followed")
        self.max_unfollowed = data.get("max_unfollowed")
        self.max_stories = data.get("max_stories")
        self.max_liked = data.get("max_liked")
        self.max_commented = data.get("max_commented")




    #TODO: napraviti proveru da li su tacni kredencijali
    def login(self):
        print("Logovanje...")

        driver = self.driver

        try:
            driver.get(URL.INSTAGRAM_LOGIN)
            # print(self.driver.page_source)

            driver.implicitly_wait(10)
            user_name_elem = driver.find_element(by=By.XPATH, value=XPaths.LOGIN_USERNAME)
            user_name_elem.clear()
            user_name_elem.send_keys(self.username)
            pass_elem = driver.find_element(by=By.XPATH, value=XPaths.LOGIN_PASSWORD)
            pass_elem.clear()
            pass_elem.send_keys(self.password)
            button = driver.find_element(by=By.XPATH, value=XPaths.LOGIN_SUBMIT_BUTTON)
            button.click()

            # TODO: proveriti neuspelo logovanje

            time.sleep(5)
            self.logged = True
            WebDriverInstance.logged = True

            statistic_dir = Configuration.USER_STATISTIC_DIR_PATH

            with open(statistic_dir) as file:
                data = json.load(file)

            data["loggedIn"] = True

            with open(statistic_dir, 'w') as file:
                json.dump(data, file)


        except Exception as e:
            print(str(e))

    def followers_following(self):
        print("Dohvatanje broja pratilaca")

        driver = self.driver
        # TODO: moze se proveriti ako je na pocetnoj strani korisnika da je ne ucitava ponovo!
        driver.get(URL.INSTAGRAM + Configuration.USERNAME)
        time.sleep(5)

        followers_number = driver.find_element(by=By.XPATH, value=XPaths.FOLLOWERS_NUMBER).text
        following_number = driver.find_element(by=By.XPATH, value=XPaths.FOLLOWING_NUMBER).text

        print("Broj pratilaca: " + followers_number)
        print("Broj pracenja: " + following_number)

        statistic_dir = Configuration.USER_STATISTIC_DIR_PATH

        with open(statistic_dir, 'r') as file:
            data = json.load(file)

        if (data is None):
            print("Error: data from statistic.json is None!")

            data = {
                "followers_number": followers_number,
                "following_number": following_number
            }

        data["followers_number"] = followers_number
        data["following_number"] = following_number

        with open(statistic_dir, 'w') as file:
            json.dump(data, file)

    #vraca broj zapracenih korisnika
    def follow(self):
        print("Priprema za pracenje...")
        driver = self.driver
        unfollowed_usernames = getUnfollowedUsernames()
        followed = getFollowedUsernames()

        #lista koja sadrzi imena korisnika koje ne treba vise pratiti
        [followed.append(username) for username in unfollowed_usernames]

        print("Vec zapraceni korisnici: ")
        print(followed)

        if not self.logged:
            self.login()

        try:
            print(f"Tag sa pracenje: {self.tag}")
            driver.get(URL.TAG_SEARCH + self.tag)

            if not showPicture(driver):
                return 0

            follow_buttons, follow_usernames = findFollowButtons(driver)
            new_followed = []

            #TODO: resiti problem sa importovanjem
            number_follows = randomNumbers.followNumberOneTry()
            print(f"Broj pracenja u ovom zahtevu: {number_follows}")

            for i in range(0, number_follows):

                button_color = follow_buttons[i].value_of_css_property("background-color")
                print("Color: " + button_color)
                print(follow_buttons[i].text)

                # ako je dugme plavo --> zaprati i ako nije nekad pre zapratio
                if button_color == Configuration.BLUE_COLOR_FOLLOW_BUTTON and follow_usernames[i] not in followed:
                    self.temp_followed = self.temp_followed + 1
                    #TODO: otkomentarisati liniju ispod na kraju testiranja
                    #follow_buttons[i].click()
                    new_followed.append(follow_usernames[i])
                    print(f"Zapracen {follow_usernames[i]}!")

                    # ako je dostignuta kvota pracenja za taj dan, prekini pracenje
                    if self.max_followed == self.temp_followed:
                        break

                    time.sleep(0.4)

                #ako je ispunjen broj pracenja za jedan zahtev
                if self.temp_followed == number_follows:
                    break

            if len(new_followed) > 0:
                updateFollowedUsernames(new_followed)


            print(f"Zapraceno {self.temp_followed} od {number_follows}")
            return self.temp_followed

            #TODO: preci na izvrsavanje svakodnevnih akcija
            # na neko vreme, pa se vratiti na pracenje dok ne predje kvotu


        except Exception as e:
            print(e)


    #TODO: kretati se kroz listu korisnika koje pratimo i proveravati kad se naidje na korisnika koji treba da se otprati,
    # kako bi se ponasalo realno ponasanje korisnika na platformi
    def unfollow(self):
        driver = self.driver

        if not self.logged:
            self.login()

        try:
            driver.get(URL.INSTAGRAM + Configuration.USERNAME)
            time.sleep(5)

        except Exception as e:
            print(e)


    #vraca broj odgledanih storija u jednom zahtevu
    #ne mora da vraca, ima vec u instagramClient instanci temp atribut!!
    def watchStories(self):
        driver = self.driver

        if not self.logged:
            self.login()

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
                print(e)
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

                    self.temp_stories = self.temp_stories + number_watched

                    if self.temp_stories == self.max_stories:
                        return


                    number_scrolling = number_scrolling - 1

                if number_watched == number_stories:
                    return

            except Exception as e:
                print(e)
                print("Nije pronadjena lista ili greska u spanu za stori!")
                continue


    def wathcFollowersStories(self):
        pass

