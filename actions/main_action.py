import os, datetime

from pymongo import MongoClient

from dotenv import find_dotenv, load_dotenv
load_dotenv(find_dotenv())

HOST = os.getenv('HOST')
PORT = int(os.getenv('PORT'))

# Подключение к БД
client = MongoClient(HOST, PORT)
db = client.test
coll = db.sample_collection

# Пример запроса 
dt_from = "2022-09-01T00:00:00"
dt_upto = "2022-12-31T23:59:00"
group_type = "month"

# Переформатирование даты из запроса
dt_format = "%Y-%m-%dT%H:%M:%S"
query_dt_from = datetime.datetime.strptime(dt_from, dt_format)
query_dt_upto = datetime.datetime.strptime(dt_upto, dt_format)

# Подготовка условий для запроса в БД
condition_from = {"dt": {"$gte": query_dt_from}}
condition_upto = {"dt": {"$lte": query_dt_from}}
condition_group = {
    "_id": {"$month": "dt"}, 
    "total_value": {"$sum": "$value"}
    }