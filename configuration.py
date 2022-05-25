import os


class Configuration:

    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:root@:3306/database"

    CHROMEDRIVER_PATH = os.path.realpath(os.path.join(os.path.dirname(__file__), 'webScraping', 'chromeDriver', 'chromedriver.exe'))
    USER_STATISTIC_DIR_PATH = os.path.realpath(os.path.join(os.path.dirname(__file__), 'webScraping', 'data', 'statistic.json'))
    FOLLOWED_USERNAMES_FILE_PATH = os.path.realpath(os.path.join(os.path.dirname(__file__), 'webScraping', 'data', 'followed_usernames.json'))
    UNFOLLOWED_USERNAMES_FILE_PATH = os.path.realpath(os.path.join(os.path.dirname(__file__), 'webScraping', 'data', 'unfollowed_usernames.json'))
    WEBDRIVER_FILE_PATH = os.path.realpath(os.path.join(os.path.dirname(__file__), 'webScraping', 'data', 'webdriver.json'))
    COOKIES_FILE_PATH = os.path.realpath(os.path.join(os.path.dirname(__file__), 'webScraping', 'data', 'cookies.json'))

    BLUE_COLOR_FOLLOW_BUTTON = "rgba(0, 149, 246, 1)"
    WHITE_COLOR_FOLLOW_BUTTON = "rgba(0, 0, 0, 0)"

    USERNAME = "dd4085222"
    PASSWORD = "newpassword.1"


    #USERNAME = "sto_photo_"
    #PASSWORD = "feelgood.007"

