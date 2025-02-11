from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import requests

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/")
def index(request:Request):    
    return templates.TemplateResponse(request=request, name="index.html", context={"request":request})

@app.get("/start_task")
def start_task(request:Request):
    response = requests.get("http://myserver:8000/task")
    return response.content