import json
import time

from selenium.webdriver.common.actions.action_builder import ActionBuilder
from selenium.webdriver.common.actions.mouse_button import MouseButton
from selenium.webdriver.common.by import By

from configuration import Configuration

from webScraping.scripts import randomNumbers
from webScraping.scripts.utility import printExceptionDetails
from webScraping.strings.urls import URL
from webScraping.strings.xpaths import XPaths

from webScraping.strings.classNamesCSS import ClassNames

#TODO: "realnije" traziti slike

#TODO: kolacici isticu posle 19 dana otprilike, tada ce morati ponovo da se uloguje

#set from driver in file
def set_cookies(driver):
    driver.get(URL.INSTAGRAM_LOGIN)
    time.sleep(5)

    with open(Configuration.COOKIES_FILE_PATH, 'r') as file:
        cookies = json.load(file)

    if len(cookies) == 0:
        return False

    for cookie in cookies:
        driver.add_cookie(cookie)

    return True


#get from driver
def get_cookies(driver):
    cookies = driver.get_cookies()
    print(cookies)
    with open(Configuration.COOKIES_FILE_PATH, 'w') as file:
        json.dump(cookies, file)



def getPicturesForTag(driver):
    num_err = 0

    while num_err < 5:
        try:

            hrefs_in_view = driver.find_elements_by_tag_name('a')
            # finding relevant hrefs
            hrefs_in_view = [elem.get_attribute('href') for elem in hrefs_in_view if '/p/' in elem.get_attribute('href')]

            return hrefs_in_view
        except Exception as e:
            # ako se vise od pet puta uzastopno desi greska, da ne bi doslo do beskonacnog vrtenja
            if num_err == 5:
                return []

            print(e)
            num_err = num_err + 1



def scrollWindow(driver, className):

    window = driver.find_element(by=By.CLASS_NAME, value=className)
    driver.execute_script(
        "arguments[0].scrollTo(0, arguments[0].scrollHeight); return arguments[0].scrollHeight", window)

#ne koristi se vise ova fja
def findStories(liked_list):
    print("Loading follow button-a...")

    try:
        stories = liked_list.find_elements(by = By.CLASS_NAME, value = ClassNames.STORIE)
        stories = [storie for storie in stories if storie.tag_name == "span"]

        return stories

    except Exception as e:
        printExceptionDetails()
        return []



def showPictureByTag(driver, hrefs_in_view):
    num_err = 0

    while num_err < 5:
        exit = False
        try:

            i = 0
            for pic_href in hrefs_in_view:
                if i == len(hrefs_in_view):
                    exit = True
                    break

                i = i + 1

                driver.get(pic_href)
                time.sleep(5)

                try:
                    # probati preko taga
                    likes_button = driver.find_element(by=By.CLASS_NAME, value=ClassNames.LIKES_OF_PICTURE)

                    print("Broj lajkova: " + likes_button.text)
                    #int(likes_button.text)
                    likes_button.click()
                    time.sleep(2)

                    return True
                except Exception as e:
                    print(e)
                    print("Korisnik onemogucio broj lajkova!")
                    num_err = num_err + 1
                    continue

            if exit:
                break


        except Exception as e:
            if num_err == 5:
                return False

            printExceptionDetails()  # ako se vise od pet puta desi greska, da ne bi doslo do beskonacnog vrtenja
            num_err = num_err + 1


def showPictureByHref(driver, href):
    driver.get(href)
    time.sleep(3)

    # probati preko taga
    likes_button = driver.find_element(by=By.CLASS_NAME, value=ClassNames.LIKES_OF_PICTURE)

    try:

        print("Broj lajkova: " + likes_button.text)
        likes_button.click()
        time.sleep(2)

        return True
    except Exception as e:
        printExceptionDetails()
        print("Korisnik onemogucio broj lajkova!")



def getTagPics(driver):
    hrefs_in_view = driver.find_elements_by_tag_name('a')
    # finding relevant hrefs
    hrefs_in_view = [elem.get_attribute('href') for elem in hrefs_in_view if '/p/' in elem.get_attribute('href')]

    return hrefs_in_view

def getUsersPics(driver):
    try:

        hrefs_in_view = driver.find_elements_by_tag_name('a')
        hrefs_in_view = [elem.get_attribute('href') for elem in hrefs_in_view if '/p/' in elem.get_attribute('href')]

        print(f"Pronadjeno {len(hrefs_in_view)} slika!")

        return hrefs_in_view

    except Exception as e:
        print(e)
        return []


def findFollowButtonsAndUsernames(driver):
    print("Loading follow button-a...")
    buttons = []
    usernames = []
    try:

        scroll_box = driver.find_element(by = By.CLASS_NAME, value = ClassNames.USERS_LIKED_LIST)

        new_buttons = scroll_box.find_elements(by = By.TAG_NAME, value = "button")
        new_usernames = scroll_box.find_elements(by = By.TAG_NAME, value = "a")

        [buttons.append(button) for button in new_buttons if button not in buttons]

        [usernames.append(username.text) for username in new_usernames if username.text not in usernames and username.text != '']

        print(f"Broj korisnika: {len(usernames)}")
        print(f"Broj dugmica {len(buttons)}")


        print(usernames)
        [print(button.text) for button in buttons]

        return buttons, usernames
    except Exception as e:
        printExceptionDetails()
        return [], []


def findUnfollowButtonsAndUsernames(driver):
    print("Loading following usernames...")


    try:

        following_list = driver.find_element(by=By.CLASS_NAME, value=ClassNames.FOLLOWING_LIST)
        items = following_list.find_elements(by=By.TAG_NAME, value="a")

        buttons = following_list.find_elements(by=By.TAG_NAME, value="button")

        following_usernames = [elem.get_attribute('href') for elem in items]
        following_usernames = [username.removeprefix("https://www.instagram.com/") for username in following_usernames]
        following_usernames = [username.removesuffix("/") for username in following_usernames]

        usernames = []
        for username in following_usernames:
            if username not in usernames:
                usernames.append(username)

        print(f"Broj korisnika: {len(usernames)}")
        print(f"Broj dugmica: {len(buttons)}")
        print(usernames)
      #  for button in buttons:
        #    print(button.text)


        return usernames, buttons

    except Exception as e:
        printExceptionDetails()

        return [], []


def clickAtPoint(driver, x, y):
    action = ActionBuilder(driver)
    action.pointer_action.move_to_location(x, y)
    action.pointer_action.pointer_down(MouseButton.LEFT)
    action.pointer_action.pointer_up(MouseButton.LEFT)
    action.perform()
    time.sleep(5)
