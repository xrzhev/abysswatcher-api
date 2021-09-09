from CertController import CertController
from models.HostsModel import *
from models.CertsModel import *
import json

from pydantic.types import Json
from DBController import DBController

class PageHelper(object):
    def __init__(self) -> None:
        pass

    def getAllHostsList(self) -> list:
        db = DBController()
        return self.convertHostsList2Json(db.getAllHosts())
        #return db.getAllHosts()
    

    def getAnyHostsList(self, begin: int, range:int) -> list:
        db = DBController()
        return self.convertHostsList2Json(db.getAnyHosts(begin, range))
        #return db.getAllHosts()

    def registerHostData(self, host: RegisterHost) -> dict:
        try: 
            db = DBController()
            # register host
            db.setHosts(host)
            # register cert
            for port in host.ports:
                cert_model = generateCertClass(url=host.url, port=port)
                cert = CertController(cert_model)
                db.setCert(cert.getRegisterCertModel())
            
            db.commit()
            return {"msg": "successful!"}
        except Exception as e:
            return {"msg": "missed...", "detail": repr(e)}
        
    
    def searchHostsList(self, word: SearchHost):
        db = DBController()
        data = db.searchHosts(word.searchword)
        return self.convertHostsList2Json(data)

        
    def convertHostsList2Json(self, hosts: list) -> json:
        container_json = []
        for host in hosts:
            data = {"id": host[0],"state":host[1], "name": host[2], "url": host[3], "certinfo": json.loads(host[4])}
            container_json.append(data)
        return container_json 
    
