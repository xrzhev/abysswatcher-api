from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from PageHelper import PageHelper
from models.CertsModel import *
from models.HostsModel import *
from DBController import DBController
from concurrent import futures

app = FastAPI()
site = PageHelper()
db = DBController()

#
# DB初期インストール処理
#
if not db.isInitializedDB():
    print("DO INITIALIZE DB...")
    db.initInstall()
    db.commit()
del db


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


@app.post("/set/host")
async def setHost(host: RegisterHostModel):
    return site.registerHostData(host)


@app.post("/update/cert")
async def updateHost(cert_id: UpdateCertModel):
    return site.updateCert(cert_id)


@app.post("/update/allcert")
async def updateAllHost():
    thread_array = []
    error_count = 0
    error_id = []
    cert_len = int(site.getCountRegistedCert()) + 1
    with futures.ThreadPoolExecutor(max_workers=32) as executor:
        for i in range(1, cert_len):
            cert_id = UpdateCertModel(cert_id = i)
            future = executor.submit(site.updateCert, cert_id)
            thread_array.append(future)

        for future in thread_array:
            ret = future.result()
            print(ret)
            if ret["msg"] == "missed...":
                error_count += 1
                error_id.append(ret["addr"])

    return {"msg": "Update Done!", "error_count": f"{error_count}", "error_id":error_id }