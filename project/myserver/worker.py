import random
from celery import Celery
import time
from pymongo import MongoClient
import os

celery = Celery(__name__)
celery.conf.broker_url = os.environ.get("CELERY_BROKER_URL", "redis://redis:6379")
celery.conf.result_backend = os.environ.get("CELERY_RESULT_BACKEND", "redis://redis:6379")

def record_task(tid):
    mongo = MongoClient("mongodb://mongodbserver:27017/")
    tdb = mongo["test"]
    tasks = tdb["tasks"]
    res = tasks.insert_one({"task_id":tid})
    return f"task {tid} initiated"

@celery.task(name="start_task_chain")
def start_task_chain(pages, s):
    #starting tasks
    time.sleep(s) # sim time taken to start task chain
    task = ct_group_pages.delay(pages,s)
    return record_task(task.id)

@celery.task(name="ct_group_pages")
def ct_group_pages(pages, s):
    time.sleep(s) # sim time taken to group pages
    groups = [[1,2],[3],[4,5],[6,7],[8,9,10]]
    # return groups
    for group in groups:
        rnd = random.randint(10,100)
        task = ct_process_group.delay(group,rnd)
        record_task(task.id)


@celery.task(name="ct_process_group")
def ct_process_group(group, s):
    time.sleep(s) # sim time taken to process group
    ents = { "in" : "1234", "id" : "01/01/2025", "ia" : 10.0, "group":group }
    return ents
