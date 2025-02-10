from celery import Celery
import time
from pymongo import MongoClient
import os

celery = Celery(__name__)
celery.conf.broker_url = os.environ.get("CELERY_BROKER_URL", "redis://redis:6379")
celery.conf.result_backend = os.environ.get("CELERY_RESULT_BACKEND", "redis://redis:6379")


@celery.task(name="process_row")
def process_row(r, s):
    time.sleep(s) # simulates a long task which takes random time
    mongo = MongoClient("mongodb://mongodbserver:27017/")
    tdb = mongo["test"]
    ctry = tdb["countries"]
    d = {"country":r[0],"latitude":r[1],"longitude":r[2],"name":r[3]}
    res = ctry.insert_one(d)
    return res.inserted_id == None