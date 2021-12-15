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

    def registerHostData(self, host: RegisterHostModel) -> dict:
        try: 
            db = DBController()
            # register host
            db.setHosts(host)
            # register cert
            for port in host.ports:
                cert_model = GenerateCertModel(url=host.url, port=port)
                cert = CertController(cert_model)
                db.setCert(cert.getRegisterCertModel())
            
            db.commit()
            return {"msg": "successful!"}
        except Exception as e:
            return {"msg": "missed...", "detail": repr(e)}
        

    def updateCert(self, cert_id: UpdateCertModel) -> None:
        db = DBController()
        url, port = db.getGenCertModelFromCertId(cert_id.cert_id)[0]
        try:
            cert_model = GenerateCertModel(url=url, port=port)
            cert = CertController(cert_model)
            db.updateCert(cert.getRegisterCertModel(), cert_id.cert_id)
            db.commit()
            return {"msg": "update successful", "addr": f"{url}:{port}"}
        except Exception as e:
            return {"msg": "missed...", "addr": f"{url}:{port}", "error": repr(e)}
        
    def getCountRegistedCert(self):
        db = DBController()
        db.CUR.execute("SELECT COUNT(id) FROM certs")
        data = db.CUR.fetchall()[0][0]
        return data

        
    def convertHostsList2Json(self, hosts: list) -> json:
        container_json = []
        for host in hosts:
            data = {"id": host[0],"state":host[1], "name": host[2], "url": host[3], "port": host[4], "begin_date": host[5], "expire_date": host[6], "issuer": host[7]}
            container_json.append(data)
        return container_json 
    

    def getSlackNoticeData(self):
        db = DBController()
        danger_hosts = db.getCertStateDanger()
        expired_hosts = db.getCertStateExpired()

        return danger_hosts, expired_hosts