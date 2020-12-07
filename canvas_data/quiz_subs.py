import requests
import queries
import json
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("API-KEY")

headers = {"Authorization": 
           f"Bearer {api_key}"}
"""This portion just grabs the quiz_submissions, might want
to just change this and adjust the original scope for this file"""
r = requests.get(queries.quiz_submissions, headers=headers)

quiz_submissions = json.loads(r.text)

#print(quiz_submissions)

"""This portion focuses on getting data from the data
First we grab submissions to the quiz, including the history"""
r = requests.get('https://lambdaschool.instructure.com/api/v1'
'/courses/645/assignments/10773/submissions?include[]=submission_history/per_page=100', 
headers=headers)
#Read in the Json
quiz_questions=json.loads(r.text)
#Iterate over the json, checking for turn ins, and good ratings
for i in quiz_questions:
    if i['submission_history'][0]['submitted_at'] != None:
        if i['submission_history'][0]['submission_data'][0]['text'] == '3':
            print("Hurray")
        else:
            print(i['submission_history'][0]['submission_data'][0]['text'])
    else:
        print("Why no turn in?")