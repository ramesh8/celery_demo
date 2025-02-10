from fastapi import BackgroundTasks, FastAPI, Request
import csv
from pymongo import MongoClient
import random
import time
import os
from worker import process_row


app = FastAPI()



def record_task(tid):
    mongo = MongoClient("mongodb://mongodbserver:27017/")
    tdb = mongo["test"]
    tasks = tdb["tasks"]
    res = tasks.insert_one({"task_id":tid})
    return "task initiated"

def processData():
    fname = "data/countries.csv"
    with open(fname, 'r') as cf:
        creader = csv.reader(cf)
        for row in creader:
            rnd = random.randint(10,100)
            task = process_row.delay(row, rnd)
            record_task(task.id)


@app.get("/")
def home(request:Request):
    return "Welcome"

@app.get("/task")
def task(bgtask:BackgroundTasks, request:Request):
    tid = processData()
    return "background task added"