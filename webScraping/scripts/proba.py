import datetime
import json
import os


starting_actions = datetime.datetime.today()
ending_actions = starting_actions + datetime.timedelta(days=1)

startingTimePermission = datetime.datetime.fromisoformat(getStartingPermission())

print(starting_actions)

print(ending_actions)

print(startingTimePermission)

print(starting_actions < startingTimePermission)