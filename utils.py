import certifi
from os import environ as env
from dotenv import find_dotenv, load_dotenv
from pymongo.mongo_client import MongoClient
import sys
import pymongo

ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)

MONGODB_PASS = env.get("MONGODB_PASSWORD")

uri = f"mongodb+srv://talkresearch:{MONGODB_PASS}@cluster0.kibxvyd.mongodb.net/?retryWrites=true&w=majority"

# Create a new client and connect to the server
client = MongoClient(uri, tlsCAFile=certifi.where())

db = client.talkresearch
users = db.users


def create_template(template):
    if template == 'blank':
        return ''
    with open(f'samples/{template}.html', 'r') as file:  # r to open file in READ mode
        html_as_string = file.read()
        file.close()
    return html_as_string


def create_doc(user, info):
    doc = {
        'user': user,
        'title': info[0],
        'template': info[1],
        'citation': info[2],
        'content': create_template(info[1])
    }

    new_doc = users.insert_one(doc)


def get_titles(user):
    titles = users.find({"user": user})
    return titles


def get_content(user, title):
    content = list(users.find(
        {
            "user": user,
            "title": title
         }
    ))

    return content[0]['content']


def save_content(user, title, content):
    search = {
            "user": user,
            "title": title
         }
    updated = users.update_one(search, {"$set": {"content": content}})


def delete_doc(object_id):
    deleted = users.delete_one({"_id": object_id})
    print(f"deleted: {deleted}")
