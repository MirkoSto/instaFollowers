import time
import json

from selenium.webdriver import Keys
from selenium.webdriver.common.by import By

from threading import Thread

from configuration import Configuration
from webScraping.scripts.randomNumbers import numberStories, nextStorie, ordinalNumberPic
from webScraping.strings.classNamesCSS import ClassNames

from webScraping.scripts.webdriverInstance import WebDriverInstance
from webScraping.strings.xpaths import XPaths
from webScraping.strings.urls import URL

from webScraping.scripts.webUtility import showPictureByTag, findFollowButtonsAndUsernames, getPicturesForTag, \
    get_cookies, set_cookies, getUsersPics, getTagPics
from webScraping.scripts.utility import getUnfollowedUsernames, getStatisticData, updateFollowedUsernames, \
    getFollowedUsernames, getFromStatistic, updateStatisticDataFollow, updateLikedPics, updateStatisticDataLike

from webScraping.scripts import randomNumbers

print(Configuration.CHROMEDRIVER_PATH)

# TODO: za svako vreme cekanja genersiati random broj sekundi
#  omoguciti random skrolovanje gore-dole pre neke akcije, sacekati neko vreme pre preuzimanja akcije
#  gledati sliku neko vreme

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

        self.started_periodic_calls = False

        #self.login_thread = Thread(target=self.login, args=())
        #self.follow_thread = Thread(target=self.follow, args=())
        #self.watch_thread = Thread(target=self.watchStories, args=())

        self.login_with_cookies(self.driver)


    #TODO: napraviti proveru da li su tacni kredencijali
    def login(self):
        print("Logovanje...")

        statistic_dir = Configuration.USER_STATISTIC_DIR_PATH
        driver = self.driver

        failed = self.login_with_cookies(driver)

        #ako nema kolacica
        if failed:
            try:
                #vec je ucitana stranica
                #driver.get(URL.INSTAGRAM_LOGIN)
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

            #ako je failed = False, zavrsava se funkcija i vraca se odgovor da je neuspelo logovanje
            if not failed:

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

                    data["logged"] = True
                    data["username"] = self.username
                    with open(statistic_dir, 'w') as file:
                        json.dump(data, file)

                    self.followers_following()

                    #preuzimanje kolacica
                    get_cookies(driver)



        #osvezavanje kolacica
        else:
            get_cookies(driver)



    #vraca vrednost failed
    def login_with_cookies(self, driver):
        # dodavanje kolacica

        has_cookies = set_cookies(driver)

        if has_cookies:
            driver.get(URL.INSTAGRAM)
            self.logged = True
            return False

        else:
            return True


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


    def preparingForFollowingOrLiking(self, driver, tag):
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

            pic_hrefs = getTagPics(driver)

            if not showPictureByTag(driver, pic_hrefs):
                return False, [], []

        except Exception as e:
            print(e)
            return False, [], []

        return True, followed, pic_hrefs

    #vraca broj zapracenih korisnika
    def follow(self, index):
        print("Priprema za pracenje...")
        driver = self.driver


        try:

            #ako dodje do greske u pripremi, izlazi iz fje
            success, followed, pic_hrefs = self.preparingForFollowingOrLiking(driver, self.follow_tags[index])
            if not success:
                return 0

            follow_buttons, follow_usernames = findFollowButtonsAndUsernames(driver)
            new_followed = []

            number_follows = randomNumbers.followNumberOneTry()
            if self.temp_followed + number_follows > self.max_followed:
                number_follows = self.max_followed - self.temp_followed

            print(f"Broj pracenja u ovom zahtevu: {number_follows}")

            i = -1
            while i < number_follows:
                i = i + 1

                button_color = follow_buttons[i].value_of_css_property("background-color")
                print("Color: " + button_color)
                print(follow_buttons[i].text)

                # ako je dugme plavo i ako nije nekad pre zapratio --> zaprati
                if button_color != Configuration.WHITE_COLOR_FOLLOW_BUTTON and follow_usernames[i] not in followed:
                    self.temp_followed = self.temp_followed + 1

                    #follow_buttons[i].click()
                    new_followed.append(follow_usernames[i])
                    print(f"Zapracen {follow_usernames[i]}!")

                    # ako je dostignuta kvota pracenja za taj dan, prekini pracenje
                    if self.max_followed == self.temp_followed:
                        break

                    time.sleep(randomNumbers.secondForWaitFollow())



            if len(new_followed) > 0:
                updateFollowedUsernames(new_followed)
                updateStatisticDataFollow(self.temp_followed)

            print(f"Zapraceno {self.temp_followed} od {number_follows}")
            return self.temp_followed

        except Exception as e:
            print(e)


    #TODO: kretati se kroz listu korisnika koje pratimo i proveravati kad se naidje na korisnika koji treba da se otprati,
    # kako bi se ponasalo realno ponasanje korisnika na platformi
    def unfollow(self):
        driver = self.driver

        try:
            driver.get(URL.INSTAGRAM + Configuration.USERNAME)
            time.sleep(5)

        except Exception as e:
            print(e)


    #TODO: obezbediti da predje na sledecu sliku sa taga, ako nema dovoljno otkljucanih korisnika na prethodnoj slici
    # i obezbediti da ne ulazi u sliku u kojoj je vec bio (ne treba pamtiti dugo te slike!)

    #ne lajkuje slike korisnika koje ne prati
    def like(self, index):
        print("Priprema za lajkovanje...")
        driver = self.driver

        liked_pics = []

        try:


            #ako dodje do greske u pripremi, izlazi iz fje
            success, followed, pic_hrefs = self.preparingForFollowingOrLiking(driver, self.like_tags[index])
            if not success:
                return 0

            follow_buttons, like_usernames = findFollowButtonsAndUsernames(driver)

            number_likes = randomNumbers.followNumberOneTry()
            if self.temp_followed + number_likes > self.max_followed:
                number_likes = self.max_liked - self.temp_liked

            print(f"Broj korisnika za lajkovanje u ovom zahtevu: {number_likes}")

            for username in like_usernames:

                driver.get(URL.INSTAGRAM + username)

                users_pics = getUsersPics(driver)
                if len(users_pics) == 0:
                    continue

                pic_number = ordinalNumberPic(len(users_pics) - 1)
                driver.get(users_pics[pic_number])

                like_button = driver.find_element(by=By.CLASS_NAME, value=ClassNames.LIKE_SPAN)
                like_button = like_button.find_element(by=By.TAG_NAME, value='Button')

                button_color = like_button.value_of_css_property('color')
                print("Boja dugmeta: " + button_color)

                # ako nije vec lajkovano
                if button_color != Configuration.RED_COLOR_LIKE_BUTTON and username not in followed:
                    self.temp_liked = self.temp_liked + 1

                    like_button.click()
                    liked_pics.append(users_pics[pic_number])
                    print(f"Lajkovana slika {users_pics[pic_number]}!")

                    if self.temp_liked == number_likes:
                        break

                    time.sleep(randomNumbers.secondForWaitFollow())

            if len(liked_pics) > 0:
                updateLikedPics(liked_pics)
                updateStatisticDataLike(self.temp_liked)

            print(f"Lajkovano {self.temp_liked} od {number_likes}")
            return self.temp_followed

        except Exception as e:
            print(e)

            if len(liked_pics) > 0:
                updateLikedPics(liked_pics)
                updateStatisticDataLike(self.temp_liked)
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
            storie = driver.find_element(by=By.CLASS_NAME, value=ClassNames.STORIE_FOLLOWING)
            storie.click()
            time.sleep(2)
        except Exception as e:
            print(e)
            print("Greska pri ulasku na stori!")
            return 0


        number_stories = numberStories()
        print("Treba da odgleda " + str(number_stories) + " storija!")

        page_body = driver.find_element(by=By.TAG_NAME, value="body")
        for i in range(0, number_stories):
            watch_time = nextStorie()
            print("Gledace " + str(watch_time) + " sekundi")
            time.sleep(watch_time)
            page_body.send_keys(Keys.ARROW_RIGHT)

            self.temp_watched = self.temp_watched + 1

        page_body.send_keys(Keys.ARROW_UP)
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

                    self.temp_watched = self.temp_stories + number_watched

                    if self.temp_stories == self.max_watched:
                        return


                    number_scrolling = number_scrolling - 1

                if number_watched == number_stories:
                    return

            except Exception as e:
                print(e)
                print("Nije pronadjena lista ili greska u spanu za stori!")
                continue




