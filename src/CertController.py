from models.CertsModel import *
import ssl
import socket
import datetime
from urllib.parse import urlparse

class CertController(object):
    def __init__(self, cert: generateCertClass) -> None:
        self.url = cert.url
        self.port = cert.port
        self.fmt= r"%b %d %H:%M:%S %Y %Z"
        self.ssl_info = self.__getSSLCertInfo()
    
    def __getSSLCertInfo(self) -> dict:
        port = self.port

        host = urlparse(self.url).netloc
        context = ssl.create_default_context()
        conn = context.wrap_socket(socket.socket(socket.AF_INET), server_hostname = host)
        conn.settimeout(3.0)
        conn.connect((host, port))
        return conn.getpeercert()
    

    def getSSLCertExpireDate(self) -> datetime.datetime:
        return datetime.datetime.strptime(self.ssl_info["notAfter"], self.fmt)

    def getSSLCertExpireUnixTime(self) -> datetime.datetime:
        return int(datetime.datetime.strptime(self.ssl_info["notAfter"], self.fmt).timestamp())
    
    def getSSLCertBeginDate(self) -> datetime.datetime:
        return datetime.datetime.strptime(self.ssl_info["notBefore"], self.fmt)
    
    def getSSLCertBeginUnixTime(self) -> datetime.datetime:
        return int(datetime.datetime.strptime(self.ssl_info["notBefore"], self.fmt).timestamp())

    def getSSLCertIssure(self) -> str:
        return self.ssl_info["issuer"][1][0][1]

    def getSSLCertState(self) -> str:
        nowtime = datetime.datetime.now()
        expire_date = self.getSSLCertExpireDate()
        delta = expire_date - nowtime
        days_left = delta.days
        # Fine
        if days_left >= 30:
            return 1
        # Expired
        elif days_left < 0:
            return 4
        # Danger
        elif days_left < 10:
            return 3
        # Warning
        elif days_left < 30:
            return 2

    def getRegisterCertModel(self) -> RegisterCert:
        cert = RegisterCert(
            url = self.url,
            port = self.port,
            sslCertExpireDate = self.getSSLCertExpireDate(),
            sslCertExpireUnixTime = self.getSSLCertExpireUnixTime(),
            sslCertBeginDate = self.getSSLCertBeginDate(),
            sslCertBeginUnixTime = self.getSSLCertBeginUnixTime(),
            sslCertState = self.getSSLCertState(),
            sslCertIssuer = self.getSSLCertIssure()
        )
        return cert