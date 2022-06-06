import random


#vraca koliko ce pratilaca sa jedne slike zapratiti
def followNumberOneTry():
    return random.randint(3, 6)


def storiesNumberOneTry():
    return random.randint(2, 5)


def numberForWaitScrollingList():
    return random.randint(3, 6)


def waitToLoadPage():
    return random.randint(3, 6)


def scrollingNumber():
    return random.randint(5, 10)


def watchStorie():
    return random.randint(7, 15)


#vraca slucajan broj izmedju 0 i 1
def secondForWaitFollow():
    return random.uniform(0.5, 2)


#izmedju 30 i 45min
def secondForWaitFollowPeriodicCall():
    return random.randint(1800, 2700)


def nextStorie():
    return random.randint(2, 7)


def numberStories():
    return random.randint(3, 6)

def ordinalNumberPic(max):
    return random.randint(0, max)

def secondForWaitLike():
    return random.randint(2, 5)

