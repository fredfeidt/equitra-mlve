from datetime import date 
from shutil import copytree
import schedule
import time
import os

outputpath = "backup"
temp = "data/temp/"

def today():
    today = date.today()
    return today

def weekly():
    # BACKUP
    copytree("./data", f"{outputpath}/{today()}/data/") # Copy all data | Alternative: copy_tree("./", f"{outputpath}/{today()}/") # Copy whole dir

def daily():
    # DELETE TEMP FILES
    for f in os.listdir(temp):
        os.remove(os.path.join(temp, f))

schedule.every().monday.at('00:00').do(weekly)
schedule.every().day.at('00:00').do(daily)

while True:
    schedule.run_pending()
    time.sleep(1)