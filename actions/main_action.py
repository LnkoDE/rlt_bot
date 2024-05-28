import os
from pymongo import MongoClient

from dotenv import find_dotenv, load_dotenv
load_dotenv(find_dotenv())

HOST = os.getenv('HOST')
PORT = int(os.getenv('PORT'))

# Подключение к БД
client = MongoClient(HOST, PORT)
db = client.test
coll = db.sample_collection

