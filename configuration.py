import os


class Configuration:

    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:root@:3306/database"

    CHROMEDRIVER_PATH = os.path.realpath(os.path.join(os.path.dirname(__file__), 'webScraping', 'chromeDriver', 'chromedriver.exe'))
    USER_STATISTIC_DIR_PATH = os.path.realpath(os.path.join(os.path.dirname(__file__), 'webScraping', 'data', 'statistic.json'))
    FOLLOWED_USERNAMES_FILE_PATH = os.path.realpath(os.path.join(os.path.dirname(__file__), 'webScraping', 'data', 'followed_usernames.json'))
    UNFOLLOWED_USERNAMES_FILE_PATH = os.path.realpath(os.path.join(os.path.dirname(__file__), 'webScraping', 'data', 'unfollowed_usernames.json'))
    WEBDRIVER_FILE_PATH = os.path.realpath(os.path.join(os.path.dirname(__file__), 'webScraping', 'data', 'webdriver.json'))
    COOKIES_FILE_PATH = os.path.realpath(os.path.join(os.path.dirname(__file__), 'webScraping', 'data', 'cookies.json'))
    LIKED_PICTURES_FILE_PATH = os.path.realpath(os.path.join(os.path.dirname(__file__), 'webScraping', 'data', 'liked_pictures.json'))
    LIKED_USERNAMES_FILE_PATH = os.path.realpath(os.path.join(os.path.dirname(__file__), 'webScraping', 'data', 'liked_usernames.json'))
    WATCHED_USERNAMES_FILE_PATH = os.path.realpath(os.path.join(os.path.dirname(__file__), 'webScraping', 'data', 'watched_usernames.json'))
    USER_PROFILE_PICTURE_FILE_PATH = os.path.realpath(os.path.join(os.path.dirname(__file__), 'webScraping', 'data', 'profile_picture.png'))
    ACTIONS_FILE_PATH = os.path.realpath(os.path.join(os.path.dirname(__file__), 'webScraping', 'data', 'actions.json'))


    BLUE_COLOR_FOLLOW_BUTTON = "rgba(0, 149, 246, 1)"
    WHITE_COLOR_FOLLOW_BUTTON = "rgba(0, 0, 0, 0)"

    RED_COLOR_LIKE_BUTTON = "rgb(237, 73, 86)"


    USERNAME2 = "mirko_stojanovic_"
    USERNAME = "dd4085222"
    PASSWORD = "newpassword.1"


