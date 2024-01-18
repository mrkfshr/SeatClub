import pip

import requests
import json

def fetch_json_from_github(url):
    response = requests.get(url)
    return response.json()

def personalize_questions(artist_name, questions):
    personalized_questions = []
    for question in questions:
        personalized_questions.append(question.replace("[name]", artist_name))
    return personalized_questions

