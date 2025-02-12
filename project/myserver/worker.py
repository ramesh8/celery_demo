import random
import signal
from celery import Celery
import time
from pymongo import MongoClient
import os
from kombu import Queue

celery = Celery(__name__)
celery.conf.broker_url = os.environ.get("CELERY_BROKER_URL", "redis://redis:6379")
celery.conf.result_backend = os.environ.get("CELERY_RESULT_BACKEND", "redis://redis:6379")
celery.conf.task_send_sent_event = True
celery.conf.task_track_started = True
celery.conf.imports = (
    "worker"
)
celery.conf.task_queues = (
    Queue("mytasks", routing_key="mytasks"),
)
celery.conf.default_queue = "mytasks"
celery.conf.default_exchange = "tasks"
celery.conf.default_exchange_type = "direct"
celery.conf.default_routing_key = "mytasks"

celery.conf.task_routes = {
    "worker.*": {"queue": "mytasks"},
}

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

@celery.task(name="critical_task", autoretry_for=(Exception,), retry_kwargs={'max_retries':3})
def critical_task():
    """Will always fail/retry until max_retries"""
    raise Exception("I will fail, but retry")

@celery.task(autoretry_for=(Exception,), retry_kwargs={'max_retries': 3}, expires=120)
def will_expire_task():
    """Will fail/retry/.../expire"""
    raise Exception("I will certainly expire")

@celery.task()
def will_terminate_task():
    """Will be terminated"""
    celery.control.revoke(will_terminate_task.request.id, terminate=True, signal=signal.SIGTERM)
    time.sleep(10)


@celery.task(autoretry_for=(Exception,), retry_kwargs={'max_retries': 3})
def recovered_task():
    """Will fail/retry/.../succeed"""
    if recovered_task.request.retries > 1:
        return "I'm a survival"
    raise Exception("I'm retrying my self")

def run_stasks():
    critical_task.delay()
    will_expire_task.delay()
    will_terminate_task.delay()
    recovered_task.delay()