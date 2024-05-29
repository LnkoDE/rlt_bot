import os, datetime, json

import pandas
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
    # Функция для выбора типа группировки
    def return_condition_group():
        if group_type == "hour":
            condition_dt = {"$dateTrunc":{"date": "$dt", "unit": "hour"}}
        elif group_type == "day":
            condition_dt = {"$dateTrunc":{"date": "$dt", "unit": "day"}}
        elif group_type == "month":
            condition_dt = {"$dateTrunc":{"date": "$dt", "unit": "month"}}
        else:
            raise TypeError
        condition_group = {"_id": condition_dt, "total_value": {"$sum": "$value"}}
        return condition_group
    
    def return_delta(count):
        if group_type == "hour":
            delta = pandas.offsets.DateOffset(hours=count)
        elif group_type == "day":
            delta = pandas.offsets.DateOffset(days=count)
        elif group_type == "month":
            delta = pandas.offsets.DateOffset(months=count)
        else:
            raise TypeError
        return delta 
        
    
    # Переформатирование даты из запроса
    dt_format = "%Y-%m-%dT%H:%M:%S"
    query_dt_from = datetime.datetime.strptime(dt_from, dt_format)
    query_dt_upto = datetime.datetime.strptime(dt_upto, dt_format)

    # Подготовка условий для запроса в БД
    condition_from = {"dt": {"$gte": query_dt_from}}
    condition_upto = {"dt": {"$lte": query_dt_upto}}
    condition_group = return_condition_group()

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
    count = 0
    for data in list_aggr:
        dataprep = list(data.values())
        dt = dataprep[0]
        delta = return_delta(count)
        dt_check = query_dt_from + delta     
  
        while dt_check < dt:
            count += 1
            values = 0
            dt_str = datetime.datetime.strftime(dt_check, dt_format)
            delta = return_delta(count)
            dt_check = query_dt_from + delta
            labels.append(dt_str)
            dataset.append(values)

        values = dataprep[1]
        dt_str = datetime.datetime.strftime(dt, dt_format)

        count +=1
        labels.append(dt_str)
        dataset.append(values)

    if return_delta(count=1) + dt <= query_dt_upto:
        while dt_check < query_dt_upto:
            values = 0
            delta = return_delta(count)
            dt_check = query_dt_from + delta
            dt_str = datetime.datetime.strftime(dt_check, dt_format)
            count +=1
            labels.append(dt_str)
            dataset.append(values)        

    answer = {"dataset": dataset, "labels": labels}
    return json.dumps(answer)