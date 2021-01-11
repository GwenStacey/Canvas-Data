import os
import json
import sqlite3
import requests
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("API-KEY")
headers = {"Authorization":
           f"Bearer {api_key}"}

conn = sqlite3.Connection("users_db.sqlite3")

def get_users():
    """
    Returns a list ready to be made into a dataframe
    of user objects from Canvas API
    This method insures all pages of data are grabbed
    """
    data_set = []
    r = requests.get("https://lambdaschool.instructure.com/api/v1/accounts/1/users", headers=headers)

    if "next" in r.links.keys():
        while "next" in r.links.keys():
            r = requests.get(r.links["next"]["url"], headers=headers)
            raw = r.json()
            for user in raw:
                data_set.append(user)
        if "last" in r.links.keys() and r.links['current']['url'] == r.links['last']['url']:
            print('Done!')
    else:
        print("Just one page!")
    return data_set

users = pd.DataFrame(get_users())
#remove extranneous features
users = users[["id", "name", "sis_user_id"]]
#replaces previous table with new version simplest
#way to go from canvas data to ours, while making sure
#we have no double entries
users.to_sql("USERS", conn, if_exists="replace", index=False)