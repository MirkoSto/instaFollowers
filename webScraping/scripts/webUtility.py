import time
from selenium.webdriver.common.by import By
from webScraping.strings.classNamesCSS import ClassNames
from configuration import Configuration
from webScraping.scripts import randomNumbers

# TODO: "realnije" traziti slike
from webScraping.strings.xpaths import XPaths


def showPicture(driver):
    num_err = 0
    pic_hrefs = []

    while num_err < 5:
        try:
            #driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            #time.sleep(5)
            # get tags
            hrefs_in_view = driver.find_elements_by_tag_name('a')
            # finding relevant hrefs
            hrefs_in_view = [elem.get_attribute('href') for elem in hrefs_in_view if '/p/' in elem.get_attribute('href')]
            # building list of unique photos
            #[pic_hrefs.append(href) for href in hrefs_in_view if href not in pic_hrefs]

           # hrefs_in_view = ["https://www.instagram.com/p/CRe6Z1-LFNS/"]
            for pic_href in hrefs_in_view:
                driver.get(pic_href)
                time.sleep(3)

                #probati preko taga
                likes_button = driver.find_element(by=By.XPATH, value=XPaths.LIKES_OF_PICTURE)

                try:

                    print("Broj lajkova: " + likes_button.text)
                    #int(likes_button.text)
                    likes_button.click()

                    return True
                except Exception as e:
                    print(e)
                    print("Korisnik onemogucio broj lajkova!")
                    num_err = num_err + 1
                    continue


        except Exception as e:
            if num_err == 5:
                return False

            print(e)  # ako se vise od pet puta desi greska, da ne bi doslo do beskonacnog vrtenja
            num_err = num_err + 1


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



def scrollWindow(driver, window):
    driver.execute_script(
        "arguments[0].scrollTo(0, arguments[0].scrollHeight); return arguments[0].scrollHeight", window)


def findStories(liked_list):
    print("Loading follow button-a...")

    try:
        stories = liked_list.find_elements(by = By.CLASS_NAME, value = ClassNames.STORIE)
        stories = [storie for storie in stories if storie.tag_name == "span"]

        return stories

    except Exception as e:
        print(e)
        return []

def findFollowButtons(driver):
    print("Loading follow button-a...")
    buttons = []
    usernames = []
    try:

        scroll_box = driver.find_element(by = By.CLASS_NAME, value = ClassNames.SCROLL_BOX_LIKES)

        new_buttons = scroll_box.find_elements(by = By.TAG_NAME, value = "button")
        new_usernames = scroll_box.find_elements(by = By.TAG_NAME, value = "a")

        [buttons.append(button) for button in new_buttons if button not in buttons]

        [usernames.append(username.text) for username in new_usernames if username.text not in usernames and username.text != '']

        print(f"Broj korisnika: {len(usernames)}")
        print(f"Broj dugmica {len(buttons)}")


        print(usernames)

        return buttons, usernames
    except Exception as e:
        print(e)
        return [], []


def findFollowingUsernames(driver):
    print("Loading following usernames...")

    following_usernames = []

    try:
        hrefs = driver.find_elements_by_tag_name('a')
        following_list = [elem.get_attribute('href') for elem in hrefs if Configuration.USERNAME + "/following/" in elem.get_attribute('href')]
        print(str(len(following_list)))

        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(randomNumbers.numberForWaitScrollingList())


    except Exception as e:
        print(e)
        return following_usernames

