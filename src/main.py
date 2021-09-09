from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from PageHelper import PageHelper
from models.HostsModel import *

app = FastAPI()
site = PageHelper()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080", "http://192.168.56.105:8080"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message":"hi!"}

@app.get("/get")
async def getHosts(position: int=None, range: int=None):
    if position != None and range != None :
        return site.getAnyHostsList(position, range)
    else:
        return site.getAllHostsList()


@app.post("/set/hosts")
async def setHosts(host: RegisterHost):
    return site.registerHostData(host)


@app.post("/search")
async def searchHosts(searchword: SearchHost):
    return site.searchHostsList(searchword)