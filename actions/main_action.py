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

def aggregatedb_bygroup(dt_from, dt_upto, group_type):
    # Переформатирование даты из запроса
    dt_format = "%Y-%m-%dT%H:%M:%S"
    query_dt_from = datetime.datetime.strptime(dt_from, dt_format)
    query_dt_upto = datetime.datetime.strptime(dt_upto, dt_format)

    # Подготовка условий для запроса в БД
    condition_from = {"dt": {"$gte": query_dt_from}}
    condition_upto = {"dt": {"$lte": query_dt_upto}}
    condition_group = {
        "_id": {"$dateTrunc":{"date": "$dt", "unit": "month"}}, 
        "total_value": {"$sum": "$value"}
        }

    # Стадии конвейера
    match_stage = {"$match": 
                {"$and": [condition_from, condition_upto]}
                }
    group_stage = {"$group": condition_group}
    sort_stage = {"$sort": {"_id": 1}}

    # Конвейер для агрегации
    pipeline = [match_stage, group_stage, sort_stage]
    aggr = coll.aggregate(pipeline)
    list_aggr = list(aggr)

    # Формирование ответа на запрос
    dataset = []
    labels = []

    for data in list_aggr:
        dataprep = list(data.values())
        dt = dataprep[0]
        values = dataprep[1]
        dt_str = datetime.datetime.strftime(dt, dt_format)
        labels.append(dt_str)
        dataset.append(values)
    answer = {"dataset": dataset, "labels": labels}
    return answer