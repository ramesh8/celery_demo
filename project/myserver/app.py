from fastapi import BackgroundTasks, FastAPI, Request
import csv
from pymongo import MongoClient
import random
import time
import os
import json
from worker import start_task_chain, record_task, run_stasks

app = FastAPI()

def processData(fname):    
    with open(fname, 'r') as f:
        pages = json.load(f)
        rnd = random.randint(10,100)
        task = start_task_chain.delay(pages, rnd)
        record_task(task.id)

@app.get("/")
def home(request:Request):
    return "Welcome"

@app.get("/task")
def task(bgtask:BackgroundTasks, request:Request):
    fname = "sample_pages.json"
    tid = processData(f"data/{fname}")
    return "task chain added"

@app.get("/stasks")
def stasks(request:Request):
    run_stasks()
    return "special tasks started"